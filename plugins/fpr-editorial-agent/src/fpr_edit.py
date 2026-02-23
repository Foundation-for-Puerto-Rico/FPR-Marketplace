#!/usr/bin/env python3
"""
FPR Editorial Agent — CLI entry point.

Usage:
    python src/fpr_edit.py <documento.docx> --project ERSV [options]
    python src/fpr_edit.py --refresh-kb --project WCRP
"""

import sys
import tempfile
from datetime import date
from pathlib import Path

import click

# Add repo root to sys.path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.knowledge_base import KnowledgeBase
from src.rule_engine import RuleEngine


@click.command()
@click.argument("document", required=False, type=click.Path(exists=True))
@click.option("--project", required=True, help="Project ID (ERSV, WCRP, or any folder in projects/)")
@click.option("--mode", default="light", type=click.Choice(["light", "deep", "audit"]), help="Editing mode")
@click.option("--audience", default=None, help="Audience profile ID")
@click.option("--lang", default="auto", type=click.Choice(["es", "en", "auto"]), help="Language")
@click.option("--author", default="FPR Editorial Agent", help="Author name for track changes")
@click.option("--output", default=None, help="Output path for edited document")
@click.option("--no-changelog", is_flag=True, help="Skip generating changelog")
@click.option("--refresh-kb", is_flag=True, help="Refresh knowledge base from sources (requires credentials)")
@click.option("--validate/--no-validate", default=True, help="Run XML validation on output")
@click.option("--export-heuristic", default=None, type=click.Path(), help="Export heuristic tasks to JSON file (for Claude Code evaluation)")
@click.option("--apply-heuristic", default=None, type=click.Path(exists=True), help="Apply heuristic results from JSON file")
def main(
    document,
    project,
    mode,
    audience,
    lang,
    author,
    output,
    no_changelog,
    refresh_kb,
    validate,
    export_heuristic,
    apply_heuristic,
):
    """FPR Editorial Agent — applies Foundation for Puerto Rico style guides as Word track changes."""

    if refresh_kb:
        click.echo(f"Knowledge base refresh for {project} is a manual operation.")
        click.echo("See CLAUDE.md Fase 1 for instructions to rebuild from SharePoint/RAG sources.")
        sys.exit(0)

    if document is None:
        click.echo("ERROR: A document path is required (unless using --refresh-kb).", err=True)
        sys.exit(1)

    doc_path = Path(document)
    if not doc_path.suffix.lower() == ".docx":
        click.echo("ERROR: Input file must be a .docx document.", err=True)
        sys.exit(1)

    # Determine output path
    if output:
        output_path = Path(output)
    else:
        output_path = doc_path.parent / f"{doc_path.stem}_FPRStyleAI_{date.today().isoformat()}.docx"

    today = date.today().isoformat()

    # Intermediate files go to system temp to avoid cluttering user's folder
    temp_base = Path(tempfile.gettempdir()) / "FPRStyleAI" / f"{doc_path.stem}_{today}"
    temp_base.mkdir(parents=True, exist_ok=True)
    changelog_path = temp_base / "changelog.md"
    flags_path = temp_base / "flags.md"

    click.echo(f"\nFPR Editorial Agent")
    click.echo(f"  Document : {doc_path.name}")
    click.echo(f"  Project  : {project}")
    click.echo(f"  Mode     : {mode}")
    click.echo(f"  Author   : {author}")
    click.echo()

    # Load knowledge base
    click.echo("Loading knowledge base...", nl=False)
    try:
        kb = KnowledgeBase(project)
        entries_count = len(kb.get_term_bank_entries())
        click.echo(f" {entries_count} term bank entries loaded.")
    except FileNotFoundError as e:
        click.echo(f"\nERROR: {e}", err=True)
        sys.exit(1)

    engine = RuleEngine(
        kb=kb,
        mode=mode,
        audience_id=audience,
        language=lang,
    )

    # Unpack document
    click.echo("Unpacking document...", nl=False)
    with tempfile.TemporaryDirectory() as tmp_dir:
        unpacked_dir = Path(tmp_dir) / "unpacked"
        unpacked_dir.mkdir()

        try:
            _unpack(doc_path, unpacked_dir)
            click.echo(" done.")
        except Exception as e:
            click.echo(f"\nERROR: Failed to unpack document: {e}", err=True)
            sys.exit(1)

        # --apply-heuristic: skip deterministic pass, load previous results + new heuristic
        if apply_heuristic:
            click.echo("Applying heuristic results from JSON...")
            result = _load_and_apply_heuristic(
                engine, unpacked_dir, Path(apply_heuristic)
            )
            _finish(result, unpacked_dir, doc_path, output_path, changelog_path,
                    flags_path, project, mode, author, no_changelog, validate)
            return

        # Run deterministic pass
        click.echo("Running deterministic pass...")
        try:
            result = engine.run(unpacked_dir)
        except Exception as e:
            click.echo(f"ERROR: Rule engine failed: {e}", err=True)
            sys.exit(1)

        total = len(result.high_confidence) + len(result.low_confidence)
        click.echo(f"  Found {total} deterministic suggestions:")
        click.echo(f"    {len(result.high_confidence)} high-confidence (-> track changes)")
        click.echo(f"    {len(result.low_confidence)} low-confidence (-> comments)")
        click.echo(f"    {len(result.skipped)} below threshold (ignored)")

        # For deep/audit modes, extract heuristic tasks
        if mode in ("deep", "audit"):
            heuristic_tasks = engine.extract_heuristic_tasks(unpacked_dir)
            click.echo(f"\n  Heuristic: {len(heuristic_tasks)} paragraphs to evaluate")

            if export_heuristic:
                # Export heuristic tasks to JSON for Claude Code to evaluate
                _export_heuristic_json(heuristic_tasks, Path(export_heuristic))
                click.echo(f"  Exported heuristic tasks to: {export_heuristic}")
                click.echo(
                    f"\n  Next step: evaluate each paragraph, then run again with:\n"
                    f"    python src/fpr_edit.py {doc_path} --project {project} "
                    f"--mode {mode} --apply-heuristic <results.json>"
                )
                return
            elif heuristic_tasks:
                # Default for deep/audit without export: print tasks for interactive use
                export_path = temp_base / "heuristic_tasks.json"
                _export_heuristic_json(heuristic_tasks, export_path)
                click.echo(f"  Exported heuristic tasks to: {export_path}")
                click.echo(
                    f"\n  To complete the heuristic pass, evaluate the tasks and run:\n"
                    f"    python src/fpr_edit.py {doc_path} --project {project} "
                    f"--mode {mode} --apply-heuristic <results.json>"
                )

        # Apply deterministic results
        _finish(result, unpacked_dir, doc_path, output_path, changelog_path,
                flags_path, project, mode, author, no_changelog, validate)


