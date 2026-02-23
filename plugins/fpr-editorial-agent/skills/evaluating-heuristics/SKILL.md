---
name: evaluating-heuristics
description: Evaluates paragraphs extracted from DOCX documents against FPR
  style rules and produces heuristic suggestions with track change markup.
  Use after editing-documents skill produces a heuristic_tasks.json in deep
  or audit mode. Handles FPR editorial review, style evaluation, WCRP and
  ERSV paragraph analysis.
allowed-tools: Read, Write
---

# Evaluating Heuristic Tasks

You evaluate prose paragraphs against FPR style rules and produce a JSON file of suggestions. This skill is invoked by the `editing-documents` skill after the deterministic pass exports a `_heuristic_tasks.json`.

## THIS IS A RIGID SKILL — Follow the protocol exactly.

## Input

A JSON file (typically `*_heuristic_tasks.json`) containing an array of objects:

```json
[
  {
    "paragraph_index": 42,
    "text": "The paragraph text from the document...",
    "language": "en",
    "prompt": "Full evaluation prompt with rules context..."
  }
]
```

## Protocol

### Step 1: Read the heuristic tasks file

Use the Read tool to load the JSON file. Note the total count of paragraphs.

### Step 2: Evaluate each paragraph

For each task in the array:
1. Read the `prompt` field — it contains the full evaluation context including active rules
2. Evaluate the paragraph text against the rules described in the prompt
3. For each style violation found, create a suggestion object

### Step 3: Write the results file

Write a JSON file with ALL suggestions from all paragraphs:

```json
[
  {
    "paragraph_index": 42,
    "original": "exact minimum text to replace",
    "replacement": "suggested replacement",
    "rule_id": "NNQ-002",
    "confidence": 0.75,
    "rationale": "One-line explanation of why this change improves the text"
  }
]
```

Save to the same directory as the input file, with name `*_heuristic_results.json` (replace `_tasks` with `_results` in the filename).

### Step 4: Report completion

Tell the user:
- How many paragraphs were evaluated
- How many suggestions were produced
- The path to the results file
- Instruct them (or the editing-documents skill) to run the apply step

## CRITICAL CONSTRAINTS — Violations are failures

1. **`original` field = minimum text.** If the problem is one word, `original` is that one word. Never put the entire sentence in `original`.

2. **Never upgrade certainty.** Do NOT change: may→will, aims to→ensures, can help→guarantees, seeks to→achieves, is intended to→delivers. If you see cautious language, LEAVE IT.

3. **Never touch protected terms.** Protected terms are project-specific and listed in `projects/{PROJECT}/protected-lexicon.yaml`. The prompt context mentions key protected phrases. Do not suggest changes to any of them.

4. **Confidence must be calibrated:**
   - 0.90-1.0: Clear grammar error, obvious typo, unambiguous terminology fix
   - 0.75-0.89: Clarity improvement, sentence structure fix, AI pattern rewrite
   - 0.60-0.74: Subjective improvement, minor style preference
   - Below 0.60: Do not include — it will be ignored

5. **Preserve FPR voice.** If a change makes text shorter but flattens the institutional voice (removes systems framing, equity language, or transformation narrative), do NOT suggest it.

6. **Empty array is valid.** If a paragraph has no problems, produce no suggestions for that paragraph. Not every paragraph needs a change.

7. **JSON format must be exact.** Each suggestion is a flat object with exactly these 6 keys: `paragraph_index`, `original`, `replacement`, `rule_id`, `confidence`, `rationale`.

8. **Replacement "" (empty string) means deletion.** Use this for filler words or phrases that should be removed entirely.

## References

- `style-rules.md` — FPR voice, clarity, AI-humanizer rules condensed
- `examples.md` — real input/output evaluation pairs showing correct behavior
