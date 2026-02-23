---
name: health
description: Check FPR Editorial Agent prerequisites and folder access
arguments:
  - name: path
    description: Optional directory to check access for
    required: false
---

Run a health check for the FPR Editorial Agent. Find the plugin root (the directory containing `src/fpr_edit.py` — two levels up from the `skills/editing-documents/` folder).

1. **Python version:** Run `python3 --version` and confirm 3.9+
2. **Auto-setup:** If `.venv` does not exist in the plugin root, create it and install dependencies:
   ```bash
   python3 -m venv "$PLUGIN_ROOT/.venv"
   "$PLUGIN_ROOT/.venv/bin/pip" install -r "$PLUGIN_ROOT/requirements.txt"
   ```
3. **Dependencies:** Run `"$PLUGIN_ROOT/.venv/bin/python" -c "import lxml, yaml, click, defusedxml; print('OK')"`
4. **Knowledge base:** Check that `core/voice-playbook.yaml` and `projects/ERSV/term-bank.yaml` exist in the plugin root
5. **Folder access:** If `$ARGUMENTS.path` is provided, verify it is readable with `ls`

Report results clearly. If anything fails, provide the fix from the `troubleshooting.md` reference in the `editing-documents` skill.
