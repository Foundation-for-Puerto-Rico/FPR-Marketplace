"""
Knowledge base loader for the FPR Editorial Agent.

Loads pre-compiled YAML files from core/ and projects/{project_id}/
and provides query methods for the rule engine.
"""

from pathlib import Path
from typing import Optional

import yaml


class KnowledgeBase:
    """Loads and provides access to FPR editorial knowledge base YAMLs."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.repo_root = Path(__file__).parent.parent

        self._voice_playbook = self._load("core/voice-playbook.yaml")
        self._master_rules = self._load("core/master-editing-rules.yaml")
        self._economist = self._load("core/economist-principles.yaml")
        self._ai_humanizer = self._load("core/ai-humanizer.yaml")

        self._term_bank = self._load(f"projects/{project_id}/term-bank.yaml")
        self._protected_lexicon = self._load(f"projects/{project_id}/protected-lexicon.yaml")
        self._audience_profiles = self._load(f"projects/{project_id}/audience-profiles.yaml")

    def _load(self, relative_path: str) -> dict:
        path = self.repo_root / relative_path
        if not path.exists():
            raise FileNotFoundError(f"Knowledge base file not found: {path}")
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def get_term_bank_entries(self) -> list[dict]:
        """Return all term bank entries for the active project."""
        return self._term_bank.get("entries", [])

    def get_protected_terms(self) -> list[str]:
        """Return flat list of all protected terms from the project lexicon."""
        terms = []
        lexicon = self._protected_lexicon.get("terms", {})
        for category in lexicon.values():
            if isinstance(category, dict):
                entries = category.get("entries", [])
                for entry in entries:
                    if isinstance(entry, str):
                        terms.append(entry)
                    elif isinstance(entry, dict):
                        terms.append(entry.get("term", ""))
        # Also check top-level lists in lexicon
        for key, value in self._protected_lexicon.items():
            if key in ("meta", "terms"):
                continue
            if isinstance(value, list):
                for entry in value:
                    if isinstance(entry, str):
                        terms.append(entry)
                    elif isinstance(entry, dict):
                        terms.append(entry.get("term", ""))
        return [t for t in terms if t]

    def get_audience_profile(self, profile_id: Optional[str] = None) -> dict:
        """Return audience profile by ID, or the first/default profile."""
        profiles = self._audience_profiles.get("profiles", [])
        if not profiles:
            return {}
        if profile_id is None:
            return profiles[0]
        for profile in profiles:
            if profile.get("id") == profile_id:
                return profile
        return profiles[0]

    def get_confidence_thresholds(self) -> dict:
        """Return confidence thresholds for track changes vs comments."""
        return self._master_rules.get("confidence_thresholds", {
            "high_confidence_track_change": 0.60,
            "low_confidence_comment": 0.60,
            "ignore_below": 0.60,
        })

    def get_modes(self) -> dict:
        """Return editing mode configurations."""
        return self._master_rules.get("modes", {})

    def get_ai_humanizer_entries(self) -> list[dict]:
        """Return deterministic AI-humanizer entries."""
        return self._ai_humanizer.get("deterministic_entries", [])

    def get_ai_humanizer_heuristic_rules(self) -> list[dict]:
        """Return heuristic AI-humanizer rules."""
        return self._ai_humanizer.get("heuristic_rules", [])

    def build_heuristic_context(
        self,
        mode: str,
        audience_id: Optional[str],
        language: str,
    ) -> str:
        """Build a compact rules context string for heuristic prompts.

        Returns a structured text block summarizing the active rules
        relevant to the given mode, audience, and language.
        """
        audience = self.get_audience_profile(audience_id)
        thresholds = self.get_confidence_thresholds()

        # Non-negotiables from master rules
        non_negotiables = self._master_rules.get("non_negotiables", [])
        nn_lines = [f"  - [{r['id']}] {r['rule']}" for r in non_negotiables]

        # Safe edits and reject list
        safe = self._master_rules.get("safe_to_tighten", [])
        reject = self._master_rules.get("reject_always", [])

        # Voice playbook key rules
        modality = self._voice_playbook.get("modality", {})
        preserve_modals = modality.get("preserve_modals", [])
        forbidden = modality.get("forbidden_upgrades", [])
        stakeholder = self._voice_playbook.get("stakeholder_formula", {})
        equity_rules = self._voice_playbook.get("equity_rules", {})

        # Protected terms (first 20 to keep prompt compact)
        protected_terms = self.get_protected_terms()[:20]

        # Economist substitutions
        eco_subs = self._economist.get("clarity_principles", {}).get("preferred_substitutions", [])
        eco_lines = [f"  - {s['original']} → {s['preferred']}" for s in eco_subs[:8]]

        # Build AI humanization lines (filter by language)
        ai_h_rules = self.get_ai_humanizer_heuristic_rules()
        ai_h_lines = []
        for r in ai_h_rules:
            lang = r.get("language", "both")
            if lang == "both" or lang == language:
                ai_h_lines.append(f"  - [{r['id']}] {r['rule']}: {r['description']}")

        mode_config = self.get_modes().get(mode, {})
        mode_desc = mode_config.get("description", mode)

        context = f"""NON-NEGOTIABLES (NEVER VIOLATE):
{chr(10).join(nn_lines)}

MODALITY PRESERVATION:
  - Preserve these modals exactly: {', '.join(preserve_modals)}
  - NEVER upgrade to: {', '.join(forbidden)}

EQUITY FRAMING:
  - DO: {'; '.join(equity_rules.get('do', [])[:2])}
  - DON'T: {'; '.join(equity_rules.get('dont', [])[:2])}

STAKEHOLDER FORMULA:
  - When listing stakeholders, use: "{stakeholder.get('standard', '')}"

SAFE TO TIGHTEN:
{chr(10).join(f'  - {s}' for s in safe[:4])}

ALWAYS REJECT:
{chr(10).join(f'  - {r}' for r in reject[:3])}

ECONOMIST CLARITY SUBSTITUTIONS:
{chr(10).join(eco_lines)}

AI HUMANIZATION RULES (rewrite AI patterns into natural prose):
{chr(10).join(ai_h_lines)}

PROTECTED TERMS (untouchable — do NOT suggest changes to these):
  {', '.join(repr(t) for t in protected_terms)}

MODE: {mode} — {mode_desc}
AUDIENCE: {audience.get('name', 'default')} ({audience.get('tone', '')})
LANGUAGE: {language}
CONFIDENCE THRESHOLDS:
  - ≥{thresholds.get('high_confidence_track_change', 0.85)}: track change
  - {thresholds.get('low_confidence_comment', 0.60)}–{thresholds.get('high_confidence_track_change', 0.85)}: comment for human review
  - <{thresholds.get('ignore_below', 0.60)}: ignore"""

        return context
