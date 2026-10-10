# human-writing

A Claude skill for writing prose that doesn't read as machine-generated. It has three parts: a set of rules drawn from the detection research, a checker script that flags violations, and a reference file with the evidence.

I built it as an artist-researcher who writes proposals, statements, and academic papers. Generic AI prose flattens all three in the same way.

## What's inside

```
SKILL.md                 the rules and the workflow Claude follows
scripts/check_tells.py   scans a draft for tells and reports sentence rhythm
references/research.md   how detectors work, frequency data, sources
```

## Install

For Claude Code:

```bash
git clone https://github.com/ramykhair/human-writing.git ~/.claude/skills/human-writing
```

The skill triggers on its own when you ask Claude for an essay, statement, proposal, email, or post. You can also call it by name.

On Claude.ai, zip the folder and upload it under Settings > Capabilities > Skills.

Other chatbots don't read skills, but you can paste the body of `SKILL.md` into custom instructions or a system prompt.

## The checker on its own

```bash
python3 scripts/check_tells.py draft.md
```

It needs no dependencies, just Python 3.8 or later. It reports:

- **Hard violations:** banned vocabulary, em dashes, "not X but Y" contrasts, inflated verbs in place of "is", trailing "-ing" clauses that inflate significance, leftover chat phrases, and placeholders
- **Warnings:** repeated watch-list words, triads, bold, bullets, curly quotes, and emoji
- **Rhythm:** sentence-length spread, with a flag when sentences cluster around the same length (the "burstiness" signal detectors measure)

## Limits

No style guide guarantees passing every detector. Trained classifiers like Pangram, GPTZero, and Turnitin, and watermarks like SynthID-Text, measure word-probability patterns that style changes only partly move. These rules remove what readers and simpler tools catch.

What actually makes text read as human is the writer's own material: specific memories, opinions, numbers, names, and a final edit. Detectors also produce false positives, and they flag non-native English writers at much higher rates (Liang et al., 2023). Treat a detector score as evidence, not proof.

## Sources

The main sources are Wikipedia's "Signs of AI writing" field guide, Pangram's corpus frequency analysis, Kobak et al. on excess vocabulary in PubMed, DetectGPT, and Binoculars. The full list is in `references/research.md`.

## License

MIT
