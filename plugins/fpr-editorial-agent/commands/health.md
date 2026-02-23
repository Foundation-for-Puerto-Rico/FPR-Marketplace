---
name: health
description: Check FPR Editorial Agent prerequisites and folder access
arguments:
  - name: path
    description: Optional directory to check access for
    required: false
---

Run a health check for the FPR Editorial Agent. Verify:

1. **Python version:** Run `python3 --version` and confirm 3.9+
2. **Dependencies:** Run `python3 -c "import lxml, yaml, click, defusedxml; print('OK')"` from the plugin root
3. **Project files:** Check that `core/voice-playbook.yaml` and `projects/ERSV/term-bank.yaml` exist
4. **Folder access:** If `$ARGUMENTS.path` is provided, verify it is readable with `ls`

Report results clearly. If anything fails, provide the fix from the `troubleshooting.md` reference in the `editing-documents` skill.
