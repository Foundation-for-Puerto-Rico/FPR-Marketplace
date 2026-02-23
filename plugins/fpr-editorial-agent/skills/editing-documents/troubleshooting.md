# Troubleshooting

## Python not found

**Symptom:** `python: command not found` or `python3: command not found`

**Fix:** Install Python 3.9+ from python.org or via Homebrew:
```
brew install python@3.12
```

## Missing dependencies

**Symptom:** `ModuleNotFoundError: No module named 'lxml'`

**Fix:** Install from the plugin's requirements.txt:
```
pip install -r requirements.txt
```

The plugin needs: `lxml>=4.9.0`, `pyyaml>=6.0`, `click>=8.1.0`, `defusedxml>=0.7.0`

## File not found

**Symptom:** `Error: Invalid value for 'DOCUMENT': Path '...' does not exist.`

**Fix:** Check the file path. Use absolute paths if relative paths fail. Verify the file exists with `ls`.

## Permission denied

**Symptom:** `PermissionError: [Errno 13] Permission denied`

**Fix:** Check file permissions. On macOS, ensure the working directory is accessible. Try copying the file to a local directory first.

## XML validation failed

**Symptom:** `WARNING: Output XML validation failed`

**Fix:** This is non-fatal — the document was still saved. If the output opens correctly in Word, the warning can be ignored. If corrupt, re-run with `--no-validate` and report the issue.

## No suggestions found

**Symptom:** `No suggestions to apply. Document is unchanged.`

**Explanation:** The document already conforms to the style guide for the given project and mode. In `light` mode this means no term bank matches were found. Try `deep` mode for heuristic evaluation.
