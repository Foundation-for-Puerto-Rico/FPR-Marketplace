# CLI Reference — fpr_edit.py

## Location

The CLI lives at `src/fpr_edit.py` relative to the plugin root.

## Usage

```
python src/fpr_edit.py <document.docx> --project <ERSV|WCRP> [options]
```

## Required Arguments

| Argument | Description |
|----------|-------------|
| `<document.docx>` | Path to input DOCX file |
| `--project` | Project ID: `ERSV` or `WCRP` |

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--mode light\|deep\|audit` | `light` | Editing mode |
| `--audience` | (project default) | Audience profile ID |
| `--lang es\|en\|auto` | `auto` | Language override |
| `--author` | `FPR Editorial Agent` | Author name for track changes |
| `--output` | `{stem}_FPRStyleAI_{date}.docx` | Custom output path |
| `--no-changelog` | false | Skip changelog generation |
| `--export-heuristic <path>` | none | Export heuristic tasks to JSON |
| `--apply-heuristic <path>` | none | Apply heuristic results from JSON |
| `--no-validate` | false | Skip XML validation on output |

## Modes

- **light**: Deterministic pass only (term bank substitutions). Fast, fully automated.
- **deep**: Deterministic + heuristic. Exports `_heuristic_tasks.json` for Claude to evaluate, then merges with `--apply-heuristic`.
- **audit**: Like deep but does not modify the document. Produces flags file only.

## Output Files

For input `report.docx`:
- `report_FPRStyleAI_2026-02-22.docx` — edited document
- `report_FPRStyleAI_2026-02-22_changelog.md` — change log
- `report_FPRStyleAI_2026-02-22_flags.md` — flagged items (if any)

## Deep Mode Two-Step Flow

1. First run exports heuristic tasks:
   ```
   python src/fpr_edit.py doc.docx --project ERSV --mode deep
   ```
   Produces `doc_heuristic_tasks.json`

2. After evaluating paragraphs, apply results:
   ```
   python src/fpr_edit.py doc.docx --project ERSV --mode deep --apply-heuristic doc_heuristic_results.json
   ```
