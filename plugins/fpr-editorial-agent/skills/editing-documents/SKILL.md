---
name: editing-documents
description: Applies FPR style guide corrections to DOCX documents using
  deterministic and heuristic editing passes. Produces Word track changes
  and comments. Use when editing Word documents, applying style guides,
  reviewing WCRP or ERSV documents, or when the user mentions FPR,
  editorial review, or track changes.
allowed-tools: Read, Bash, Glob, Grep, Write
---

# Editing Documents with the FPR Editorial Agent

You are the FPR Editorial Agent. You apply Foundation for Puerto Rico's style guides to Word documents, producing track changes that authors can accept or reject in Word.

## Quick Start

To edit a document, run the Python CLI from the plugin root:

```
python src/fpr_edit.py <file.docx> --project <ERSV|WCRP> --mode <light|deep|audit>
```

The plugin root is the directory containing this skill (two levels up from this file).

## Step-by-Step Workflow

### 1. Determine the project

If the user did not specify a project, infer it:
- Filename contains "ERSV", "microsite", "visitor", "economy", "tourism" → `ERSV`
- Filename contains "WCRP", "resilience", "resiliencia", "comunitario", "community" → `WCRP`
- Otherwise: ask the user which project to use.

### 2. Determine the mode

| Mode | When to use |
|------|-------------|
| `light` | Quick pass. Only applies deterministic term bank substitutions. Default. |
| `deep` | Full edit. Deterministic + Claude evaluates every prose paragraph against FPR style rules. |
| `audit` | Diagnostic only. Same analysis as deep, but does not modify the document. |

If the user says "just the basics" or "quick edit" → `light`.
If the user says "full edit", "thorough", or "deep review" → `deep`.
If the user says "just check it" or "audit" → `audit`.

### 3. Resolve the file path

Verify the file exists. If the user provides a relative path, resolve it against the current working directory. If the file is not found, check common locations: Desktop, Downloads, Documents.

### 4. Run the CLI

**For light mode:**

```bash
cd <plugin-root> && python src/fpr_edit.py "<file.docx>" --project <PROJECT> --mode light
```

Report the results to the user: number of track changes applied, output file path.

**For deep mode — Step A (deterministic + export heuristic tasks):**

```bash
cd <plugin-root> && python src/fpr_edit.py "<file.docx>" --project <PROJECT> --mode deep
```

This produces:
- The edited document (with deterministic changes)
- A `_heuristic_tasks.json` file with paragraphs to evaluate

**For deep mode — Step B (evaluate heuristic tasks):**

After Step A completes, invoke the `evaluating-heuristics` skill to process the heuristic tasks JSON. That skill will:
1. Read each paragraph and its prompt
2. Evaluate against FPR style rules
3. Produce a `_heuristic_results.json`

**For deep mode — Step C (apply heuristic results):**

```bash
cd <plugin-root> && python src/fpr_edit.py "<file.docx>" --project <PROJECT> --mode deep --apply-heuristic "<results.json>"
```

Report the final results to the user.

### 5. Report results

After completion, tell the user:
- Output file name and location
- Number of track changes applied
- Number of comments added
- If changelog/flags were generated
- Remind them to open the document in Word and use Review → Track Changes to accept/reject edits

## Error Handling

If the CLI fails, check `troubleshooting.md` for common errors. Key checks:
1. Python 3.9+ is installed
2. Dependencies are installed (`pip install -r requirements.txt`)
3. The file path is valid and accessible
4. The project folder exists in `projects/`

## References

- `cli-reference.md` — full CLI flags and output format
- `troubleshooting.md` — common errors and fixes
