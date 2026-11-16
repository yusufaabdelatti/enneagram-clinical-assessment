"""PDF report generation: premium, clinical-style layout with charts.

Narrative/explanatory content (titles, clinical notes, type profiles) always
renders in English regardless of which language the client answered in. Only
the Q&A appendix reflects the client's actual answer language - see
answer_language in generate_pdf_report() and the Arabic rendering helpers
below.
"""

import io
import os
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import arabic_reshaper
from bidi.algorithm import get_display

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether,
)
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .questions import TYPE_NAMES, TYPE_ITEMS, INSTINCT_ITEMS, INSTINCT_NAMES, FUNCTIONING_ITEMS
from .questions_ar import TYPE_ITEMS_AR, INSTINCT_ITEMS_AR, FUNCTIONING_ITEMS_AR
from .content import (
    TYPE_PROFILES, LEVEL_BANDS, CENTER_SUMMARY, FIX_DESCRIPTIONS,
    INSTINCT_POSITION_DESC, ARROW_CLARIFICATION, FUNCTIONING_VS_LEVELS_NOTE,
)
from .scoring import band_for_score

_ARABIC_FONT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "fonts", "NotoNaskhArabic.ttf")
pdfmetrics.registerFont(TTFont("ArabicFont", _ARABIC_FONT_PATH))


def _ar(text):
    """Reshape + bidi-reorder Arabic text so it renders correctly in reportlab."""
    return get_display(arabic_reshaper.reshape(text))

# ---------------------------------------------------------------------------
# Palette - muted, clinical, "premium letterhead" feel
# ---------------------------------------------------------------------------
NAVY = colors.HexColor("#1B2A4A")
SLATE = colors.HexColor("#4A5568")
SLATE_LIGHT = colors.HexColor("#8A94A6")
GOLD = colors.HexColor("#B8975A")
LINE_GRAY = colors.HexColor("#D8DCE3")
BG_PANEL = colors.HexColor("#F6F7F9")
TEXT_DARK = colors.HexColor("#1F2430")

TYPE_COLORS_HEX = {
    1: "#2C5F8A", 2: "#B8975A", 3: "#A6633C", 4: "#7A5C8A",
    5: "#4A7C7C", 6: "#5B6C8F", 7: "#C98A3E", 8: "#8B4A3F", 9: "#3F7D5B",
}

mpl_rc = {
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#D8DCE3",
    "axes.labelcolor": "#4A5568",
    "text.color": "#1F2430",
    "xtick.color": "#4A5568",
    "ytick.color": "#4A5568",
}
plt.rcParams.update(mpl_rc)


def _fig_to_image(fig, width_in=6.5):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=200, bbox_inches="tight", transparent=False, facecolor="white")
    plt.close(fig)
    buf.seek(0)
    img = Image(buf)
    aspect = img.imageHeight / float(img.imageWidth)
    img.drawWidth = width_in * inch
    img.drawHeight = width_in * inch * aspect
    return img


def _radar_chart(normalized_scores):
    types = list(range(1, 10))
    labels = [f"{t}\n{TYPE_NAMES[t]}" for t in types]
    values = [normalized_scores[t] for t in types]
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(types), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="#1B2A4A", linewidth=2)
    ax.fill(angles, values, color="#B8975A", alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=7, color="#8A94A6")
    ax.set_ylim(0, 100)
    ax.spines["polar"].set_color("#D8DCE3")
    ax.grid(color="#D8DCE3", linewidth=0.7)
    pass  # title provided by surrounding report section header
    return _fig_to_image(fig, width_in=5.6)


def _bar_chart_types(ranked):
    types = [r[0] for r in ranked]
    values = [r[1] for r in ranked]
    colors_bar = [TYPE_COLORS_HEX[t] for t in types]
    labels = [f"Type {t} · {TYPE_NAMES[t]}" for t in types]

    fig, ax = plt.subplots(figsize=(7, 4.2))
    y_pos = np.arange(len(types))[::-1]
    ax.barh(y_pos, values, color=colors_bar, height=0.62)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score (%)", fontsize=9)
    pass  # title provided by surrounding report section header
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#D8DCE3")
    for i, v in enumerate(values):
        ax.text(v + 1.5, y_pos[i], f"{v:.0f}%", va="center", fontsize=8.5, color="#4A5568")
    fig.tight_layout()
    return _fig_to_image(fig, width_in=6.4)


