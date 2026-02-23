---
name: edit
description: Edit a DOCX document using FPR style guides
arguments:
  - name: file
    description: Path to the DOCX file
    required: true
  - name: project
    description: "Project ID (ERSV or WCRP)"
    required: false
  - name: mode
    description: "Editing mode: light, deep, or audit"
    required: false
---

Edit the document `$ARGUMENTS.file` using the FPR Editorial Agent.

Project: `$ARGUMENTS.project` (if not provided, detect from filename).
Mode: `$ARGUMENTS.mode` (if not provided, default to `light`).

Use the `editing-documents` skill to execute this task.
