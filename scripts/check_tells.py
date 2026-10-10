#!/usr/bin/env python3
"""Scan prose for AI-writing tells.

Usage:
    python3 check_tells.py draft.md
    cat draft.txt | python3 check_tells.py -

Exit code 1 if hard violations are found, 0 otherwise.
"""
import re
from collections import Counter
import statistics
import sys

BANNED = [
    "delve", "delves", "delving", "tapestry", "testament", "intricate", "intricacies",
    "meticulous", "meticulously", "pivotal", "underscore", "underscores", "underscoring",
    "vibrant", "realm", "boasts", "garner", "garnered", "bolster", "bolstered", "interplay",
    "showcase", "showcases", "showcasing", "foster", "fosters", "fostering", "leverage",
    "leveraging", "multifaceted", "nuanced", "robust", "seamless", "seamlessly", "holistic",
    "synergy", "paradigm", "embark", "embarked", "unlock", "unleash", "elevate", "empower",
    "resonate", "resonates", "align with", "aligns with", "crucial", "enduring", "indelible",
    "nestled", "in the heart of", "rich heritage", "renowned", "groundbreaking",
    "game-changer", "ever-evolving", "evolving landscape", "key turning point",
    "valuable insights", "plays a pivotal role", "serves as a reminder", "setting the stage",
    "it's important to note", "it is important to note", "it's worth noting",
    "it is worth noting", "notably", "furthermore", "moreover", "in conclusion",
    "in summary", "at its core", "in today's world", "in an era of",
]

WATCH = [
    "enhance", "highlight", "highlighting", "emphasize", "emphasizing", "ensure", "ensuring",
    "reflect", "reflecting", "quietly", "steady", "dependable", "practical", "clearer",
    "matters", "prioritize", "echoed", "challenge", "associated with", "landscape",
    "journey", "navigate",
]

COPULA_AVOIDANCE = [
    "serves as", "stands as", "functions as", "operates as", "acts as a testament",
]

CHAT_RESIDUE = [
    "certainly!", "great question", "i hope this helps", "let me know if",
    "feel free to", "would you like me to", "as an ai", "my last knowledge update",
]