def _instinct_chart(instinct_stack):
    names = [INSTINCT_NAMES[i[0]] for i in instinct_stack]
    values = [i[1] for i in instinct_stack]
    bar_colors = ["#1B2A4A", "#5B6C8F", "#B8975A"]

    fig, ax = plt.subplots(figsize=(6, 2.6))
    x_pos = np.arange(len(names))
    ax.bar(x_pos, values, color=bar_colors, width=0.5)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names, fontsize=9)
    ax.set_ylim(0, 100)
    ax.set_ylabel("Score (%)", fontsize=8.5)
    pass  # title provided by surrounding report section header
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)
    for i, v in enumerate(values):
        ax.text(i, v + 2, f"{v:.0f}%", ha="center", fontsize=8.5, color="#4A5568")
    fig.tight_layout()
    return _fig_to_image(fig, width_in=5.6)


def _functioning_gauge(score, band_label):
    fig, ax = plt.subplots(figsize=(6, 1.3))
    ax.barh([0], [100], color="#EEF0F3", height=0.5)
    ax.barh([0], [score], color="#1B2A4A", height=0.5)
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.5, 0.5)
    ax.axis("off")
    ax.text(score, 0.42, f"{score:.0f}%", ha="center", fontsize=10, color="#1B2A4A", weight="bold")
    ax.text(1, -0.42, "Unhealthy", fontsize=8, color="#8A94A6")
    ax.text(50, -0.42, "Average", fontsize=8, color="#8A94A6", ha="center")
    ax.text(99, -0.42, "Healthy", fontsize=8, color="#8A94A6", ha="right")
    fig.tight_layout()
    return _fig_to_image(fig, width_in=5.6)


def _styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(name="ReportTitle", fontName="Helvetica-Bold", fontSize=26,
                           textColor=NAVY, leading=30, spaceAfter=6))
    ss.add(ParagraphStyle(name="ReportSubtitle", fontName="Helvetica", fontSize=12,
                           textColor=SLATE, leading=16, spaceAfter=2))
    ss.add(ParagraphStyle(name="SectionHeader", fontName="Helvetica-Bold", fontSize=15,
                           textColor=NAVY, leading=18, spaceBefore=18, spaceAfter=8))
    ss.add(ParagraphStyle(name="SubHeader", fontName="Helvetica-Bold", fontSize=11.5,
                           textColor=GOLD, leading=14, spaceBefore=10, spaceAfter=4))
    ss.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=9.7,
                           textColor=TEXT_DARK, leading=14.5, spaceAfter=6))
    ss.add(ParagraphStyle(name="BodySmall", fontName="Helvetica", fontSize=8.6,
                           textColor=SLATE, leading=12.5, spaceAfter=4))
    ss.add(ParagraphStyle(name="Label", fontName="Helvetica-Bold", fontSize=8.5,
                           textColor=SLATE, leading=11))
    ss.add(ParagraphStyle(name="QItem", fontName="Helvetica", fontSize=8.3,
                           textColor=TEXT_DARK, leading=12))
    ss.add(ParagraphStyle(name="QItemAR", fontName="ArabicFont", fontSize=9.2,
                           textColor=TEXT_DARK, leading=15, alignment=TA_RIGHT))
    ss.add(ParagraphStyle(name="CoverFooter", fontName="Helvetica", fontSize=9,
                           textColor=SLATE_LIGHT, alignment=TA_CENTER, leading=12))
    return ss


