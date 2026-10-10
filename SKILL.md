---
name: human-writing
description: Writing rules that strip the patterns AI detectors and human readers use to spot machine-written prose, plus a checker script that flags violations. Use this skill whenever writing or revising prose meant for people to read, such as essays, articles, artist statements, exhibition or grant proposals, abstracts, bios, emails, cover letters, social posts, or blog posts, even if the user doesn't mention AI detection. Also use it when the user asks to make text sound human, humanize a draft, remove AI tells, make writing "less like ChatGPT", or check whether a text reads as AI-generated. Do not use it for code, commit messages, or terminal answers.
---

# Human writing

Detectors and experienced readers catch AI text on two layers:

1. **Statistics.** These are low perplexity (word choices that are too predictable) and low burstiness (sentences of similar length). Trained classifiers learn subtler versions of the same signals.
2. **Surface tells.** These are favored vocabulary, stock sentence shapes, inflated significance, and chat-style formatting. Wikipedia editors, teachers, and editors spot these by eye.

The rules below target both. The surface rules remove what readers notice. The rhythm and specificity rules push the statistics toward human ranges. See `references/research.md` for the evidence behind each rule.

## Workflow

1. Before drafting, gather the specific material: names, numbers, dates, places, the author's own opinions and experiences. Ask the user for these if the piece depends on them. Specific detail does more than any other rule, and it can't be faked. That cuts both ways. Never invent facts about the user's own work, life, or results to make the prose concrete. That includes how a piece looks or behaves, what happened at an event, how people reacted, and numbers. If the user isn't available to ask, write the sentence with a visible `[confirm: ...]` marker and list every marker in your reply. A vivid invented detail is worse than a plain true one, because the author may sign it without noticing.
2. Draft with the rules below in mind.
3. Save the draft to a file and run the checker:
   ```bash
   python3 <skill-dir>/scripts/check_tells.py draft.md
   ```
   It reports banned words, em dashes, contrast constructions, triads, copula avoidance, chat residue, formatting tells, and sentence-length variation. Exit code 1 means hard violations remain.
4. Fix every hard violation. Treat warnings as judgment calls. Re-run until clean.
5. Do the read-aloud pass in "Final pass" below. The script can't judge specificity or voice.

## 1. Vocabulary

These words appear at many times their human rates in post-2023 text. One of them is coincidence. Several together are a strong signal. Rewrite the sentence instead of swapping in a synonym, because a synonym keeps the same inflated shape.

**Banned:** delve, tapestry, testament, intricate, intricacies, meticulous(ly), pivotal, underscore(s), vibrant, landscape (figurative), realm, boasts, garner, bolster(ed), interplay, showcase/showcasing, foster(ing), leverage, multifaceted, nuanced, robust, seamless, holistic, synergy, paradigm, embark, journey (figurative), navigate (figurative), unlock, unleash, elevate, empower, resonate, align with, crucial, enduring, indelible, nestled, in the heart of, rich heritage, renowned, groundbreaking, game-changer, ever-evolving, evolving landscape, key turning point, valuable insights, a testament to, plays a pivotal role, serves as a reminder, setting the stage for, it's important to note, it's worth noting, notably, furthermore, moreover, in conclusion, in summary, at its core, in today's world, in an era of. Also "Additionally" and "Ultimately" as sentence openers.

**Watch list** (fine once per piece, suspicious in clusters): enhance, highlight, emphasize, ensure, reflect, quietly, steady, dependable, practical, clearer, matters, prioritize, echoed, challenge, associated with. The 2026 models lean on these plainer words, so the tell is frequency rather than the word itself.

## 2. Sentence shapes

