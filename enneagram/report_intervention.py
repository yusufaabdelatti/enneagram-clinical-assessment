"""
Report 2: Personalized Intervention & Session Planning Report.

Confidential, practitioner-only. Content comes from Groq (see groq_utils.py),
grounded in the client's actual assessment results. This module only handles
layout/rendering - it never invents clinical content itself.
"""

import io
from datetime import datetime

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable,
)

from .questions import TYPE_NAMES
from .content import TYPE_PROFILES
from .report import NAVY, SLATE, SLATE_LIGHT, GOLD, LINE_GRAY, BG_PANEL, TEXT_DARK

MAROON = colors.HexColor("#7A2E2E")
MAROON_BG = colors.HexColor("#F7EDEC")

# Helvetica/WinAnsiEncoding covers common "smart" typography (curly quotes,
# en/em dashes, ellipsis) just fine - reportlab re-encodes those automatically.
# What it does NOT cover is the hyphen-variant block (non-breaking hyphen etc.),
# which an LLM sometimes emits in compound terms like "Type‑1" and which then
# renders as a missing-glyph box. Only normalize those specific characters;
# don't touch anything else, or we mangle perfectly fine punctuation.
_CHAR_REPLACEMENTS = {
    "‐": "-", "‑": "-", "‒": "-", "―": "-",  # hyphen variants
    " ": " ",  # non-breaking space
}


def _sanitize(obj):
    if isinstance(obj, str):
        for bad, good in _CHAR_REPLACEMENTS.items():
            obj = obj.replace(bad, good)
        return obj
    if isinstance(obj, dict):
        return {k: _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize(v) for v in obj]
    return obj


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(name="IRTitle", fontName="Helvetica-Bold", fontSize=15,
                           textColor=NAVY, leading=18, spaceBefore=4, spaceAfter=8))
    ss.add(ParagraphStyle(name="IRSub", fontName="Helvetica-Bold", fontSize=11.5,
                           textColor=GOLD, leading=14, spaceBefore=10, spaceAfter=4))
    ss.add(ParagraphStyle(name="IRBody", fontName="Helvetica", fontSize=9.4,
                           textColor=TEXT_DARK, leading=13.8, spaceAfter=5))
    ss.add(ParagraphStyle(name="IRSmall", fontName="Helvetica", fontSize=8.3,
                           textColor=SLATE, leading=11.8, spaceAfter=4))
    ss.add(ParagraphStyle(name="IRCell", fontName="Helvetica", fontSize=8.2,
                           textColor=TEXT_DARK, leading=11.2))
    ss.add(ParagraphStyle(name="IRCellBold", fontName="Helvetica-Bold", fontSize=8.2,
                           textColor=NAVY, leading=11.2))
    ss.add(ParagraphStyle(name="IRHead", fontName="Helvetica-Bold", fontSize=8.2,
                           textColor=colors.white, leading=11.2))
    return ss


