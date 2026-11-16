"""
Groq-powered personalization for the practitioner Intervention & Session
Planning Report (Report 2). Groq is used ONLY to turn this client's actual
assessment results into practitioner-facing discussion material; the model
never re-scores or re-types the client, and every output section is explicitly
framed as a hypothesis for the practitioner to explore, not a diagnosis.

Free API key: https://console.groq.com/keys (sign up, "Create API Key").
"""

import json
import urllib.request
import urllib.error

from .questions import (
    TYPE_NAMES, INTEGRATION_ARROW, DISINTEGRATION_ARROW, INSTINCT_NAMES,
    harmonic_triad_for, hornevian_group_for,
)
from .content import TYPE_PROFILES, LEVEL_BANDS
from .scoring import band_for_score

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """You are assisting a licensed psychotherapist by translating a client's Enneagram \
self-assessment results into practitioner-facing session material. You write ONLY for the \
practitioner's own confidential use - never content to hand directly to the client unedited.

Hard rules:
- Never state the client's type, pattern, or any derived trait as a confirmed fact. Use hedged \
language ("may", "often", "consider exploring whether...").
- Clearly separate what the assessment data actually supports from what is a hypothesis requiring \
further exploration in session.
- Do not present any Enneagram type as inherently good or bad.
- Session questions must be open-ended and must not lead the client toward confirming the \
Enneagram result - they should invite genuine reflection.
- Scenario choices are NOT a personality test. Never imply a selected choice would prove or diagnose \
anything. Frame scenarios purely as discussion-starters.
- Only select interventions that plausibly fit this specific profile - do not list every possible \
intervention.
- Ground every section in the specific type, wing, tritype, instinct stack, and functioning data \
given to you. Avoid generic Enneagram-textbook filler that could apply to any client.
- Output ONLY valid JSON matching the exact schema given in the user message. No markdown fences, \
no commentary outside the JSON object.
"""

JSON_SCHEMA_INSTRUCTIONS = """
Return a single JSON object with exactly this shape:

{
  "psychological_formulation": {
    "core_motivations": "string",
    "underlying_fears": "string",
    "cognitive_emotional_patterns": "string",
    "defensive_tendencies": "string",
    "interpersonal_patterns": "string",
    "flexibility_and_rigidity": "string",
    "evidence_vs_hypothesis": "string - one paragraph distinguishing what the assessment data itself supports from what remains an open hypothesis for session exploration"
  },
  "strengths_and_resources": ["string", "... 5-7 items"],
  "development_areas": ["string", "... 3-5 prioritized items, most relevant first"],
  "session_questions": {
    "Self-awareness and identity": ["string", "..."],
    "Core motivations and fears": ["string", "..."],
    "Emotional regulation": ["string", "..."],
    "Relationships and interpersonal patterns": ["string", "..."],
    "Decision-making": ["string", "..."],
    "Coping with stress": ["string", "..."],
    "Personal needs and boundaries": ["string", "..."],
    "Growth and development": ["string", "..."]
  },
  "discussion_topics": [
    {"topic": "string", "why_relevant": "string", "explore": "string"}
  ],
  "scenarios": [
    {
      "title": "string - short scenario name",
      "situation": "string - 2-3 sentence realistic situation tailored to this profile",
      "choices": [
        {"label": "A", "text": "string", "pattern": "string", "motivation": "string", "consequences": "string", "alternative": "string"},
        {"label": "B", "text": "string", "pattern": "string", "motivation": "string", "consequences": "string", "alternative": "string"}
      ]
    }
  ],
  "interventions": [
    {
      "modality": "string e.g. CBT / ACT / Emotional regulation / Boundary-setting / Values clarification",
      "target_pattern": "string",
      "objective": "string",
      "explanation": "string",
      "implementation": "string",
      "homework": "string",
      "requires_clinical_judgment": "boolean - true if this goes beyond a general self-development exercise and needs the practitioner's clinical judgment/further assessment, false if it is a general self-development exercise"
    }
  ],
  "session_roadmap": [
    {"phase": "Initial exploration", "description": "string"},
    {"phase": "Further exploration", "description": "string"},
    {"phase": "Skill development", "description": "string"},
    {"phase": "Application", "description": "string"},
    {"phase": "Review", "description": "string"}
  ]
}

Provide 2-3 session_questions per theme (every theme key must be present), 2-3 discussion_topics,
exactly 2 scenarios with 2-3 choices each, and 3-5 interventions (not more - select only what fits).
"""


def _build_profile_context(client_name, type_result, instinct_result, functioning_score,
                            type_answers, instinct_answers):
    primary = type_result["primary_type"]
    wing = type_result["wing"]
    prof = TYPE_PROFILES[primary]
    band_label, _ = band_for_score(functioning_score, LEVEL_BANDS)
    stack = instinct_result["stack"]
    stack_notation = "/".join(code.upper() for code, _ in stack)

    tritype_lines = []
    for center, type_num in type_result["tritype"].items():
        tritype_lines.append(f"{center}: Type {type_num} ({TYPE_NAMES[type_num]})")

    lines = [
        f"Client identifier: {client_name or 'Confidential Client'}",
        f"Primary type: {primary} - {prof['name']}",
        f"Core fear: {prof['core_fear']}",
        f"Core desire: {prof['core_desire']}",
        f"Wing: {wing} - {TYPE_NAMES[wing]}",
        f"Integration (growth) direction: {INTEGRATION_ARROW[primary]} - {TYPE_NAMES[INTEGRATION_ARROW[primary]]}",
        f"Disintegration (stress) direction: {DISINTEGRATION_ARROW[primary]} - {TYPE_NAMES[DISINTEGRATION_ARROW[primary]]}",
        f"Harmonic triad: {harmonic_triad_for(primary)}",
        f"Hornevian group: {hornevian_group_for(primary)}",
        "Tritype: " + "; ".join(tritype_lines),
        f"Instinctual stack (dominant/secondary/blind spot): {stack_notation} "
        f"({', '.join(f'{INSTINCT_NAMES[c]} {p:.0f}%' for c, p in stack)})",
        f"Functioning score: {functioning_score:.0f}% ({band_label})",
        f"Type score spread (all 9, 0-100): " + ", ".join(
            f"{t}:{v:.0f}" for t, v in sorted(type_result['normalized'].items())),
    ]
    return "\n".join(lines)


def generate_intervention_content(client_name, type_result, instinct_result, functioning_score,
                                   type_answers, instinct_answers, api_key, model=None,
                                   timeout=60):
    """Calls Groq's chat completions API and returns the parsed JSON content dict.
    Raises RuntimeError with a clear message on any failure (missing key, HTTP error,
    bad JSON) so the caller can surface it to the practitioner rather than silently
    falling back to generic content.
    """
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured. Get a free key at https://console.groq.com/keys "
            "(sign up, then 'Create API Key') and add it to Streamlit secrets.")

    profile_context = _build_profile_context(
        client_name, type_result, instinct_result, functioning_score, type_answers, instinct_answers)

    user_message = (
        "Client's assessment profile:\n\n" + profile_context + "\n\n" +
        JSON_SCHEMA_INSTRUCTIONS
    )

    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        "temperature": 0.6,
        "response_format": {"type": "json_object"},
    }

    req = urllib.request.Request(
        GROQ_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"Groq API error {e.code}: {detail[:500]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not reach Groq API: {e.reason}") from e

    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected Groq response shape: {body}") from e

    content = content.strip()
    if content.startswith("```"):
        content = content.strip("`")
        if content.lower().startswith("json"):
            content = content[4:]

    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Groq did not return valid JSON: {e}\nRaw content: {content[:800]}") from e