TRAILING_ING = re.compile(
    r",\s+(highlighting|underscoring|reflecting|emphasizing|showcasing|contributing to|"
    r"symbolizing|demonstrating|illustrating|cementing|solidifying|ensuring|marking)\b",
    re.I,
)
CONTRAST = re.compile(
    r"\bnot (just|only|merely|simply)\b[^.?!]{0,80}\b(but|it's|it is)\b"
    r"|\bit'?s not\b[^.?!]{0,60}[,;]\s*it'?s\b"
    r"|\bisn't (just|only|merely)\b",
    re.I,
)
TRIAD = re.compile(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? and \w+", re.I)
PLACEHOLDER = re.compile(r"\[(insert|describe|your|add)[^\]]*\]|\d{4}-XX-XX", re.I)
DASHES = re.compile(r"[—–]| -- ")
BOLD = re.compile(r"\*\*[^*]+\*\*")
BULLET = re.compile(r"^\s*([-*•]|\d+\.)\s+", re.M)
CURLY = re.compile(r"[“”‘’]")
ODD_UNICODE = re.compile(r"[→←↔≈✅⚠✨🚀─━│]|[\U0001F300-\U0001FAFF]")
OPENERS = re.compile(r"^\s*(additionally|ultimately),", re.I | re.M)
CHAT_OPENER = re.compile(
    r"\A\s*(certainly|absolutely|sure|of course|great question)\b[!,.]?|\A\s*here's (a|an|the|your)\b",
    re.I,
)


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def find_terms(text, terms):
    hits = []
    for term in terms:
        for m in re.finditer(r"\b" + re.escape(term) + r"\b", text, re.I):
            hits.append((line_of(text, m.start()), m.group(0)))
    return sorted(hits)


def find_regex(text, pattern):
    return [(line_of(text, m.start()), m.group(0).strip()) for m in pattern.finditer(text)]


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def sentences(text):
    body = re.sub(r"^#+ .*$", "", text, flags=re.M)
    body = BULLET.sub("", body)
    parts = re.split(r"(?<=[.!?])\s+", body)
    return [p for p in (s.strip() for s in parts) if len(p.split()) >= 2]


def rhythm_report(text):
    lengths = [len(s.split()) for s in sentences(text)]
    if len(lengths) < 5:
        return None, []
    mean = statistics.mean(lengths)
    cv = statistics.pstdev(lengths) / mean if mean else 0
    flat_runs = []
    for i in range(len(lengths) - 2):
        window = lengths[i:i + 3]
        if max(window) - min(window) <= 3:
            flat_runs.append(i + 1)
    stats = {
        "sentences": len(lengths),
        "mean": round(mean, 1),
        "min": min(lengths),
        "max": max(lengths),
        "cv": round(cv, 2),
        "short (<=6)": sum(1 for n in lengths if n <= 6),
        "long (>=30)": sum(1 for n in lengths if n >= 30),
    }
    return stats, flat_runs


def report(label, hits, limit=12):
    if not hits:
        return
    print(f"  {label}: {len(hits)}")
    for ln, s in hits[:limit]:
        print(f"    line {ln}: {s}")
    if len(hits) > limit:
        print(f"    ... {len(hits) - limit} more")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    src = sys.argv[1]
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    text = strip_code(text)

    hard = {
        "Banned vocabulary": find_terms(text, BANNED),
        "Em/en dashes": find_regex(text, DASHES),
        "Not-X-but-Y contrasts": find_regex(text, CONTRAST),
        "Copula avoidance (use is/has)": find_terms(text, COPULA_AVOIDANCE),
        "Trailing significance clauses": find_regex(text, TRAILING_ING),
        "Chat residue": find_terms(text, CHAT_RESIDUE) + find_regex(text, CHAT_OPENER),
        "Placeholders": find_regex(text, PLACEHOLDER),
        "Additionally/Ultimately openers": find_regex(text, OPENERS),
    }
    soft = {
        "Watch-list words": find_terms(text, WATCH),
        "Possible triads": find_regex(text, TRIAD),
        "Bold in text": find_regex(text, BOLD),
        "Bullet/numbered lines": find_regex(text, BULLET),
        "Curly quotes": find_regex(text, CURLY),
        "Emoji/decorative Unicode": find_regex(text, ODD_UNICODE),
    }

    hard_count = sum(len(v) for v in hard.values())
    print(f"HARD VIOLATIONS: {hard_count}")
    for k, v in hard.items():
        report(k, v)

    print("\nWARNINGS (judgment calls):")
    for k, v in soft.items():
        if k == "Watch-list words":
            counts = Counter(s.lower() for _, s in v)
            repeated = [(0, f"{w} x{n}") for w, n in counts.items() if n > 1]
            if repeated:
                print(f"  Watch-list words used more than once: {len(repeated)}")
                for _, s in repeated:
                    print(f"    {s}")
        elif k == "Possible triads" and len(v) <= 1:
            continue
        else:
            report(k, v, limit=6)

    stats, flat = rhythm_report(text)
    print("\nRHYTHM:")
    if stats is None:
        print("  Too few sentences to measure.")
    else:
        print("  " + ", ".join(f"{k} {v}" for k, v in stats.items()))
        if stats["cv"] < 0.4:
            print("  Sentence lengths are too uniform (cv < 0.4). Mix very short and very long sentences.")
        if stats["short (<=6)"] == 0 or stats["long (>=30)"] == 0:
            print("  Missing extremes: include at least one sentence of 6 words or fewer and one of 30 or more.")
        if flat:
            print(f"  Runs of 3 similar-length sentences start at sentence(s): {flat[:10]}")

    sys.exit(1 if hard_count else 0)


if __name__ == "__main__":
    main()
