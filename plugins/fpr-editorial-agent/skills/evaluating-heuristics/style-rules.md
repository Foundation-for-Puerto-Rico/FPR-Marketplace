# FPR Style Rules Reference

This file is loaded by the `evaluating-heuristics` skill as a reference for paragraph evaluation. Apply these rules when assessing each paragraph and deciding whether to propose a suggestion.

---

## Non-Negotiable Rules

These five rules override everything else. Violating any of them is a disqualifying error.

**NNQ-001: No certainty upgrades.**
Never increase the degree of certainty in a claim. Preserve the author's original modals exactly: _can_, _may_, _might_, _aims to_, _seeks to_, _helps_, _is intended to_. Do not convert cautious language into guaranteed outcomes. "May help" must stay "may help." "Aims to" must stay "aims to." Never write _will ensure_, _guarantees_, or _will achieve_ where the source used a weaker modal.

**NNQ-002: Preserve-first line editing.**
Default to minimal edits that stay as close to the original phrasing as possible. Recompose only when there is a significant problem: meaning ambiguity, grammatical error, major reader friction, terminology inconsistency, or density that breaks clarity. Use the escalation ladder — fix punctuation and connector words first; fix parallel structure second; split the sentence third; recompose (keeping 70-80% of original wording) as a last resort. One-word problem means one-word fix.

**NNQ-003: Protect FPR voice.**
If a change makes text shorter or cleaner but flattens the FPR institutional voice, reject the change. Do not swap signature institutional language for generic corporate synonyms. Do not delete the values layer (stewardship, shared prosperity, community benefit). A shorter sentence that sounds like any government document is worse than the original.

**NNQ-004: Equity and asset-based framing.**
Write from an asset-based perspective. Attribute disparities to structural conditions, historic investment patterns, and unequal access — never to the communities themselves. Use people-centered terms: residents, communities, families, youth, workforce. Never use stigmatizing labels.

**NNQ-005: Systems and governance integrity.**
Maintain strong systems framing: regional coordination, multisector collaboration, durable platforms — not one-off programs. Do not remove governance language or weaken the institutional nature of a model simply to shorten the text.

---

## FPR Voice

### Voice Attributes
FPR documents are: authoritative but accessible, visionary but anchored in evidence, asset-based and not deficit-based, multisector and systems-oriented, propositive, and built for long-term transformation. Edits that move text away from any of these attributes are incorrect.

### Paragraph Architecture
Well-formed FPR paragraphs follow a recognizable arc of beats. Preserve all beats, especially the _assets/opportunities_ beat and the _proposal/model_ beat. The canonical arc is:

1. Context or diagnosis
2. Challenges, gaps, or fragmentation
3. Assets and opportunities
4. Proposal or model
5. Expected results or transformation

Do not delete the _assets/opportunities_ beat or the _proposal/model_ beat simply to shorten the text.

### Point of View
Default is third-person institutional. Use "we" only when it clearly strengthens an institutional stance. Use present tense for current conditions. Use present-intent or future forms for proposals: _will_, _is envisioned_, _will enable_.

### Protected Manifesto Phrases
The following phrases appear throughout FPR documents as part of deliberate institutional language. They must never be altered or replaced:

- "framework for transformation"
- "living roadmap"
- "thriving future"
- "rooted in sustainability, resilience and shared prosperity"
- "shared stewardship"
- "inclusive community engagement"
- "collective responsibility"
- "asset-based development"
- "sustainable destination management"
- "permanent, independent, multisectoral, decision-making body"
- "coordinated independent regional governance system"
- "enduring institutional anchor" / "institutional backbone"
- "braided funding"
- "visitor economy becomes a strategic lever"
- "tourism enhances — not burdens — local communities"
- "treat human capital as a form of public infrastructure"
- "integrated, technologically advanced, multimodal"
- "Mobility as a Service (MaaS)… digital backbone"

### Stakeholder Formula
When stakeholder groups are listed, use this exact formula:
_municipal governments, nonprofit organizations, public agencies, private sector actors, community stakeholders, and residents_

### Terminology: Attractions vs. Attractors
Both words are in use and must be preserved. "Attractions" refers to concrete assets and places people visit. "Attractors" emphasizes the drawing power and strategic function of cultural, natural, or creative elements. Define "attractors" on first use with a plain-language appositive, then use consistently.