def _finish(result, unpacked_dir, doc_path, output_path, changelog_path,
            flags_path, project, mode, author, no_changelog, validate):
    """Apply changes and write output files."""
    total = len(result.high_confidence) + len(result.low_confidence)

    if mode == "audit":
        click.echo("\nAudit mode: generating flags file only (document not modified).")
        _write_flags(flags_path, result)
        click.echo(f"  Flags: {flags_path}")
        if not no_changelog:
            _write_changelog(changelog_path, result, doc_path.name, project, mode)
            click.echo(f"  Changelog: {changelog_path}")
        click.echo("\nDone.")
        return

    if total == 0:
        click.echo("\nNo suggestions to apply. Document is unchanged.")
        import shutil
        shutil.copy2(doc_path, output_path)
    else:
        click.echo("\nApplying changes...", nl=False)
        try:
            from src.docx_writer import DocxWriter
            writer = DocxWriter(
                unpacked_dir=unpacked_dir,
                original_docx=doc_path,
                author=author,
            )
            stats = writer.apply(result)
            click.echo(
                f" {stats['track_changes_applied']} track changes, "
                f"{stats['comments_applied']} comments applied."
            )
            if stats["failed"] > 0:
                click.echo(f"  WARNING: {stats['failed']} suggestions failed to apply.")

            click.echo(f"Saving output to {output_path.name}...", nl=False)
            writer.save(destination=output_path, validate=validate)
            click.echo(" done.")

        except Exception as e:
            click.echo(f"\nERROR: Failed to apply changes: {e}", err=True)
            sys.exit(1)

    if not no_changelog:
        _write_changelog(changelog_path, result, doc_path.name, project, mode)
        click.echo(f"  Changelog: {changelog_path}")

    if result.low_confidence:
        _write_flags(flags_path, result)
        click.echo(f"  Flags: {flags_path}")

    click.echo(f"\nDone. Output: {output_path}")