def _header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE_GRAY)
    canvas.setLineWidth(0.6)
    canvas.line(0.75 * inch, LETTER[1] - 0.6 * inch, LETTER[0] - 0.75 * inch, LETTER[1] - 0.6 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(SLATE_LIGHT)
    canvas.drawString(0.75 * inch, LETTER[1] - 0.5 * inch, "Enneagram Clinical Profile")
    canvas.drawRightString(LETTER[0] - 0.75 * inch, LETTER[1] - 0.5 * inch, "Confidential")

    canvas.setStrokeColor(LINE_GRAY)
    canvas.line(0.75 * inch, 0.65 * inch, LETTER[0] - 0.75 * inch, 0.65 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(SLATE_LIGHT)
    canvas.drawString(0.75 * inch, 0.5 * inch, f"Generated {datetime.now().strftime('%B %d, %Y')}")
    canvas.drawRightString(LETTER[0] - 0.75 * inch, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()


def generate_pdf_report(client_info, type_result, instinct_result, functioning_score,
                         type_answers, instinct_answers, functioning_answers, answer_language="en"):
    """Returns PDF bytes. All narrative content is always English; when
    answer_language == "ar", only the Q&A appendix statement text switches to
    the Arabic wording the client actually saw (properly shaped/reordered)."""
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=LETTER,
        leftMargin=0.75 * inch, rightMargin=0.75 * inch,
        topMargin=0.85 * inch, bottomMargin=0.85 * inch,
        title="Enneagram Clinical Profile",
    )
    ss = _styles()
    story = []

    # ---------------- Cover page ----------------
    story.append(Spacer(1, 1.6 * inch))
    story.append(Paragraph("ENNEAGRAM", ParagraphStyle(
        name="Brand", fontName="Helvetica-Bold", fontSize=14, textColor=GOLD,
        alignment=TA_CENTER, leading=16, spaceAfter=4)))
    story.append(Paragraph("Clinical Personality Profile", ParagraphStyle(
        name="BrandTitle", fontName="Helvetica-Bold", fontSize=28, textColor=NAVY,
        alignment=TA_CENTER, leading=32, spaceAfter=20)))
    story.append(HRFlowable(width="40%", thickness=1, color=GOLD, hAlign="CENTER", spaceAfter=24))

    client_name = client_info.get("name") or "Confidential Client"
    story.append(Paragraph(client_name, ParagraphStyle(
        name="ClientName", fontName="Helvetica-Bold", fontSize=18, textColor=TEXT_DARK,
        alignment=TA_CENTER, spaceAfter=6)))
    story.append(Paragraph(datetime.now().strftime("Assessment date: %B %d, %Y"), ParagraphStyle(
        name="ClientDate", fontName="Helvetica", fontSize=11, textColor=SLATE,
        alignment=TA_CENTER, spaceAfter=40)))

    primary = type_result["primary_type"]
    wing = type_result["wing"]
    story.append(Paragraph(
        f"Primary Type: {primary} — {TYPE_NAMES[primary]}  (Wing: {wing})",
        ParagraphStyle(name="PrimaryBanner", fontName="Helvetica-Bold", fontSize=15,
                       textColor=colors.white, alignment=TA_CENTER, backColor=NAVY,
                       borderPadding=(10, 14, 10, 14), leading=18)
    ))
    story.append(Spacer(1, 1.2 * inch))
    story.append(Paragraph(
        "Prepared for use in a therapeutic context. This report is a clinical conversation "
        "support tool, not a stand-alone diagnostic instrument, and is intended for review "
        "together with a licensed therapist.",
        ss["CoverFooter"]))
    story.append(PageBreak())

    # ---------------- Summary / Overview ----------------
    story.append(Paragraph("Clinical Summary", ss["SectionHeader"]))
    prof = TYPE_PROFILES[primary]
    summary_tbl_data = [
        ["Primary Type", f"{primary} — {prof['name']}"],
        ["Wing", f"{wing} — {TYPE_NAMES[wing]}"],
        ["Tritype", "  /  ".join(f"{v} ({k.split(' ')[0]})" for k, v in type_result["tritype"].items())],
        ["Dominant Instinct", INSTINCT_NAMES[instinct_result["stack"][0][0]]],
        ["Growth Direction", f"Integration → Type {type_result['integration']} ({TYPE_NAMES[type_result['integration']]})"],
        ["Stress Direction", f"Disintegration → Type {type_result['disintegration']} ({TYPE_NAMES[type_result['disintegration']]})"],
    ]
    t = Table(summary_tbl_data, colWidths=[1.7 * inch, 4.6 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BG_PANEL),
        ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9.3),
        ("GRID", (0, 0), (-1, -1), 0.5, LINE_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(Paragraph(prof["basic_pattern"], ss["Body"]))

    # ---------------- Radar + bar charts ----------------
    story.append(PageBreak())
    story.append(Paragraph("Type Distribution", ss["SectionHeader"]))
    story.append(_radar_chart(type_result["normalized"]))
    story.append(PageBreak())
    story.append(Paragraph("Type Scores — Ranked", ss["SectionHeader"]))
    story.append(_bar_chart_types(type_result["ranked"]))
    story.append(Spacer(1, 14))
    story.append(Paragraph("Instinctual Stacking", ss["SectionHeader"]))
    story.append(_instinct_chart(instinct_result["stack"]))

    # ---------------- Primary type deep dive ----------------
    story.append(Paragraph(f"Type {primary}: {prof['name']}", ss["SectionHeader"]))
    story.append(Paragraph(f"<i>Also known as: {prof['alt_names']}</i>", ss["BodySmall"]))
    story.append(Paragraph(f"<b>Core Fear:</b> {prof['core_fear']}", ss["Body"]))
    story.append(Paragraph(f"<b>Core Desire:</b> {prof['core_desire']}", ss["Body"]))
    story.append(Paragraph(f"<b>Core Motivation:</b> {prof['core_motivation']}", ss["Body"]))

    story.append(Paragraph("Levels of Functioning (Type-Specific)", ss["SubHeader"]))
    for lvl, key in [("Healthy", "healthy"), ("Average", "average"), ("Unhealthy", "unhealthy")]:
        story.append(Paragraph(f"<b>{lvl}:</b> {prof[key]}", ss["Body"]))

    story.append(Paragraph("Growth & Stress Pathways", ss["SubHeader"]))
    story.append(Paragraph(f"<b>Under stress:</b> {prof['stress_behaviors']}", ss["Body"]))
    story.append(Paragraph(f"<b>Stress arrow:</b> {prof['stress_direction']}", ss["Body"]))
    story.append(Paragraph(f"<b>Growth arrow:</b> {prof['growth_direction']}", ss["Body"]))
    story.append(Paragraph(f"<i>{ARROW_CLARIFICATION}</i>", ss["BodySmall"]))

    story.append(Paragraph("Clinical Notes", ss["SubHeader"]))
    story.append(Paragraph(prof["therapy_notes"], ss["Body"]))

    story.append(Paragraph("Suggested Questions to Explore in Session", ss["SubHeader"]))
    for q in prof["questions_to_explore"]:
        story.append(Paragraph(f"• {q}", ss["Body"]))

    # Wing flavor
    story.append(Paragraph(f"Wing Influence: {wing} ({TYPE_NAMES[wing]})", ss["SubHeader"]))
    wing_prof = TYPE_PROFILES[wing]
    story.append(Paragraph(
        f"The {wing} wing contributes a secondary flavor drawn from {wing_prof['name']}, "
        f"whose core motivation is \"{wing_prof['core_motivation']}\" This often blends with the "
        f"primary type's pattern rather than replacing it.", ss["Body"]))

    story.append(Spacer(1, 10))
    stack = instinct_result["stack"]
    stack_notation = " / ".join(code.upper() for code, _pct in stack)
    story.append(Paragraph(f"<b>Full Instinctual Stack: {stack_notation}</b>", ss["Body"]))
    position_labels = ["dominant", "secondary", "blind_spot"]
    for (code, pct), pos in zip(stack, position_labels):
        label = pos.replace("_", " ").title()
        story.append(Paragraph(
            f"<b>{label} — {INSTINCT_NAMES[code]} ({pct:.0f}%):</b> {INSTINCT_POSITION_DESC[pos]}",
            ss["Body"]))

    # ---------------- Functioning level ----------------
    story.append(Paragraph("Overall Functioning Indicator", ss["SectionHeader"]))
    band_label, band_desc = band_for_score(functioning_score, LEVEL_BANDS)
    story.append(_functioning_gauge(functioning_score, band_label))
    story.append(Paragraph(f"<b>{band_label}</b> ({functioning_score:.0f}%)", ss["Body"]))
    story.append(Paragraph(band_desc, ss["Body"]))
    story.append(Paragraph(
        "<i>Note: this is a general self-report indicator of current functioning, not a validated "
        "clinical scale. It is intended as a conversation starting point only.</i>", ss["BodySmall"]))
    story.append(Spacer(1, 6))
    story.append(Paragraph("<b>Traditional Enneagram Level (1-9):</b> Cannot be reliably determined "
                            "from this score - see note below.", ss["Body"]))
    story.append(Paragraph(FUNCTIONING_VS_LEVELS_NOTE, ss["BodySmall"]))

    story.append(PageBreak())

    # ---------------- Centers ----------------
    story.append(Paragraph("Centers of Intelligence (Tritype Summary)", ss["SectionHeader"]))
    story.append(Paragraph(
        f"<b>Core Type (primary driver): {primary} — {prof['name']}.</b> The two fixes below are "
        f"supporting influences from the other centers, not alternate core types.", ss["Body"]))
    for center, type_num in type_result["tritype"].items():
        story.append(Paragraph(f"{center} → Type {type_num} ({TYPE_NAMES[type_num]})", ss["SubHeader"]))
        story.append(Paragraph(CENTER_SUMMARY[center], ss["Body"]))
        story.append(Paragraph(FIX_DESCRIPTIONS[center], ss["BodySmall"]))

    story.append(PageBreak())

    # ---------------- Full Q&A appendix ----------------
    is_ar = answer_language == "ar"
    story.append(Paragraph("Appendix A — Full Item Responses (Type Scale)", ss["SectionHeader"]))
    if is_ar:
        story.append(Paragraph(
            "<i>The client answered in Arabic; statement text below is shown as presented to them.</i>",
            ss["BodySmall"]))
    qa_rows = [["#", "Type", "Statement", "Response"]]
    for idx, (t, text) in enumerate(TYPE_ITEMS):
        ans = type_answers.get(idx, "—")
        cell = Paragraph(_ar(TYPE_ITEMS_AR[idx]), ss["QItemAR"]) if is_ar else text
        qa_rows.append([str(idx + 1), str(t), cell, str(ans)])
    qa_table = Table(qa_rows, colWidths=[0.28 * inch, 0.38 * inch, 4.9 * inch, 0.55 * inch], repeatRows=1)
    qa_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.3),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (1, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(qa_table)

    story.append(PageBreak())
    story.append(Paragraph("Appendix B — Instinctual Variant Responses", ss["SectionHeader"]))
    if is_ar:
        story.append(Paragraph(
            "<i>The client answered in Arabic; statement text below is shown as presented to them.</i>",
            ss["BodySmall"]))
    inst_rows = [["#", "Instinct", "Statement", "Response"]]
    for idx, (inst, text) in enumerate(INSTINCT_ITEMS):
        ans = instinct_answers.get(idx, "—")
        cell = Paragraph(_ar(INSTINCT_ITEMS_AR[idx]), ss["QItemAR"]) if is_ar else text
        inst_rows.append([str(idx + 1), INSTINCT_NAMES[inst], cell, str(ans)])
    inst_table = Table(inst_rows, colWidths=[0.28 * inch, 1.1 * inch, 4.15 * inch, 0.58 * inch], repeatRows=1)
    inst_table.setStyle(qa_table.getStyle() if hasattr(qa_table, "getStyle") else TableStyle([]))
    inst_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.3),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (1, -1), "CENTER"),
        ("ALIGN", (3, 0), (3, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(inst_table)

    story.append(PageBreak())
    story.append(Paragraph("Appendix C — Functioning Scale Responses", ss["SectionHeader"]))
    if is_ar:
        story.append(Paragraph(
            "<i>The client answered in Arabic; statement text below is shown as presented to them.</i>",
            ss["BodySmall"]))
    func_rows = [["#", "Statement", "Response"]]
    for idx, text in enumerate(FUNCTIONING_ITEMS):
        ans = functioning_answers.get(idx, "—")
        cell = Paragraph(_ar(FUNCTIONING_ITEMS_AR[idx]), ss["QItemAR"]) if is_ar else text
        func_rows.append([str(idx + 1), cell, str(ans)])
    func_table = Table(func_rows, colWidths=[0.3 * inch, 5.3 * inch, 0.6 * inch], repeatRows=1)
    func_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (2, 0), (2, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    story.append(func_table)

    doc.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
    buf.seek(0)
    return buf.getvalue()
