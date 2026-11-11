"""Scoring logic for the Enneagram assessment."""

from .questions import (
    TYPE_ITEMS,
    INSTINCT_ITEMS,
    FUNCTIONING_ITEMS,
    WINGS,
    CENTERS,
    INTEGRATION_ARROW,
    DISINTEGRATION_ARROW,
)


def score_types(type_answers):
    """type_answers: dict mapping item index (0-based, within TYPE_ITEMS) -> 1-5."""
    raw = {t: 0 for t in range(1, 10)}
    counts = {t: 0 for t in range(1, 10)}
    for idx, (t, _text) in enumerate(TYPE_ITEMS):
        val = type_answers.get(idx)
        if val is not None:
            raw[t] += val
            counts[t] += 1

    normalized = {}
    for t in range(1, 10):
        max_possible = counts[t] * 5
        normalized[t] = round((raw[t] / max_possible) * 100, 1) if max_possible else 0.0

    ranked = sorted(normalized.items(), key=lambda kv: kv[1], reverse=True)
    primary = ranked[0][0]

    wing_candidates = WINGS[primary]
    wing = max(wing_candidates, key=lambda w: normalized[w])

    tritype = {}
    for center_name, members in CENTERS.items():
        best = max(members, key=lambda m: normalized[m])
        tritype[center_name] = best

    return {
        "raw": raw,
        "normalized": normalized,
        "ranked": ranked,
        "primary_type": primary,
        "wing": wing,
        "tritype": tritype,
        "integration": INTEGRATION_ARROW[primary],
        "disintegration": DISINTEGRATION_ARROW[primary],
    }


def score_instincts(instinct_answers):
    """instinct_answers: dict mapping item index (0-based, within INSTINCT_ITEMS) -> 1-5."""
    raw = {"sp": 0, "so": 0, "sx": 0}
    counts = {"sp": 0, "so": 0, "sx": 0}
    for idx, (inst, _text) in enumerate(INSTINCT_ITEMS):
        val = instinct_answers.get(idx)
        if val is not None:
            raw[inst] += val
            counts[inst] += 1

    normalized = {}
    for inst in raw:
        max_possible = counts[inst] * 5
        normalized[inst] = round((raw[inst] / max_possible) * 100, 1) if max_possible else 0.0

    stack = sorted(normalized.items(), key=lambda kv: kv[1], reverse=True)
    return {"raw": raw, "normalized": normalized, "stack": stack}


def score_functioning(functioning_answers):
    """functioning_answers: dict mapping item index (0-based, within FUNCTIONING_ITEMS) -> 1-5."""
    total = 0
    count = 0
    for idx, _text in enumerate(FUNCTIONING_ITEMS):
        val = functioning_answers.get(idx)
        if val is not None:
            total += val
            count += 1
    max_possible = count * 5
    score = round((total / max_possible) * 100, 1) if max_possible else 0.0
    return score


def band_for_score(score, bands):
    for low, high, label, desc in bands:
        if low <= score < high:
            return label, desc
    return bands[-1][2], bands[-1][3]