def _export_heuristic_json(tasks: list[dict], path: Path) -> None:
    """Export heuristic tasks to a JSON file for external evaluation."""
    import json
    # Strip the full context from export to keep file manageable
    export = []
    for task in tasks:
        export.append({
            "paragraph_index": task["paragraph_index"],
            "text": task["text"],
            "language": task["language"],
            "prompt": task["prompt"],
        })
    path.write_text(json.dumps(export, indent=2, ensure_ascii=False), encoding="utf-8")


def _load_and_apply_heuristic(engine, unpacked_dir, heuristic_json: Path):
    """Load heuristic results JSON and merge with a fresh deterministic pass."""
    import json
    from src.rule_engine import EngineResult

    # Run deterministic pass first
    result = engine.run(unpacked_dir)

    # Load heuristic suggestions
    data = json.loads(heuristic_json.read_text(encoding="utf-8"))

    # The JSON can be either a flat list of suggestions or per-paragraph results
    suggestions = []
    if isinstance(data, list):
        for item in data:
            if "suggestions" in item:
                # Per-paragraph format: {paragraph_index, suggestions: [...]}
                p_idx = item.get("paragraph_index", 0)
                for s in item["suggestions"]:
                    s.setdefault("paragraph_index", p_idx)
                    suggestions.append(s)
            elif "original" in item:
                # Flat format: direct suggestion objects
                suggestions.append(item)

    engine.add_heuristic_suggestions(result, suggestions)

    heur_high = sum(1 for s in result.high_confidence if s.source == "heuristic")
    heur_low = sum(1 for s in result.low_confidence if s.source == "heuristic")
    click.echo(f"  Heuristic: {heur_high} track changes + {heur_low} comments added")

    return result


def _unpack(docx_path: Path, target_dir: Path) -> None:
    """Unpack DOCX zip into target directory."""
    import zipfile
    import xml.dom.minidom

    with zipfile.ZipFile(docx_path, "r") as zf:
        zf.extractall(target_dir)

    # Pretty-print XML files for easier manipulation
    for xml_file in target_dir.rglob("*.xml"):
        try:
            content = xml_file.read_bytes()
            dom = xml.dom.minidom.parseString(content)
            pretty = dom.toprettyxml(indent="  ", encoding="utf-8")
            xml_file.write_bytes(pretty)
        except Exception:
            pass  # Leave file as-is if parsing fails


def _write_changelog(
    path: Path,
    result,
    doc_name: str,
    project: str,
    mode: str,
) -> None:
    """Write markdown changelog of applied changes."""
    from datetime import datetime

    lines = [
        f"# FPR Editorial Agent — Changelog",
        f"",
        f"**Document:** {doc_name}",
        f"**Project:** {project}",
        f"**Mode:** {mode}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## Track Changes Applied ({len(result.high_confidence)})",
        f"",
    ]

    for s in sorted(result.high_confidence, key=lambda x: x.paragraph_index):
        lines.append(f"- **[{s.rule_id}]** `{s.original}` → `{s.replacement}`")
        lines.append(f"  _{s.rationale}_")
        lines.append(f"")

    if result.low_confidence:
        lines += [
            f"## Comments Added ({len(result.low_confidence)})",
            f"",
        ]
        for s in sorted(result.low_confidence, key=lambda x: x.paragraph_index):
            lines.append(f"- **[{s.rule_id}]** `{s.original}` → `{s.replacement}` (confidence: {s.confidence:.0%})")
            lines.append(f"  _{s.rationale}_")
            lines.append(f"")

    path.write_text("\n".join(lines), encoding="utf-8")


def _write_flags(path: Path, result) -> None:
    """Write flags file for human review items."""
    lines = [
        "# FPR Editorial Agent — Flags for Human Review",
        "",
        "Items below require editorial judgment before accepting.",
        "",
    ]

    for s in result.low_confidence:
        lines.append(f"## [{s.rule_id}] Paragraph {s.paragraph_index}")
        lines.append(f"")
        lines.append(f"**Original:** `{s.original}`")
        lines.append(f"**Suggested:** `{s.replacement}`")
        lines.append(f"**Confidence:** {s.confidence:.0%}")
        lines.append(f"**Rationale:** {s.rationale}")
        lines.append(f"")

    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
