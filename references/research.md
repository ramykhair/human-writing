# Research behind the rules

Compiled October 2026. Read this when the user asks why a rule exists, or wants the evidence.

## How detectors work

| Method | What it measures | Notes |
|---|---|---|
| Perplexity | How predictable each next word is to a language model | AI text is low-perplexity because models sample likely tokens. Formal and non-native writing is also low-perplexity, which causes false positives. |
| Burstiness | Variation in sentence length and structure | Humans mix short and long sentences. Models cluster around 10–20 words. |
| DetectGPT (Mitchell et al., ICML 2023) | Probability curvature: whether small rewrites of a passage lower its log probability | AI text sits near a local maximum. AUROC rose from 0.81 to 0.95 on GPT-NeoX fake news. |
| Binoculars (ICML 2024) | Ratio of perplexity to cross-perplexity between a base model and an instruction-tuned model | Detects over 90% of ChatGPT samples at a 0.01% false-positive rate, with no training data. |
| Trained classifiers (Pangram, GPTZero, Turnitin) | Deep models trained on labeled human and AI corpora | Pangram states that visible tells are not inputs, and that the model combines "millions of signals". GPTZero adds a paraphrase-specific component. |
| Watermarks (SynthID-Text) | A keyed pseudorandom bias applied through tournament sampling at generation time | Needs the key to detect. Weak on short or low-entropy text. |

## Surface tells with data (Pangram, per 10,000 words, human vs AI)

| Tell | Human | AI | Multiple |
|---|---|---|---|
| Markdown in plain text | 8 | 90 | 12× (bold 43×, headers 23×) |
| AI phrases | 3 | 30 | 12× ("delve into" 45×) |
| Em dashes | 2 | 17 | 10× (OpenAI 9×, Anthropic 7×, Gemini 3 Pro 0.7×) |
| Bullet lists | 3 | 28 | 9× |
| Triads | 5 | 19 | 4× |
| "Not just X but Y" | 1 | 3 | 3× |
| Unusual Unicode | 28 | 71 | 3× (─ 940×, → 48×) |
| AI openers | 1 | 2 | 2× ("Certainly! Here's" 70×) |
| Emoji | 0.1 | 0.2 | 2× (✅ 167×, 🚀 26×) |

## Vocabulary by model era (Wikipedia: Signs of AI writing)

- **2023 to mid-2024 (GPT-4):** additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant
- **Mid-2024 to mid-2025 (GPT-4o):** align with, enhance, fostering, highlighting, showcasing
- **Mid-2025 to mid-2026 (GPT-5):** emphasizing, enhance, highlighting, showcasing, plus notability wording ("independent coverage", "active social media presence")
- **Mid-2026 onward:** challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally. Also more periods and commas, with sentences of 8–20 words.
- **Grok:** causal, empirical, correlate, underscore

Kobak et al. (Science Advances, 2025) found excess style vocabulary in 14 million PubMed abstracts. They estimate at least 10% of 2024 abstracts were LLM-processed, and up to 30% in some subcorpora.

## Things that are not reliable signs

Wikipedia lists these as ineffective:

- perfect grammar
- formal or "fancy" prose in general
- transition words on their own
- mixed registers
- Markdown from people who use it daily
- unsourced content

Humans judge AI text at near-chance rates.

## Detector failure modes

- **Bias against non-native writers:** Liang et al. (Patterns, 2023) found seven detectors flagged 61.3% of TOEFL essays as AI.
- **Edited text:** Accuracy drops on paraphrased or human-edited text for every major detector.
- **Short text:** Accuracy also drops on short passages.
- **Benchmark vs real world:** Vendor benchmarks (for example, GPTZero's 99.5%) differ from independent tests, one of which found 87% accuracy with a 10% false-positive rate.

## Sources

- https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- https://www.pangram.com/signs-of-ai-writing
- https://arxiv.org/pdf/2406.07016 (Kobak et al., excess vocabulary)
- https://arxiv.org/pdf/2412.11385 (Why does ChatGPT "delve" so much?)
- https://arxiv.org/abs/2301.11305 (DetectGPT)
- https://arxiv.org/html/2401.12070v3 (Binoculars)
- https://arxiv.org/pdf/2412.05139 (Practical examination of AI text detectors)
- https://arxiv.org/html/2603.03410 (SynthID-Text detection analysis)
- https://arxiv.org/pdf/2603.27006 (Markdown training and LLM prose)
- https://themarkup.org/machine-learning/2023/08/14/ai-detection-tools-falsely-accuse-international-students-of-cheating
- https://casrai.org/guides/how-ai-detection-actually-works
- https://tropes.fyi/directory
