"""
Rule engine for the FPR Editorial Agent.

Implements two passes:
1. Deterministic: regex-based term bank substitutions on <w:t> text content
2. Heuristic: paragraphs + context exported for Claude Desktop/Code to evaluate externally
"""

import json
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import lxml.etree

from src.knowledge_base import KnowledgeBase

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


@dataclass
class Suggestion:
    """A single editorial suggestion."""
    original: str
    replacement: str
    rule_id: str
    confidence: float
    rationale: str
    paragraph_index: int
    source: str  # "deterministic" or "heuristic"


@dataclass
class EngineResult:
    """Results from a full engine run."""
    high_confidence: list[Suggestion] = field(default_factory=list)   # ≥ threshold → track changes
    low_confidence: list[Suggestion] = field(default_factory=list)    # mid-range → Word comments
    skipped: list[Suggestion] = field(default_factory=list)           # below ignore threshold


class RuleEngine:
    """Two-pass editorial rule engine."""

    def __init__(
        self,
        kb: KnowledgeBase,
        mode: str = "light",
        audience_id: Optional[str] = None,
        language: str = "auto",
    ):
        self.kb = kb
        self.mode = mode
        self.audience_id = audience_id
        self.language = language
        self.thresholds = kb.get_confidence_thresholds()

    def run(self, unpacked_dir: Path) -> EngineResult:
        """Run both passes and return classified suggestions."""
        doc_xml = unpacked_dir / "word" / "document.xml"
        if not doc_xml.exists():
            raise FileNotFoundError(f"document.xml not found at {doc_xml}")

        tree = lxml.etree.parse(str(doc_xml))
        root = tree.getroot()

        result = EngineResult()

        # Pass 1: deterministic term bank
        det_suggestions = self._deterministic_pass(root)
        for s in det_suggestions:
            self._classify(s, result)

        # Pass 2: heuristic paragraphs are exported via extract_heuristic_tasks()
        # for Claude Desktop/Code to evaluate externally. Call add_heuristic_suggestions()
        # to incorporate the results back.

        # Sort all suggestions by paragraph_index descending (process end→start)
        for lst in (result.high_confidence, result.low_confidence):
            lst.sort(key=lambda s: s.paragraph_index, reverse=True)

        return result

    def _classify(self, suggestion: Suggestion, result: EngineResult) -> None:
        high = self.thresholds.get("high_confidence_track_change", 0.85)
        low = self.thresholds.get("low_confidence_comment", 0.60)
        ignore = self.thresholds.get("ignore_below", 0.60)

        if suggestion.confidence >= high:
            result.high_confidence.append(suggestion)
        elif suggestion.confidence >= low:
            result.low_confidence.append(suggestion)
        else:
            result.skipped.append(suggestion)

    # ------------------------------------------------------------------
    # DETERMINISTIC PASS
    # ------------------------------------------------------------------

    def _deterministic_pass(self, root) -> list[Suggestion]:
        """Apply term bank substitutions to <w:t> text content."""
        entries = self.kb.get_term_bank_entries() + self.kb.get_ai_humanizer_entries()
        protected = set(self.kb.get_protected_terms())
        suggestions = []

        paragraphs = root.findall(f".//{{{WORD_NS}}}p")

        # Track which context_aware rules have already been applied (first-reference only)
        applied_context_aware: set[str] = set()

        # Build full document text for checking if replacement already exists
        all_para_texts = []
        for para in paragraphs:
            all_para_texts.append(self._get_para_text(para))
        full_doc_text = "\n".join(all_para_texts)

        for p_idx, para in enumerate(paragraphs):
            para_type = self._get_paragraph_type(para)
            para_text = all_para_texts[p_idx]

            for entry in entries:
                applies_in = entry.get("applies_in", ["prose"])
                if para_type not in applies_in:
                    continue

                original = unicodedata.normalize("NFC", entry.get("original", ""))
                replacement = unicodedata.normalize("NFC", entry.get("replacement", ""))
                if not original or replacement == original:
                    continue

                # Skip if the original is a protected term
                if original in protected:
                    continue

                case_sensitive = entry.get("case_sensitive", True)
                context_aware = entry.get("context_aware", False)
                rule_id = entry.get("id", "UNKNOWN")

                if context_aware:
                    # Skip if this rule was already applied earlier in the document
                    if rule_id in applied_context_aware:
                        continue
                    # Skip if the expanded form already exists anywhere in the document
                    if replacement.lower() in full_doc_text.lower():
                        continue

                # Match in paragraph text
                flags = 0 if case_sensitive else re.IGNORECASE
                pattern_type = entry.get("pattern_type", "literal")
                if pattern_type == "regex":
                    pattern = original
                else:
                    pattern = re.escape(original)
                match = re.search(pattern, para_text, flags)
                if match:
                    # Use the actual matched text from the document (preserves case)
                    # so the docx_writer can find it with exact string match
                    matched_text = match.group(0)
                    suggestions.append(Suggestion(
                        original=matched_text,
                        replacement=replacement,
                        rule_id=rule_id,
                        confidence=1.0,
                        rationale=entry.get("rule", "Term bank substitution"),
                        paragraph_index=p_idx,
                        source="deterministic",
                    ))
                    # Mark context_aware rules as applied so they don't fire again
                    if context_aware:
                        applied_context_aware.add(rule_id)

        return suggestions

    def _get_paragraph_type(self, para) -> str:
        """Classify a paragraph as prose, heading, table, or footnote."""
        # Check if inside a table cell
        parent = para.getparent()
        while parent is not None:
            if parent.tag == f"{{{WORD_NS}}}tbl":
                return "tables"
            parent = parent.getparent()

        # Check paragraph style for headings
        pPr = para.find(f"{{{WORD_NS}}}pPr")
        if pPr is not None:
            pStyle = pPr.find(f"{{{WORD_NS}}}pStyle")
            if pStyle is not None:
                style_val = pStyle.get(f"{{{WORD_NS}}}val", "")
                if style_val.lower().startswith("heading"):
                    return "headings"
                if "footnote" in style_val.lower() or "endnote" in style_val.lower():
                    return "footnotes"

        return "prose"

    def _get_para_text(self, para) -> str:
        """Extract all text content from a paragraph element (NFC-normalized)."""
        texts = []
        for t in para.findall(f".//{{{WORD_NS}}}t"):
            if t.text:
                texts.append(unicodedata.normalize("NFC", t.text))
        return "".join(texts)

    # ------------------------------------------------------------------
    # HEURISTIC PASS — export/import for Claude Desktop/Code
    # ------------------------------------------------------------------

    def extract_heuristic_tasks(self, unpacked_dir: Path) -> list[dict]:
        """Extract prose paragraphs with context for external heuristic evaluation.

        Returns a list of dicts, each containing:
        - paragraph_index: int
        - text: str (paragraph text)
        - language: str (detected language)
        - context: str (active rules context)
        - prompt: str (ready-to-use evaluation prompt)

        Claude Desktop (via MCP) or Claude Code evaluates these and returns
        suggestions via add_heuristic_suggestions().
        """
        doc_xml = unpacked_dir / "word" / "document.xml"
        if not doc_xml.exists():
            return []

        tree = lxml.etree.parse(str(doc_xml))
        root = tree.getroot()
        paragraphs = root.findall(f".//{{{WORD_NS}}}p")

        context = self.kb.build_heuristic_context(
            mode=self.mode,
            audience_id=self.audience_id,
            language=self.language,
        )

        tasks = []
        for p_idx, para in enumerate(paragraphs):
            if self._get_paragraph_type(para) != "prose":
                continue

            para_text = self._get_para_text(para).strip()
            if len(para_text) < 20:
                continue

            para_lang = self._detect_language(para_text) if self.language == "auto" else self.language

            lang_instruction = (
                "Responde ÚNICAMENTE en JSON. Evalúa el texto en español."
                if para_lang == "es"
                else "Respond ONLY in JSON. Evaluate the text in English."
            )

            prompt = f"""{lang_instruction}

ACTIVE RULES CONTEXT:
{context}

TEXT TO EVALUATE:
{para_text}

TASK:
Identify style violations. For each one, return EXACTLY this JSON format:
{{
  "suggestions": [
    {{
      "original": "exact minimum text to replace",
      "replacement": "suggested replacement",
      "rule_id": "rule ID applied",
      "confidence": 0.0,
      "rationale": "one-line explanation"
    }}
  ]
}}

CRITICAL CONSTRAINTS:
- "original" must be the MINIMUM string containing the problem (never the whole sentence if the problem is one word)
- confidence 0.60+ = auto track change with explanatory comment; below 0.60 = ignored
- Do NOT suggest changes that violate preserve-first, certainty upgrades, or equity framing
- Do NOT suggest changes to protected terms
- If the paragraph has no problems, return {{"suggestions": []}}"""

            tasks.append({
                "paragraph_index": p_idx,
                "text": para_text,
                "language": para_lang,
                "context": context,
                "prompt": prompt,
            })

        return tasks

    def add_heuristic_suggestions(
        self,
        result: EngineResult,
        suggestions_data: list[dict],
    ) -> None:
        """Incorporate heuristic suggestions from Claude Desktop/Code.

        Args:
            result: The EngineResult to add suggestions to.
            suggestions_data: List of dicts with keys:
                original, replacement, rule_id, confidence, rationale, paragraph_index
        """
        heuristic_mode = self.kb.get_modes().get(self.mode, {})
        applies = heuristic_mode.get("applies", [])
        high_only = "heuristic_high_confidence_only" in applies and "heuristic_all" not in applies

        for item in suggestions_data:
            original = item.get("original", "").strip()
            replacement = item.get("replacement", "").strip()
            confidence = float(item.get("confidence", 0.0))

            if not original or not replacement or original == replacement:
                continue
            if confidence < self.thresholds.get("ignore_below", 0.60):
                continue
            if high_only and confidence < self.thresholds.get("high_confidence_track_change", 0.85):
                continue

            suggestion = Suggestion(
                original=original,
                replacement=replacement,
                rule_id=item.get("rule_id", "HEURISTIC"),
                confidence=confidence,
                rationale=item.get("rationale", ""),
                paragraph_index=item.get("paragraph_index", 0),
                source="heuristic",
            )
            self._classify(suggestion, result)

        # Re-sort after adding heuristic suggestions
        for lst in (result.high_confidence, result.low_confidence):
            lst.sort(key=lambda s: s.paragraph_index, reverse=True)

    def _detect_language(self, text: str) -> str:
        """Simple heuristic language detection (es/en) per paragraph."""
        spanish_indicators = [
            "de ", "la ", "el ", "en ", "los ", "las ", "que ", "del ", "con ", "para ",
            "por ", "una ", "como ", "es ", "su ", "se ", "al ", "no ", "esta ", "son ",
        ]
        text_lower = text.lower()
        spanish_count = sum(1 for ind in spanish_indicators if ind in text_lower)
        return "es" if spanish_count >= 3 else "en"