### What Is Safe to Edit
- Remove true redundancy (same idea repeated without adding new function)
- Replace unclear pronouns with explicit nouns
- Reduce hedge-stacking when three or more hedges co-occur in a single sentence
- Break very long sentences only if the rhythm and the vision-evidence-action arc are preserved
- Convert dense run-on lists to structured bullets when it improves public readability

### What Must Never Be Edited
- Signature institutional phrases replaced with generic corporate synonyms
- Values language deleted (stewardship, shared prosperity, community benefit)
- Bridge logic that carries the paragraph architecture removed
- Systems language oversimplified into linear program talk
- Modality upgraded (weaker modal replaced with stronger one)

---

## Clarity Principles

Derived from Orwell's rules as applied in the Economist style tradition. Apply these when evaluating wordiness, passivity, and jargon.

**ECO-001:** Do not use clichéd metaphors or figures of speech. Write plainly.

**ECO-002:** Prefer the shorter word when it conveys the same meaning without loss of precision.

**ECO-003:** Cut any word that can be cut without changing the meaning.

**ECO-004:** Prefer active voice over passive voice when active voice is natural and does not shift the emphasis wrongly.

**ECO-005:** Prefer an everyday equivalent when jargon can be replaced without loss of precision.

**ECO-006:** Break any rule before producing writing that is outright awkward or unclear.

### Common Substitutions (apply in English)
| Wordy form | Preferred form |
|---|---|
| in order to | to |
| due to the fact that | because |
| at this point in time | now |
| in the event that | if |
| permit | let |
| demonstrate | show |
| utilise | use |
| commence | begin |
| endeavour | try |
| purchase | buy |
| persons | people |

### Sentence and Paragraph Clarity
- A paragraph is a unit of thought, not a unit of length. A paragraph that mixes multiple ideas is a clarity problem.
- Avoid parenthetical interruptions that break the flow of a sentence when the idea can be placed at the start or end instead.
- Maximum one semicolon per sentence in narrative sections. Semicolon chains are a clarity problem.
- Reduce accidental repetition by rotating phrasing, without flattening voice or changing meaning.
- Abbreviations: write the full form on first use unless the abbreviation is universally known. Prefer a descriptive reference (_the agency_, _the programme_) on subsequent mentions rather than repeating the acronym.
- Puerto Rico place names must carry correct Spanish accents: Bayamón, Loíza, Río Grande, etc.

---

## AI Writing Patterns

FPR documents are often drafted with AI assistance. The heuristic pass identifies AI writing patterns and proposes corrections. Both Spanish and English patterns are in scope.

### Deterministic Patterns (already removed automatically — do not re-flag)
The following patterns are handled in the deterministic pass before heuristic evaluation. If you see them remaining in the paragraph text, do flag them; otherwise do not duplicate the deterministic work.

**English filler preambles (delete entirely):**
- "It is important to note that"
- "It is worth noting that"
- "It bears mentioning that"
- "It should be highlighted that"
- "It goes without saying that"
- "While there are many factors to consider,"
- "In the ever-evolving landscape of"

**English formulaic transitions (delete entirely):**
- "Furthermore," / "Moreover," / "Additionally,"
- "In conclusion," / "Moving forward,"
- "In light of this," / "With that in mind,"
- "As previously noted,"

**English inflated importance (replace with plain equivalent):**
- "plays a pivotal/crucial/vital role in" → "contributes to"

**Spanish filler preambles (delete entirely):**
- "Es importante destacar que" / "Es importante señalar que"
- "Cabe mencionar que" / "Cabe destacar que"
- "En este sentido," / "En definitiva," / "En resumen,"
- "Dicho de otro modo," / "Para finalizar,"

**Spanish connectors to simplify:**
- "Asimismo," → "También,"
- "Por ende," → "Por eso,"
- "Si bien es cierto que" → "Aunque"
- "Resulta fundamental" → "Es clave"

**Spanish calques from English (correct):**
- "hacer sentido" → "tener sentido"
- "juega un rol vital/crucial" → "cumple una función esencial/clave"
- "en orden de" → "para"

### Heuristic Patterns (evaluate and flag if present)

**AIH-H-001: Em dash overuse.**
Flag em dashes that serve routine purposes (clarifier, simple appositive, sentence join). Replace with the punctuation that best serves the context: comma, period, colon, or parentheses. Keep em dashes only when they add clear rhetorical value — a pivot or contrast that should pop, an intentional cadence break, or compressed emphasis. Confidence range: 0.75–0.90.