def _kv_table(rows, ss, col_widths=(1.3 * inch, 5.2 * inch)):
    body = [[Paragraph(f"<b>{k}</b>", ss["IRCellBold"]), Paragraph(v, ss["IRCell"])] for k, v in rows]
    t = Table(body, colWidths=list(col_widths))
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("BACKGROUND", (0, 0), (0, -1), BG_PANEL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def _header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE_GRAY)
    canvas.line(0.7 * inch, LETTER[1] - 0.55 * inch, LETTER[0] - 0.7 * inch, LETTER[1] - 0.55 * inch)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(MAROON)
    canvas.drawString(0.7 * inch, LETTER[1] - 0.45 * inch, "CONFIDENTIAL — PRACTITIONER USE ONLY")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(SLATE_LIGHT)
    canvas.drawRightString(LETTER[0] - 0.7 * inch, LETTER[1] - 0.45 * inch, "Intervention & Session Planning Report")
    canvas.line(0.7 * inch, 0.55 * inch, LETTER[0] - 0.7 * inch, 0.55 * inch)
    canvas.drawRightString(LETTER[0] - 0.7 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


def generate_intervention_pdf(client_info, type_result, instinct_result, functioning_score, ai_content):
    ai_content = _sanitize(ai_content)
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=LETTER, leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.85 * inch, bottomMargin=0.85 * inch,
        title="Enneagram Intervention & Session Planning Report",
    )
    ss = _styles()
    story = []

    primary = type_result["primary_type"]
    wing = type_result["wing"]
    prof = TYPE_PROFILES[primary]
    client_name = client_info.get("name") or "Confidential Client"

    # ---------------- Cover ----------------
    story.append(Spacer(1, 0.9 * inch))
    story.append(Paragraph(
        "CONFIDENTIAL — PRACTITIONER / PSYCHOLOGIST USE ONLY — NOT FOR CLIENT DISTRIBUTION",
        ParagraphStyle(name="Banner", fontName="Helvetica-Bold", fontSize=11, textColor=colors.white,
                       alignment=TA_CENTER, backColor=MAROON, borderPadding=(8, 10, 8, 10), leading=14)))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph("ENNEAGRAM", ParagraphStyle(
        name="Brand", fontName="Helvetica-Bold", fontSize=13, textColor=GOLD,
        alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph("Intervention & Session Planning Report", ParagraphStyle(
        name="BrandTitle", fontName="Helvetica-Bold", fontSize=22, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=14, leading=26)))
    story.append(HRFlowable(width="35%", thickness=1, color=GOLD, hAlign="CENTER", spaceAfter=20))
    story.append(Paragraph(client_name, ParagraphStyle(
        name="ClientName", fontName="Helvetica-Bold", fontSize=16, textColor=TEXT_DARK,
        alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph(datetime.now().strftime("Prepared %B %d, %Y"), ParagraphStyle(
        name="ClientDate", fontName="Helvetica", fontSize=10.5, textColor=SLATE,
        alignment=TA_CENTER, spaceAfter=30)))
    story.append(Paragraph(
        f"Primary Type {primary} ({prof['name']}) · Wing {wing} ({TYPE_NAMES[wing]})",
        ParagraphStyle(name="PrimaryBanner", fontName="Helvetica-Bold", fontSize=13,
                       textColor=colors.white, alignment=TA_CENTER, backColor=NAVY,
                       borderPadding=(8, 12, 8, 12), leading=16)))
    story.append(Spacer(1, 0.6 * inch))
    story.append(Paragraph(
        "This report translates the attached assessment results into practical discussion points and "
        "potential intervention directions for use in session. It is generated from this client's "
        "actual profile and is intended to support - not replace - the practitioner's own clinical "
        "judgment. Content is hypothesis-generating, not diagnostic.",
        ParagraphStyle(name="CoverFooter", fontName="Helvetica", fontSize=9.5, textColor=SLATE,
                       alignment=TA_CENTER, leading=13.5)))
    story.append(PageBreak())

    # ---------------- A. Psychological Formulation ----------------
    pf = ai_content.get("psychological_formulation", {})
    story.append(Paragraph("A. Psychological Formulation", ss["IRTitle"]))
    rows = [
        ("Core Motivations", pf.get("core_motivations", "")),
        ("Underlying Fears", pf.get("underlying_fears", "")),
        ("Cognitive/Emotional Patterns", pf.get("cognitive_emotional_patterns", "")),
        ("Defensive Tendencies", pf.get("defensive_tendencies", "")),
        ("Interpersonal Patterns", pf.get("interpersonal_patterns", "")),
        ("Flexibility & Rigidity", pf.get("flexibility_and_rigidity", "")),
    ]
    story.append(_kv_table(rows, ss))
    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Evidence vs. Hypothesis:</b> " + pf.get("evidence_vs_hypothesis", ""),
                            ss["IRBody"]))
    story.append(PageBreak())

    # ---------------- B. Strengths & C. Development Areas ----------------
    story.append(Paragraph("B. Strengths and Resources", ss["IRTitle"]))
    for s in ai_content.get("strengths_and_resources", []):
        story.append(Paragraph(f"• {s}", ss["IRBody"]))

    story.append(Paragraph("C. Potential Development Areas", ss["IRTitle"]))
    for d in ai_content.get("development_areas", []):
        story.append(Paragraph(f"• {d}", ss["IRBody"]))
    story.append(PageBreak())

    # ---------------- D. Session Questions ----------------
    story.append(Paragraph("D. Suggested Session Questions", ss["IRTitle"]))
    story.append(Paragraph(
        "Open-ended, intended to invite reflection - not to lead the client toward confirming "
        "the assessment result.", ss["IRSmall"]))
    for theme, questions in ai_content.get("session_questions", {}).items():
        story.append(Paragraph(theme, ss["IRSub"]))
        for q in questions:
            story.append(Paragraph(f"• {q}", ss["IRBody"]))
    story.append(PageBreak())

    # ---------------- E. Discussion Topics ----------------
    story.append(Paragraph("E. Suggested Discussion Topics", ss["IRTitle"]))
    for topic in ai_content.get("discussion_topics", []):
        rows = [
            ("Topic", topic.get("topic", "")),
            ("Why Relevant", topic.get("why_relevant", "")),
            ("What to Explore", topic.get("explore", "")),
        ]
        story.append(_kv_table(rows, ss))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ---------------- F. Scenarios ----------------
    story.append(Paragraph("F. Choice-Based Scenarios & Exercises", ss["IRTitle"]))
    story.append(Paragraph(
        "For discussion only - a selected choice is never proof of a type or condition. The goal is "
        "self-reflection and identifying behavioral alternatives.", ss["IRSmall"]))
    for scenario in ai_content.get("scenarios", []):
        story.append(Paragraph(f"Scenario: {scenario.get('title', '')}", ss["IRSub"]))
        story.append(Paragraph(scenario.get("situation", ""), ss["IRBody"]))
        for choice in scenario.get("choices", []):
            rows = [
                (f"Choice {choice.get('label', '')}", choice.get("text", "")),
                ("Possible Pattern", choice.get("pattern", "")),
                ("Possible Motivation", choice.get("motivation", "")),
                ("Possible Consequences", choice.get("consequences", "")),
                ("Alternative to Explore", choice.get("alternative", "")),
            ]
            story.append(_kv_table(rows, ss))
            story.append(Spacer(1, 6))
        story.append(Spacer(1, 6))
    story.append(PageBreak())

    # ---------------- G. Interventions ----------------
    story.append(Paragraph("G. Suggested Interventions & Practical Exercises", ss["IRTitle"]))
    for iv in ai_content.get("interventions", []):
        tag = "Requires clinical judgment" if iv.get("requires_clinical_judgment") else "General self-development exercise"
        story.append(Paragraph(f"{iv.get('modality', '')} — <i>{tag}</i>", ss["IRSub"]))
        rows = [
            ("Target Pattern", iv.get("target_pattern", "")),
            ("Objective", iv.get("objective", "")),
            ("Explanation", iv.get("explanation", "")),
            ("Implementation", iv.get("implementation", "")),
            ("Homework/Reflection", iv.get("homework", "")),
        ]
        story.append(_kv_table(rows, ss))
        story.append(Spacer(1, 8))
    story.append(PageBreak())

    # ---------------- H. Session Roadmap ----------------
    story.append(Paragraph("H. Suggested Session Roadmap", ss["IRTitle"]))
    story.append(Paragraph(
        "A flexible suggested sequence, not a mandatory treatment protocol.", ss["IRSmall"]))
    roadmap_rows = [[Paragraph("Phase", ss["IRHead"]), Paragraph("Description", ss["IRHead"])]]
    for step in ai_content.get("session_roadmap", []):
        roadmap_rows.append([
            Paragraph(f"<b>{step.get('phase', '')}</b>", ss["IRCell"]),
            Paragraph(step.get("description", ""), ss["IRCell"]),
        ])
    rtbl = Table(roadmap_rows, colWidths=[1.5 * inch, 5.0 * inch], repeatRows=1)
    rtbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(rtbl)

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    buf.seek(0)
    return buf.getvalue()
