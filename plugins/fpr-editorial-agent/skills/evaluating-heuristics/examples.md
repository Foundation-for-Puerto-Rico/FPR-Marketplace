# Evaluation Examples

These four examples demonstrate correct evaluator behavior. Study the reasoning before evaluating live paragraphs.

---

## Example 1: No changes needed — protected manifesto language used correctly

**Input paragraph:**
> The Wellness and Climate Resilience Plan (WCRP) represents a framework for transformation rooted in sustainability, resilience and shared prosperity. It functions as a living roadmap for communities across the region, one that treats human capital as a form of public infrastructure and places residents at the center of every decision.

**Expected output:**
```json
{"suggestions": []}
```

**Reasoning:** This paragraph uses three phrases from the protected manifesto lexicon: "framework for transformation," "living roadmap," and "rooted in sustainability, resilience and shared prosperity," and the protected human capital framing. None of these may be altered, simplified, or replaced — even though a general editor might feel tempted to shorten them or swap them for plainer synonyms. The paragraph architecture is sound (context/proposal beats present), the modality is appropriate, and there is no clarity problem for a public reader. Correct behavior is to return an empty suggestions array.

---

## Example 2: Certainty upgrade trap — cautious language must stay cautious

**Input paragraph:**
> The proposed mobility corridor may help reduce travel times between municipalities and aims to improve access to economic opportunities for low-income residents. If implemented as designed, it could generate an estimated 1,200 jobs during the construction phase.

**Expected output:**
```json
{"suggestions": []}
```

**Reasoning:** A careless evaluator might try to "strengthen" this paragraph by replacing "may help reduce" with "will reduce," "aims to improve" with "improves," or "could generate" with "will generate." That would be a certainty upgrade — a violation of NNQ-001, the highest-priority non-negotiable rule. The paragraph is intentionally cautious because the project is in a proposal stage. The modals _may_, _aims to_, and _could_ are not weaknesses to be fixed; they are accurate representations of the author's epistemic position. Correct behavior is to return an empty suggestions array. Do not touch modality.

---

## Example 3: Genuine clarity issue — wordy construction with minimum fix

**Input paragraph:**
> Due to the fact that the region has historically experienced significant underinvestment in transportation infrastructure, residents in rural municipalities have been confronted with the situation of having limited access to employment centers, healthcare facilities, and educational institutions, a circumstance that has contributed to the perpetuation of economic inequalities across generations.

**Expected output:**
```json
{
  "suggestions": [
    {
      "paragraph_index": 0,
      "original": "Due to the fact that",
      "replacement": "Because",
      "rule_id": "ECO-001",
      "confidence": 0.75,
      "rationale": "\"Due to the fact that\" is a wordy construction. \"Because\" is shorter and clearer with no loss of meaning or voice."
    },
    {
      "paragraph_index": 0,
      "original": "have been confronted with the situation of having limited access",
      "replacement": "have had limited access",
      "rule_id": "NNQ-002",
      "confidence": 0.75,
      "rationale": "\"Confronted with the situation of having\" is circumlocutory. \"Have had\" carries the same meaning with less friction for a public reader."
    }
  ]
}
```

**Reasoning:** This paragraph has two genuine clarity problems. "Due to the fact that" is a classic wordy construction with a direct one-word replacement ("because") from the preferred substitutions list. "Have been confronted with the situation of having" is a circumlocution that adds three words of friction without adding meaning. Both fixes stay as close as possible to the original (preserve-first), touch only the minimum necessary text, and do not alter the meaning, the modality, or the equity framing. The confidence of 0.75 is appropriate: these are clear improvements, not merely preferences. Notice that the rest of the paragraph — including the equity framing and the reference to historic underinvestment — is left untouched.

---

## Example 4: AI writing pattern — filler preamble and inflated importance phrase

**Input paragraph:**
> It is important to note that community engagement plays a pivotal role in the success of resilience planning initiatives. Residents bring local knowledge, lived experience, and social trust that no external consultant can replicate, and their participation from the earliest stages of planning ensures that solutions are grounded in actual community needs.

**Expected output:**
```json
{
  "suggestions": [
    {
      "paragraph_index": 0,
      "original": "It is important to note that community engagement plays a pivotal role in the success of resilience planning initiatives.",
      "replacement": "Community engagement is central to the success of resilience planning initiatives.",
      "rule_id": "AIH-EN-001",
      "confidence": 0.80,
      "rationale": "\"It is important to note that\" is an AI filler preamble (AIH-EN-001). \"Plays a pivotal role in\" is an AI inflated importance phrase (AIH-EN-021). Combined, the opening sentence carries two AI signals. Rewriting as a direct statement removes both patterns while preserving the full meaning and the asset-based framing."
    }
  ]
}
```

**Reasoning:** The paragraph opens with two confirmed AI patterns: the filler preamble "It is important to note that" (AIH-EN-001) and the inflated importance phrase "plays a pivotal role in" (AIH-EN-021). Because both patterns appear in the same sentence, it is cleaner to rewrite the full opening sentence as a single suggestion rather than propose two overlapping edits on the same text. The replacement is direct, preserves the equity framing and meaning, and removes the AI tell in one step. The second sentence is clean — no AI patterns, no clarity problems, strong asset-based framing — and is left untouched. Confidence of 0.80 is appropriate: this is a confirmed pattern rewrite, not a stylistic preference.