**AIH-H-002: Uniform sentence length (low burstiness).**
If all sentences in a paragraph cluster between 15 and 22 words with very low variation, flag for sentence length variation. Break one long sentence into two, or merge two short ones. Aim for a mix of short (5–10 words), medium (12–20), and long (22–35). Confidence range: 0.65–0.80.

**AIH-H-003: AI signal word clustering (English).**
Flag paragraphs containing three or more of these words: _delve, robust, comprehensive, pivotal, transformative, nuanced, multifaceted, leverage, foster, streamline, harness, holistic, unprecedented, seamless, paramount, cornerstone, catalyst, synergy, tapestry, landscape (figurative), bolster, elevate, spearhead, navigate (figurative), cutting-edge, groundbreaking_. Replace each with the simplest accurate word. Confidence range: 0.70–0.85.

**AIH-H-004: Español neutro (Spanish).**
Flag overly formal or generic Spanish that sounds like it was translated by a bot rather than written by a competent Puerto Rican institutional professional. Replace bureaucratic constructions with direct, accessible language. "Se caracteriza por" should become an active verb. Do not introduce slang — keep institutional register but make it natural. Confidence range: 0.65–0.80.

**AIH-H-005: Gerundio abusivo (Spanish).**
Flag gerunds not expressing simultaneity. "Analizando los datos, se concluye" → "Al analizar los datos, se concluye". Gerunds used as English present-participle calques are an AI tell. Gerunds expressing simultaneity ("Caminando por la calle, vio el letrero") are correct and should not be flagged. Confidence range: 0.75–0.85.

**AIH-H-006: Negative parallelism (English).**
Flag "It's not just X — it's Y" and "It's not merely X — it's Y" constructions. Rewrite as direct statements. Confidence range: 0.80–0.90.

**AIH-H-007: Promotional tone.**
Flag travel-brochure and marketing language in institutional reports: _breathtaking, rich cultural tapestry, unprecedented opportunity, groundbreaking initiative, must-visit, stunning natural beauty, vibrant community_. Replace with specific, evidence-based descriptions. This tone undermines credibility in PRDOH plans. Confidence range: 0.75–0.85.

**AIH-H-008: Hedge stacking (English).**
Flag sentences with three or more hedging devices co-occurring: _may, might, could, potentially, possibly, perhaps, arguably, somewhat, to some extent_. Reduce to at most one hedge per sentence. Note: this is different from NNQ-001 — do not remove a single intentional hedge; only reduce when they stack excessively. Confidence range: 0.70–0.80.

**AIH-H-009: Vague attribution.**
Flag claims attributed to unnamed sources: "Industry reports suggest...", "Experts believe...", "Studies have shown...", "Observers have cited...". Either specify the source or rewrite as a direct statement without the false authority appeal. Confidence range: 0.70–0.80.

**AIH-H-010: Passive voice clusters (Spanish).**
Flag paragraphs in Spanish with four or more _se + verb_ impersonal constructions. Rewrite with active subjects. Some _se_ constructions are natural in Spanish; only flag when they cluster and obscure who does what. Confidence range: 0.65–0.75.

---

## Confidence Calibration

Use these bands to assign confidence to every suggestion. Do not include a suggestion below 0.60 — it will be ignored by the pipeline.

| Confidence | When to use |
|---|---|
| 0.90–1.0 | Clear grammar error, obvious typo, unambiguous terminology fix with no voice risk |
| 0.75–0.89 | Clarity improvement, sentence structure fix, confirmed AI pattern rewrite |
| 0.60–0.74 | Subjective improvement, minor style preference, genuine but arguable cleanup |
| Below 0.60 | Do not include — the pipeline discards it |

When in doubt between two bands, choose the lower one. Overconfident suggestions that alter voice or meaning are worse than no suggestion at all.

---

## Protected Terms

Each project maintains a protected lexicon in `projects/{PROJECT}/protected-lexicon.yaml`. These terms are project-specific and must never be modified, replaced, or deleted — not even for clarity, grammar, or simplification.

Before proposing any change to a term, phrase, or acronym, consider whether it may appear in the protected lexicon. If the paragraph uses an acronym or brand name specific to the project (WCRP, ERSV, PRITA, etc.), assume it is protected unless you have explicit evidence otherwise.

The core manifesto phrases listed in the FPR Voice section above are also protected at the global level and apply to all projects.
