"""
DOCX writer for the FPR Editorial Agent.

Applies suggestions from the rule engine as native Word track changes
(high confidence) or Word comments (low confidence).

Track changes use lxml for cross-run text matching (handles Word's
arbitrary run fragmentation) and unique w:id assignment.
"""

from pathlib import Path
from datetime import datetime, timezone
from typing import Optional
import copy
import unicodedata

import lxml.etree

from src.rule_engine import EngineResult, Suggestion

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
W = f"{{{WORD_NS}}}"

# Namespace map for lxml element creation
NSMAP = {"w": WORD_NS}


class DocxWriter:
    """Applies editorial suggestions to an unpacked DOCX as track changes."""

    def __init__(
        self,
        unpacked_dir: Path,
        original_docx: Path,
        author: str = "FPR Editorial Agent",
        initials: str = "FPR",
    ):
        self.unpacked_dir = Path(unpacked_dir)
        self.original_docx = Path(original_docx)
        self.author = author
        self.initials = initials
        self._next_id_counter = None
        self._next_comment_id = 0

    def apply(self, result: EngineResult) -> dict:
        """Apply all suggestions from the engine result.

        High-confidence suggestions -> track changes (<w:ins>/<w:del>)
        Low-confidence suggestions -> Word comments

        Returns a dict with counts of applied/failed changes.
        """
        stats = {"track_changes_applied": 0, "comments_applied": 0, "failed": 0}

        # Initialize the ID counter by scanning the document for existing IDs
        self._init_id_counter()

        # Apply high-confidence suggestions as track changes
        # Already sorted end->start by the engine
        for suggestion in result.high_confidence:
            try:
                # Comment first — anchor needs original text before track change replaces it
                self._apply_comment(suggestion)
                self._apply_track_change(suggestion)
                stats["track_changes_applied"] += 1
                stats["comments_applied"] += 1
            except Exception as e:
                stats["failed"] += 1
                print(f"  WARNING: Failed to apply track change for '{suggestion.original}': {e}")

        # Apply low-confidence suggestions as Word comments (pure lxml)
        for suggestion in result.low_confidence:
            try:
                self._apply_comment(suggestion)
                stats["comments_applied"] += 1
            except Exception as e:
                stats["failed"] += 1
                print(f"  WARNING: Failed to apply comment for '{suggestion.original}': {e}")

        return stats

    # ------------------------------------------------------------------
    # Unique w:id management
    # ------------------------------------------------------------------

    def _init_id_counter(self) -> None:
        """Scan document.xml for the highest existing w:id and start from there."""
        doc_xml = self.unpacked_dir / "word" / "document.xml"
        tree = lxml.etree.parse(str(doc_xml))
        root = tree.getroot()

        max_id = 0
        for elem in root.iter():
            wid = elem.get(f"{W}id")
            if wid is not None:
                try:
                    max_id = max(max_id, int(wid))
                except ValueError:
                    pass
        self._next_id_counter = max_id + 1

    def _next_id(self) -> int:
        """Return the next unique w:id and increment the counter."""
        val = self._next_id_counter
        self._next_id_counter += 1
        return val

    # ------------------------------------------------------------------
    # Track changes — cross-run matching
    # ------------------------------------------------------------------

    def _apply_track_change(self, suggestion: Suggestion) -> None:
        """Replace occurrence of original text with tracked ins/del pair.

        Handles text that spans multiple <w:r> elements (run fragmentation)
        by concatenating run texts per paragraph, finding the match, and
        splitting/replacing the affected runs.
        """
        doc_xml = self.unpacked_dir / "word" / "document.xml"
        tree = lxml.etree.parse(str(doc_xml))
        root = tree.getroot()

        original = unicodedata.normalize("NFC", suggestion.original)
        replacement = unicodedata.normalize("NFC", suggestion.replacement)

        # Search all paragraphs for the match
        for para in root.iter(f"{W}p"):
            runs = self._get_text_runs(para)
            if not runs:
                continue

            # Build concatenated text with offset map
            concat_text, offset_map = self._build_offset_map(runs)

            # Find the match in concatenated text
            idx = concat_text.find(original)
            if idx == -1:
                continue

            # Found match — identify affected runs
            match_start = idx
            match_end = idx + len(original)

            affected = self._get_affected_runs(offset_map, match_start, match_end)
            if not affected:
                continue

            # Extract rPr from the first affected run
            rpr_xml = self._extract_rpr_lxml(affected[0]["run"])

            # Build the replacement nodes
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            del_id = self._next_id()
            ins_id = self._next_id()

            # Calculate prefix (text before match in first run) and
            # suffix (text after match in last run)
            first = affected[0]
            last = affected[-1]
            prefix_text = first["text"][:match_start - first["offset"]]
            suffix_text = last["text"][match_end - last["offset"]:]

            # Build new XML elements to insert
            new_elements = []

            # Prefix run (text before the match in the first affected run)
            if prefix_text:
                new_elements.append(self._make_run_elem(prefix_text, rpr_xml))

            # <w:del> with the original text
            new_elements.append(self._make_del_elem(original, rpr_xml, del_id, timestamp))

            # <w:ins> with the replacement text (skip for pure deletions)
            if replacement:
                new_elements.append(self._make_ins_elem(replacement, rpr_xml, ins_id, timestamp))

            # Suffix run (text after the match in the last affected run)
            if suffix_text:
                new_elements.append(self._make_run_elem(suffix_text, rpr_xml))

            # Replace the affected runs in the paragraph.
            # Runs may have different parents (e.g., one inside <w:hyperlink>,
            # another directly in <w:p>). Insert new elements at the position
            # of the first run's parent container within the paragraph.
            first_run = affected[0]["run"]
            first_parent = first_run.getparent()

            # If first run's parent is the paragraph itself, insert directly.
            # Otherwise, insert at the parent container's position in the paragraph.
            if first_parent.tag == f"{W}p":
                insert_parent = first_parent
                insert_pos = list(insert_parent).index(first_run)
            else:
                # Run is inside a wrapper (hyperlink, smartTag, etc.)
                # Insert new elements at the wrapper's position in the paragraph
                insert_parent = para
                insert_pos = list(para).index(first_parent)

            # Remove all affected runs from their respective parents
            for a in affected:
                run_parent = a["run"].getparent()
                run_parent.remove(a["run"])
                # Clean up empty wrapper elements
                if run_parent.tag != f"{W}p" and len(run_parent) == 0:
                    wrapper_parent = run_parent.getparent()
                    if wrapper_parent is not None:
                        wrapper_parent.remove(run_parent)

            # Insert new elements at the resolved position
            for i, elem in enumerate(new_elements):
                insert_parent.insert(insert_pos + i, elem)

            # Write back
            tree.write(str(doc_xml), xml_declaration=True, encoding="UTF-8", standalone=True)
            return

        raise ValueError(f"Text not found in any paragraph: '{original}'")

    def _get_text_runs(self, para):
        """Get all <w:r> elements in a paragraph that contain <w:t> text.

        Finds runs that are direct children of the paragraph AND runs
        nested inside non-tracked-change wrappers (e.g., <w:hyperlink>,
        <w:smartTag>). Skips runs inside <w:del> or <w:ins> elements
        to avoid re-processing already-tracked changes.

        Returns list of {"run": element, "text": str} dicts.
        """
        results = []
        # Use findall to get ALL <w:r> descendants, then filter
        for run in para.findall(f".//{W}r"):
            # Skip runs inside tracked changes (w:del or w:ins)
            ancestor = run.getparent()
            inside_tracked = False
            while ancestor is not None and ancestor is not para:
                if ancestor.tag in (f"{W}del", f"{W}ins"):
                    inside_tracked = True
                    break
                ancestor = ancestor.getparent()
            if inside_tracked:
                continue

            text_parts = []
            for t_elem in run.findall(f"{W}t"):
                if t_elem.text:
                    text_parts.append(unicodedata.normalize("NFC", t_elem.text))
            if text_parts:
                results.append({"run": run, "text": "".join(text_parts)})
        return results

    def _build_offset_map(self, runs):
        """Build concatenated text and offset map from runs.

        Returns (full_text, list of {run, text, offset}).
        """
        offset = 0
        mapped = []
        parts = []
        for r in runs:
            mapped.append({"run": r["run"], "text": r["text"], "offset": offset})
            parts.append(r["text"])
            offset += len(r["text"])
        return "".join(parts), mapped

    def _get_affected_runs(self, offset_map, match_start, match_end):
        """Return the subset of offset_map entries that overlap with [match_start, match_end)."""
        affected = []
        for entry in offset_map:
            run_start = entry["offset"]
            run_end = run_start + len(entry["text"])
            # Check overlap: run intersects [match_start, match_end)
            if run_start < match_end and run_end > match_start:
                affected.append(entry)
        return affected

    def _extract_rpr_lxml(self, run_elem) -> Optional[lxml.etree._Element]:
        """Extract <w:rPr> from a run element, or None if absent."""
        rpr = run_elem.find(f"{W}rPr")
        if rpr is not None:
            import copy
            return copy.deepcopy(rpr)
        return None

    def _make_run_elem(self, text, rpr):
        """Create a <w:r> element with optional <w:rPr> and <w:t>."""
        r = lxml.etree.Element(f"{W}r")
        if rpr is not None:
            import copy
            r.append(copy.deepcopy(rpr))
        t = lxml.etree.SubElement(r, f"{W}t")
        t.text = text
        # Preserve whitespace
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        return r

    def _make_del_elem(self, text, rpr, wid, timestamp):
        """Create a <w:del> element wrapping a run with <w:delText>."""
        del_elem = lxml.etree.Element(f"{W}del")
        del_elem.set(f"{W}id", str(wid))
        del_elem.set(f"{W}author", self.author)
        del_elem.set(f"{W}date", timestamp)

        r = lxml.etree.SubElement(del_elem, f"{W}r")
        if rpr is not None:
            import copy
            r.append(copy.deepcopy(rpr))
        dt = lxml.etree.SubElement(r, f"{W}delText")
        dt.text = text
        dt.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        return del_elem

    def _make_ins_elem(self, text, rpr, wid, timestamp):
        """Create a <w:ins> element wrapping a run with <w:t>."""
        ins_elem = lxml.etree.Element(f"{W}ins")
        ins_elem.set(f"{W}id", str(wid))
        ins_elem.set(f"{W}author", self.author)
        ins_elem.set(f"{W}date", timestamp)

        r = lxml.etree.SubElement(ins_elem, f"{W}r")
        if rpr is not None:
            import copy
            r.append(copy.deepcopy(rpr))
        t = lxml.etree.SubElement(r, f"{W}t")
        t.text = text
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
        return ins_elem

    # ------------------------------------------------------------------
    # Comments (low confidence)
    # ------------------------------------------------------------------

    def _apply_comment(self, suggestion: Suggestion) -> None:
        """Add a Word comment using pure lxml — no minidom/Document mixing."""
        comment_id = self._next_comment_id
        self._next_comment_id += 1

        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        comment_text = (
            f"{suggestion.rationale}\n"
            f"Suggested: {suggestion.replacement!r}\n"
            f"Confidence: {suggestion.confidence:.0%}"
        )

        # 1. Inject comment range markers into document.xml
        self._inject_comment_anchors(suggestion.original, comment_id, timestamp)

        # 2. Append comment entry to comments.xml
        self._append_to_comments_xml(comment_id, comment_text, timestamp)

    def _inject_comment_anchors(self, original: str, comment_id: int, timestamp: str) -> None:
        """Insert commentRangeStart/End and commentReference around the target run."""
        doc_xml = self.unpacked_dir / "word" / "document.xml"
        tree = lxml.etree.parse(str(doc_xml))
        root = tree.getroot()

        original = unicodedata.normalize("NFC", original)

        for para in root.iter(f"{W}p"):
            runs = self._get_text_runs(para)
            if not runs:
                continue
            concat_text, offset_map = self._build_offset_map(runs)
            idx = concat_text.find(original)
            if idx == -1:
                continue

            # Use the first affected run as the anchor
            affected = self._get_affected_runs(offset_map, idx, idx + len(original))
            if not affected:
                continue
            anchor_run = affected[0]["run"]
            parent = anchor_run.getparent()
            pos = list(parent).index(anchor_run)

            # <w:commentRangeStart w:id="N"/>
            cs = lxml.etree.Element(f"{W}commentRangeStart")
            cs.set(f"{W}id", str(comment_id))
            parent.insert(pos, cs)

            # <w:commentRangeEnd w:id="N"/> — after the anchor run (pos+2 because we inserted cs)
            ce = lxml.etree.Element(f"{W}commentRangeEnd")
            ce.set(f"{W}id", str(comment_id))
            anchor_pos_after = list(parent).index(anchor_run) + 1
            parent.insert(anchor_pos_after, ce)

            # <w:r><w:rPr><w:rStyle w:val="CommentReference"/></w:rPr>
            #   <w:commentReference w:id="N"/></w:r>
            ref_run = lxml.etree.Element(f"{W}r")
            rpr = lxml.etree.SubElement(ref_run, f"{W}rPr")
            rs = lxml.etree.SubElement(rpr, f"{W}rStyle")
            rs.set(f"{W}val", "CommentReference")
            cref = lxml.etree.SubElement(ref_run, f"{W}commentReference")
            cref.set(f"{W}id", str(comment_id))
            parent.insert(anchor_pos_after + 1, ref_run)

            tree.write(str(doc_xml), xml_declaration=True, encoding="UTF-8", standalone=True)
            return

        raise ValueError(f"Text not found for comment anchor: '{original}'")

    def _append_to_comments_xml(self, comment_id: int, text: str, timestamp: str) -> None:
        """Append a <w:comment> entry to word/comments.xml (create if needed)."""
        import xml.sax.saxutils as saxutils
        comments_xml = self.unpacked_dir / "word" / "comments.xml"

        # Ensure comments.xml exists with proper namespaces
        if not comments_xml.exists():
            comments_xml.write_text(
                '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
                '<w:comments'
                ' xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
                ' xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml"'
                '></w:comments>',
                encoding="utf-8",
            )
            self._ensure_comments_relationship()
            self._ensure_comments_content_type()

        tree = lxml.etree.parse(str(comments_xml))
        root = tree.getroot()

        # Build <w:comment> element
        comment_elem = lxml.etree.SubElement(root, f"{W}comment")
        comment_elem.set(f"{W}id", str(comment_id))
        comment_elem.set(f"{W}author", self.author)
        comment_elem.set(f"{W}date", timestamp)
        comment_elem.set(f"{W}initials", self.initials)

        p = lxml.etree.SubElement(comment_elem, f"{W}p")
        r = lxml.etree.SubElement(p, f"{W}r")
        t = lxml.etree.SubElement(r, f"{W}t")
        t.text = text
        t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")

        tree.write(str(comments_xml), xml_declaration=True, encoding="UTF-8", standalone=True)

    def _ensure_comments_relationship(self) -> None:
        """Add comments.xml relationship to word/_rels/document.xml.rels if missing."""
        rels_path = self.unpacked_dir / "word" / "_rels" / "document.xml.rels"
        if not rels_path.exists():
            return
        content = rels_path.read_text(encoding="utf-8")
        if "comments" in content.lower():
            return
        # Insert before closing tag
        rel = (
            '<Relationship Id="rIdComments"'
            ' Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments"'
            ' Target="comments.xml"/>'
        )
        content = content.replace("</Relationships>", f"  {rel}\n</Relationships>")
        rels_path.write_text(content, encoding="utf-8")

    def _ensure_comments_content_type(self) -> None:
        """Add comments content type to [Content_Types].xml if missing."""
        ct_path = self.unpacked_dir / "[Content_Types].xml"
        if not ct_path.exists():
            return
        content = ct_path.read_text(encoding="utf-8")
        if "comments" in content.lower():
            return
        override = (
            '<Override PartName="/word/comments.xml"'
            ' ContentType="application/vnd.openxmlformats-officedocument'
            '.wordprocessingml.comments+xml"/>'
        )
        content = content.replace("</Types>", f"  {override}\n</Types>")
        ct_path.write_text(content, encoding="utf-8")

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, destination: Optional[Path] = None, validate: bool = True) -> None:
        """Pack the unpacked directory into a DOCX zip."""
        import subprocess, sys
        if destination:
            target = Path(destination)
        else:
            from datetime import date
            target = self.original_docx.parent / f"{self.original_docx.stem}_FPRStyleAI_{date.today().isoformat()}.docx"
        pack_script = Path(__file__).parent.parent / "scripts" / "office" / "pack.py"
        cmd = [sys.executable, str(pack_script), str(self.unpacked_dir), str(target), "--force"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"pack.py failed: {result.stderr.strip()}")