- **Drop "not X, but Y" and its relatives**: "it's not just X, it's Y", "not only... but also", "no X, no Y, just Z", "no longer X; it is Y", "less about X than Y", and "X rather than Y" used as a reveal. This is the most-cited AI tell, at about 3× human rates. Models reach for these because they create a fake sense of insight by knocking down a position nobody held. State the claim directly.
- **No epigram endings.** Don't close a paragraph or the piece with a short aphorism, such as "The text is never fixed. It exists only in relation to a body." or "Here the letter answers to the body that approaches it." This is the 2026 version of "delve": tidy, quotable, abstract, and present in almost every model's output. End a paragraph on a fact, an example, or the next step in the argument.
- **Break the triad habit.** Models group things in threes at about 4× human rates. Use one, two, or four. Keep a genuine triad only if it's the only one in the piece.
- **Use "is" and "has".** "Serves as", "stands as", "functions as", "represents", "boasts", "features", and "offers" replace plain copulas in AI prose. Humans write "is".
- **Cut trailing significance clauses**, such as ", highlighting its importance", ", reflecting broader trends", or ", contributing to the growth of...". They add a shallow interpretation to the end of a fact. Delete them, or turn them into a sentence with real content.
- **Name relationships exactly.** "Associated with" and "in connection with" are vague. Say who did what.
- **Vary sentence length hard.** Put a five-word sentence next to a thirty-five-word one. Current models write in a narrow band of about 8–20 words, and that uniformity is what burstiness measures.
- **Vary paragraph length.** A one-line paragraph is fine.
- **Use the whole punctuation set,** including semicolons, parentheses, colons, and questions. Models underuse semicolons and parentheses. Contractions are normal.

## 3. Content

- **No inflated significance.** A building isn't "a testament" to anything. Say what it is and what happened there.
- **No brochure tone.** Words like "nestled", "vibrant" and "renowned" read like a press release.
- **No vague attribution,** such as "experts argue", "critics note" or "studies show". Name the person and the work, or drop the claim.
- **No formulaic arc** that ends in "Despite these challenges..." and an upbeat outlook.
- **No closing summary.** End on the last real point.
- **No hedging disclaimers,** such as "While details are limited" or "may vary".
- **Commit to positions.** Human writers take sides, admit doubt in specific places, and digress when it earns its place. AI balances every claim.
- **Prefer plain verbs:** "wrote" not "authored", "used" not "utilized", "started" not "embarked on".

## 4. Formatting (prose only)

These rules apply to essays, statements, emails, and posts. Technical documentation can keep headings and lists.

- **Em dashes:** AI uses them at about 10× human rates. Use a comma, colon, parentheses, or a new sentence instead.
- **Bold:** Don't bold words inside prose. AI bolds at about 43× human rates.
- **Lists:** No bullet lists where sentences would work, and no "**Label:** text" list items.
- **Headings:** Use them only if the document type calls for them, and write them in sentence case.
- **Characters:** No emoji, no decorative Unicode (→ ≈ ✅ ⚠), and straight quotes only.
- **Markdown:** None in plain-text destinations such as email, forms, or social posts.

## 5. Chat residue

- **Openers:** None, such as "Certainly!", "Great question", or "Here's a...".
- **Closers:** None, such as "I hope this helps", "Let me know if...", or "Feel free to...".
- **Placeholders:** None, such as [Insert X] or 2025-XX-XX.
- **Self-reference:** No mention of being an AI or of a knowledge cutoff.

## 6. Citations

Never invent a source, quote, DOI, ISBN, page number, or URL. Fabricated references are the strongest evidence of AI use that exists, stronger than any style tell. If a source can't be verified, say so or leave the claim out.

## Final pass

The script catches patterns. This pass catches what it can't.

1. **Opening:** Does the first sentence say something, or does it set the stage? Cut stage-setting.
2. **Detail:** Find each abstract claim. Can a concrete detail replace it? Replace it.
3. **Ending:** Does the last paragraph only restate the piece? Delete it. Does any paragraph end on a neat aphorism? Replace it with something concrete.
4. **Invented facts:** Is every claim about the user's own work traceable to something they said? If not, add a `[confirm]` marker.
5. **Voice:** Could this paragraph appear in anyone's essay? If so, add the author's actual view, experience, or material.
6. **Rhythm:** Read it aloud. A run of sentences with the same rhythm needs breaking.

## Honest limits

Tell the user plainly, when it's relevant, that no style guide guarantees passing every detector. These rules remove the tells that readers and simple tools use, and they widen sentence-level variation. Trained classifiers (Pangram, GPTZero, Turnitin) and watermark detectors (SynthID-Text) measure word-probability patterns that style rules only partly change. The most reliable path is human material and a human edit pass. Don't promise detector results, and don't use tricks like inserted typos or homoglyph characters. They degrade the writing, and they are a form of deception rather than good writing.
