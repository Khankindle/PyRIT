# Cultural fit, refusal behavior, memorization, and agentic audits

PyRIT provides reusable orchestration, datasets, targets, and scorers for authorized
model evaluations. These dimensions are best treated as **audits**, not certificates.
A single score cannot establish that a model is culturally appropriate, censored, or
trained on a particular work.

## Cultural appropriateness and fit

Build a locally reviewed test set with contributors who understand the communities and
languages being represented. Record locale, language/script, scenario, intended meaning,
acceptable response range, and reviewer provenance. Include both culturally grounded
questions and matched controls (same task expressed across locales); do not reduce a
culture to a single norm or infer quality from a model's agreement with a stereotype.
Measure task success, factuality, respectful handling of uncertainty, harmful
stereotyping, and quality differences across locale/language slices. Report sample sizes,
uncertainty, and disagreement; let qualified human reviewers adjudicate ambiguous cases.
Never use an LLM judge as the sole ground truth. Rotate or blind presentation where
possible and separately evaluate language fluency so it does not mask cultural errors.

## Censorship and refusal behavior

“Censorship” is not a single observable property. Define the policy or expectation being
tested (provider safety refusal, jurisdiction-specific restriction, political topic
avoidance, or user-configured policy) before measuring. Use paired prompts covering
allowed and disallowed requests on the same topic, neutral phrasing controls, and
paraphrases. Record refusal, partial answer, factual completeness, and stated rationale;
compare rates by topic, language, and phrasing. Distinguish safe refusal from failure to
answer a legitimate request. Avoid treating a refusal alone as evidence of a policy or
political motive.

## User-supplied text / verbatim memorization screening

A user may supply a work they are authorized to test and generate bounded continuation
probes from selected excerpts. Compare model responses to the supplied reference using
contiguous token overlap (and, for practical full evaluations, a separately chosen
near-duplicate metric and human review). PyRIT's `pyrit.score.copyright_memorization`
module provides a simple longest-contiguous-token screen and a bounded one-shot probe
builder; it does not upload, retain, or parse book files. Applications should obtain
explicit consent, process locally where possible, enforce file and excerpt limits, avoid
sending complete books to third parties, and securely delete transient material.

A match is evidence that a model produced similar text under a particular prompt; it is
**not evidence of training inclusion or illegality**. No black-box output test can
reliably prove that a work was in the training corpus, establish authorization, or decide
copyright liability. Report prompt, model/version, date, sampled passages, output, metric,
and limitations. Seek legal review before drawing legal conclusions. Do not automate
iterative extraction, bypass refusals, or redistribute generated copyrighted passages.

## Petri-style behavioral auditing

For multi-turn risks such as sycophancy, deception, cooperation with misuse, or
self-preservation, prefer controlled scenario-based audits over isolated one-shot
prompts. The Petri project (Anthropic, open source) describes an auditor–target–judge
loop over natural-language seeds and interaction transcripts. Integrations should pin
and review the upstream implementation and license, isolate tools and credentials,
set turn/token/cost limits, log complete transcripts, and use human review of flagged
cases. Run multiple seeds and judge configurations; scores are comparative signals, not
absolute safety guarantees. PyRIT can run such tests through its existing scenario,
target, and scoring abstractions; this document does not vendor or claim to implement
Anthropic's Petri framework.

## Suggested reporting checklist

- Define construct, intended use, allowed policy, and threat model before testing.
- Record exact model/version, endpoint settings, prompts, sampling parameters, and date.
- Include matched controls, independent seeds, stratified results, and uncertainty.
- Separate automated screening from human adjudication; preserve dissent and ambiguity.
- Minimize sensitive uploads and retained transcripts; document consent and access.
- Re-run after model or policy changes. Never present audit scores as proof of legality.

## References

- Anthropic, [Petri: An open-source auditing tool to accelerate AI safety research](https://alignment.anthropic.com/2025/petri/) and its [source repository](https://github.com/safety-research/petri).
- Wang et al., [CDEval: A Benchmark for Measuring the Cultural Dimensions of LLMs](https://aclanthology.org/2024.c3nlp-1.1/), which combines generated items with human verification.
- Sukiennik et al., [An Evaluation of Cultural Value Alignment in LLM](https://arxiv.org/abs/2504.08863), evaluating culture across countries/languages and emphasizing grounded comparison.
- Carlini et al., [Extracting Training Data from Large Language Models](https://arxiv.org/abs/2012.07805), demonstrating that prompted outputs can reveal memorized examples; extraction is an empirical signal, not a legal conclusion.
