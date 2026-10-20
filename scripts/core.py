#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Game Feel UI Core - BM25 search engine for Game Feel, Juiciness, Sensory UI,
Forgiveness Mechanics, Physics Curves, Procedural Audio, and Stack Guidelines.
Stdlib-only (zero external dependencies).
"""

import csv
import difflib
import re
from collections import defaultdict
from math import log
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
MAX_RESULTS = 3

CSV_CONFIG = {
    "mechanics": {
        "file": "mechanics.csv",
        "search_cols": [
            "Mechanic ID", "Mechanic Name", "Game Dev Origin", "Category",
            "Frequency Tier", "Keywords", "UI Equivalent", "Trigger", "When to Use"
        ],
        "output_cols": [
            "Mechanic ID", "Mechanic Name", "Game Dev Origin", "Category",
            "Frequency Tier", "Intensity", "UI Equivalent", "Trigger",
            "Timing / Physics Spec", "CSS / JS Snippet", "When to Use",
            "Anti-Patterns (Avoid)", "Reduced Motion Fallback", "Performance Notes"
        ],
    },
    "components": {
        "file": "components.csv",
        "search_cols": [
            "Component ID", "Component Name", "Frequency Tier", "Keywords",
            "Anticipation (Wind-up)", "Impact (Activation)", "Forgiveness (Invisible Feel)"
        ],
        "output_cols": [
            "Component ID", "Component Name", "Frequency Tier", "Keywords",
            "Anticipation (Wind-up)", "Impact (Activation)", "Follow-Through (Settle)",
            "Forgiveness (Invisible Feel)", "Audio & Haptic Pairing", "Code Recipe", "Avoid"
        ],
    },
    "audio": {
        "file": "audio-haptics.csv",
        "search_cols": [
            "Sound ID", "Sound Name", "Category", "Keywords", "Best For", "Waveform / Synthesis"
        ],
        "output_cols": [
            "Sound ID", "Sound Name", "Category", "Waveform / Synthesis",
            "Frequency Envelope", "Duration", "Max Gain", "Haptic Pattern (ms)",
            "Best For", "Web Audio JS Snippet", "Guardrails"
        ],
    },
    "physics": {
        "file": "physics-curves.csv",
        "search_cols": [
            "Curve ID", "Curve Name", "Motion Archetype", "Keywords", "Best For"
        ],
        "output_cols": [
            "Curve ID", "Curve Name", "Motion Archetype", "Recommended Duration",
            "CSS Easing / linear()", "Framer Motion Config", "GSAP Ease",
            "Best For", "Avoid"
        ],
    },
    "profiles": {
        "file": "app-profiles.csv",
        "search_cols": [
            "Profile ID", "Product Archetype", "Keywords", "Recommended Mechanics"
        ],
        "output_cols": [
            "Profile ID", "Product Archetype", "Recommended Juice Budget",
            "High-Freq Tier Strategy", "Medium-Freq Tier Strategy",
            "Hero Moment Strategy", "Recommended Mechanics",
            "Audio & Haptic Policy", "Avoid (Anti-Patterns)"
        ],
    },
    "anti-patterns": {
        "file": "anti-patterns.csv",
        "search_cols": [
            "Anti-Pattern ID", "Name", "Category", "Keywords",
            "Symptom (What Goes Wrong)", "The Game-Feel Fix"
        ],
        "output_cols": [
            "Anti-Pattern ID", "Name", "Category", "Severity",
            "Symptom (What Goes Wrong)", "Why Developers Do It",
            "The Game-Feel Fix", "Code Bad vs Good"
        ],
    },
}

UNTRUNCATED_COLS = {
    "CSS / JS Snippet", "Code Recipe", "Web Audio JS Snippet",
    "CSS Easing / linear()", "Framer Motion Config", "Code Bad vs Good",
    "Code Good", "Code Bad", "Recommended Mechanics",
}

STACK_CONFIG = {
    "react": {"file": "stacks/react.csv"},
    "nextjs": {"file": "stacks/nextjs.csv"},
    "framer-motion": {"file": "stacks/framer-motion.csv"},
    "html-tailwind": {"file": "stacks/html-tailwind.csv"},
    "css-waapi": {"file": "stacks/css-waapi.csv"},
    "gsap": {"file": "stacks/gsap.csv"},
    "shadcn": {"file": "stacks/shadcn.csv"},
    "vue": {"file": "stacks/vue.csv"},
    "svelte": {"file": "stacks/svelte.csv"},
    "react-native": {"file": "stacks/react-native.csv"},
    "flutter": {"file": "stacks/flutter.csv"},
}

STACK_COLS = {
    "search_cols": ["Category", "Guideline", "Description", "Do", "Don't", "Mechanic Ref"],
    "output_cols": [
        "Category", "Guideline", "Description", "Do", "Don't",
        "Code Good", "Code Bad", "Severity", "Mechanic Ref"
    ],
}

AVAILABLE_STACKS = list(STACK_CONFIG.keys())

_STOPWORDS = {
    "to", "in", "on", "at", "is", "of", "by", "or", "an", "if", "no", "so",
    "do", "be", "we", "it", "as", "the", "and", "for", "are", "was", "with",
}

_SYNONYMS = {
    "hit-stop": "hitstop",
    "freeze-frame": "freeze frame hitstop",
    "coyote-time": "coyote time",
    "input-buffer": "input buffer",
    "input-buffering": "input buffer",
    "squash-and-stretch": "squash stretch",
    "screen-shake": "shake trauma",
    "error-shake": "error shake trauma",
    "cmd+k": "cmdk command palette",
    "cmd-k": "cmdk command palette",
    "drag-and-drop": "drag drop kanban",
    "dnd": "drag drop kanban",
    "e-commerce": "ecommerce",
    "web-audio": "audio sound synth",
    "sound-effect": "audio sound",
    "sfx": "audio sound",
    "micro-interaction": "microinteraction",
    "micro-interactions": "microinteraction",
    "juiciness": "juice",
    "game-feel": "game feel",
    "a11y": "accessibility reduced-motion",
}

_SYNONYM_PATTERNS = [
    (re.compile(r"(?<!\w)" + re.escape(k) + r"(?!\w)", re.IGNORECASE), v)
    for k, v in sorted(_SYNONYMS.items(), key=lambda item: len(item[0]), reverse=True)
]


def _normalize(text: str) -> str:
    out = str(text)
    for pattern, repl in _SYNONYM_PATTERNS:
        out = pattern.sub(repl, out)
    return out


class BM25:
    """Pure-stdlib BM25 ranking engine."""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avgdl = 0.0
        self.idf = {}
        self.doc_freqs = defaultdict(int)
        self.N = 0
        self._term_freqs = []

    def tokenize(self, text: str) -> list:
        text = _normalize(str(text).lower())
        text = re.sub(r"[^\w\s]", " ", text)
        return [w for w in text.split() if len(w) >= 2 and w not in _STOPWORDS]

    def fit(self, documents: list):
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.N = len(self.corpus)
        if self.N == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.N or 1.0
        self._term_freqs = []
        for doc in self.corpus:
            tf = defaultdict(int)
            for word in doc:
                tf[word] += 1
            self._term_freqs.append(tf)
            for word in tf:
                self.doc_freqs[word] += 1
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.N - freq + 0.5) / (freq + 0.5) + 1)

    def score(self, query: str) -> list:
        q_tokens = self.tokenize(query)
        scores = []
        for idx in range(self.N):
            s = 0.0
            doc_len = self.doc_lengths[idx]
            tfs = self._term_freqs[idx]
            for token in q_tokens:
                if token in self.idf:
                    tf = tfs.get(token, 0)
                    idf = self.idf[token]
                    num = tf * (self.k1 + 1)
                    den = tf + self.k1 * (1 - self.b + self.b * doc_len / self.avgdl)
                    s += idf * (num / den)
            scores.append((idx, s))
        return sorted(scores, key=lambda x: x[1], reverse=True)

    def vocabulary(self) -> list:
        return list(self.idf.keys())


def _load_csv(filepath: Path) -> list:
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _suggest_terms(bm25: BM25, query: str, limit: int = 5) -> list:
    if bm25 is None:
        return []
    q_tokens = set(bm25.tokenize(query))
    if not q_tokens:
        return []
    candidates = []
    for term in bm25.vocabulary():
        if term in q_tokens:
            continue
        sim = max(difflib.SequenceMatcher(None, qt, term).ratio() for qt in q_tokens)
        if sim >= 0.72:
            candidates.append((-sim, term))
    return [term for _, term in sorted(candidates)[:limit]]


DOMAIN_KEYWORDS = {
    "audio": [
        "audio", "sound", "sfx", "synth", "oscillator", "pitch", "semitone",
        "chime", "thud", "buzz", "haptic", "vibrate", "frequency", "combo sound",
    ],
    "physics": [
        "cubic-bezier", "bezier", "easing", "curve", "stiffness", "damping",
        "linear()", "spring config", "duration", "velocity curve", "overshoot curve",
    ],
    "components": [
        "button", "modal", "dialog", "dropdown", "menu", "popover", "checkbox",
        "toggle", "switch", "kanban", "card", "toast", "cmdk", "command palette",
        "input", "form", "copy", "clipboard", "tab", "slider", "scrubber",
        "onboarding", "accordion", "dropzone", "pricing card", "like button",
    ],
    "anti-patterns": [
        "anti-pattern", "avoid", "mistake", "fatigue", "slot machine", "jank",
        "lag", "thrashing", "cls", "bad practice", "problem", "bug",
    ],
    "profiles": [
        "saas", "fintech", "banking", "ecommerce", "storefront", "dashboard",
        "analytics", "edtech", "gamified", "ai chat", "workspace", "creative tool",
        "portfolio", "landing page", "product type", "archetype", "budget",
    ],
    "mechanics": [
        "hitstop", "freeze frame", "anticipation", "squash", "stretch", "recoil",
        "kickback", "knockback", "trauma", "shake", "coyote time", "input buffer",
        "hitbox", "magnetic", "ripple", "shimmer", "sheen", "particle", "spark",
        "odometer", "tilt", "optimistic", "asymmetric", "flip", "stagger",
        "rubber band", "detent", "keycap", "strikethrough", "border beam",
    ],
}


def detect_domain(query: str):
    q_low = _normalize(query.lower())
    scores = {d: 0.0 for d in CSV_CONFIG}
    for domain, kws in DOMAIN_KEYWORDS.items():
        for kw in kws:
            if kw in q_low:
                scores[domain] += max(1, len(kw.split())) * 2.0
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best, best_score = ranked[0]
    runner_up = ranked[1][0] if len(ranked) > 1 and ranked[1][1] > 0 else None
    return (best if best_score > 0 else "mechanics"), runner_up


def search(query: str, domain: str = None, max_results: int = MAX_RESULTS) -> dict:
    auto_detected = domain is None
    runner_up = None
    if domain is None:
        domain, runner_up = detect_domain(query)

    if domain not in CSV_CONFIG:
        return {"error": f"Unknown domain '{domain}'. Valid: {', '.join(CSV_CONFIG)}"}

    cfg = CSV_CONFIG[domain]
    filepath = DATA_DIR / cfg["file"]
    rows = _load_csv(filepath)
    if not rows:
        return {"error": f"Dataset empty or missing: {filepath.name}", "domain": domain}

    docs = [" ".join(str(r.get(c, "")) for c in cfg["search_cols"]) for r in rows]
    bm25 = BM25()
    bm25.fit(docs)
    ranked = bm25.score(query)

    results = []
    for idx, sc in ranked[:max_results]:
        if sc <= 0:
            continue
        row = rows[idx]
        results.append({col: row.get(col, "") for col in cfg["output_cols"] if col in row})

    return {
        "domain": domain,
        "auto_detected": auto_detected,
        "runner_up_domain": runner_up,
        "query": query,
        "file": cfg["file"],
        "count": len(results),
        "results": results,
        "suggestions": _suggest_terms(bm25, query) if not results else [],
    }


def search_stack(query: str, stack: str, max_results: int = MAX_RESULTS) -> dict:
    if stack not in STACK_CONFIG:
        return {"error": f"Unknown stack '{stack}'. Valid: {', '.join(AVAILABLE_STACKS)}"}

    filepath = DATA_DIR / STACK_CONFIG[stack]["file"]
    rows = _load_csv(filepath)
    if not rows:
        return {"error": f"Stack file missing or empty: {filepath}", "stack": stack}

    docs = [" ".join(str(r.get(c, "")) for c in STACK_COLS["search_cols"]) for r in rows]
    bm25 = BM25()
    bm25.fit(docs)
    ranked = bm25.score(query)

    results = []
    for idx, sc in ranked[:max_results]:
        if sc <= 0:
            continue
        row = rows[idx]
        results.append({col: row.get(col, "") for col in STACK_COLS["output_cols"] if col in row})

    # If query is generic (e.g. stack name itself) and returned 0 BM25 hits, return top rows
    if not results and query.strip().lower() in {stack, "all", "guidelines", "juice", "game feel"}:
        for row in rows[:max_results]:
            results.append({col: row.get(col, "") for col in STACK_COLS["output_cols"] if col in row})

    return {
        "stack": stack,
        "query": query,
        "file": STACK_CONFIG[stack]["file"],
        "count": len(results),
        "results": results,
        "suggestions": _suggest_terms(bm25, query) if not results else [],
    }
