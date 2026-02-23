---
name: edit-wcrp
description: Edit a DOCX document using WCRP project style guide
arguments:
  - name: file
    description: Path to the DOCX file
    required: true
---

Edit the document `$ARGUMENTS.file` using the FPR Editorial Agent with project `WCRP` and mode `deep`.

Use the `editing-documents` skill to execute this task.
