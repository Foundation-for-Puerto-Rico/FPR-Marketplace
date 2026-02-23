---
name: edit-ersv
description: Edit a DOCX document using ERSV project style guide
arguments:
  - name: file
    description: Path to the DOCX file
    required: true
---

Edit the document `$ARGUMENTS.file` using the FPR Editorial Agent with project `ERSV` and mode `deep`.

Use the `editing-documents` skill to execute this task.
