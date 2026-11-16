"""
One-off generator for a personal Enneagram study guide PDF.
Not used by the Streamlit app - run manually: python make_study_guide.py
Reuses the same visual language as the client report for consistency.
"""

import io
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable,
)

from enneagram.questions import (
    TYPE_NAMES, WINGS, CENTERS, INTEGRATION_ARROW, DISINTEGRATION_ARROW, INSTINCT_NAMES,
    HARMONIC_TRIADS, HORNEVIAN_GROUPS, harmonic_triad_for, hornevian_group_for,
)
from enneagram.content import (
    TYPE_PROFILES, LEVEL_BANDS, CENTER_SUMMARY, HARMONIC_TRIAD_DESC, HORNEVIAN_GROUP_DESC,
    RISO_HUDSON_LEVELS, FUNCTIONING_VS_LEVELS_NOTE, ARROW_CLARIFICATION,
)
from enneagram.report import NAVY, SLATE, SLATE_LIGHT, GOLD, LINE_GRAY, BG_PANEL, TEXT_DARK, TYPE_COLORS_HEX

CENTER_EMOTION = {
    "Body (Gut) Center": "Anger / rage",
    "Heart Center": "Shame",
    "Head Center": "Fear / anxiety",
}
CENTER_TYPES_LABEL = {
    "Body (Gut) Center": "8, 9, 1",
    "Heart Center": "2, 3, 4",
    "Head Center": "5, 6, 7",
}


def styles():
    ss = getSampleStyleSheet()
    ss.add(ParagraphStyle(name="GTitle", fontName="Helvetica-Bold", fontSize=15,
                           textColor=NAVY, leading=18, spaceBefore=4, spaceAfter=8))
    ss.add(ParagraphStyle(name="GSub", fontName="Helvetica-Bold", fontSize=11,
                           textColor=GOLD, leading=13, spaceBefore=8, spaceAfter=4))
    ss.add(ParagraphStyle(name="GBody", fontName="Helvetica", fontSize=9.4,
                           textColor=TEXT_DARK, leading=13.5, spaceAfter=5))
    ss.add(ParagraphStyle(name="GSmall", fontName="Helvetica", fontSize=8.2,
                           textColor=SLATE, leading=11.5, spaceAfter=3))
    ss.add(ParagraphStyle(name="GCell", fontName="Helvetica", fontSize=7.8,
                           textColor=TEXT_DARK, leading=10.5))
    ss.add(ParagraphStyle(name="GCellBold", fontName="Helvetica-Bold", fontSize=7.8,
                           textColor=NAVY, leading=10.5))
    ss.add(ParagraphStyle(name="GTCell", fontName="Helvetica", fontSize=8.2,
                           textColor=TEXT_DARK, leading=10.8))
    ss.add(ParagraphStyle(name="GTHead", fontName="Helvetica-Bold", fontSize=8.2,
                           textColor=colors.white, leading=10.8))
    return ss


def row_of(cells, ss, header=False):
    style = ss["GTHead"] if header else ss["GTCell"]
    return [Paragraph(str(c), style) for c in cells]


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE_GRAY)
    canvas.line(0.7 * inch, LETTER[1] - 0.55 * inch, LETTER[0] - 0.7 * inch, LETTER[1] - 0.55 * inch)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(SLATE_LIGHT)
    canvas.drawString(0.7 * inch, LETTER[1] - 0.45 * inch, "Enneagram Study Guide")
    canvas.drawRightString(LETTER[0] - 0.7 * inch, LETTER[1] - 0.45 * inch, "Personal Reference")
    canvas.line(0.7 * inch, 0.55 * inch, LETTER[0] - 0.7 * inch, 0.55 * inch)
    canvas.drawRightString(LETTER[0] - 0.7 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build():
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=LETTER, leftMargin=0.7 * inch, rightMargin=0.7 * inch,
                             topMargin=0.8 * inch, bottomMargin=0.75 * inch,
                             title="Enneagram Study Guide")
    ss = styles()
    story = []

    # ---------- Cover ----------
    story.append(Spacer(1, 1.6 * inch))
    story.append(Paragraph("ENNEAGRAM", ParagraphStyle(
        name="Brand", fontName="Helvetica-Bold", fontSize=13, textColor=GOLD,
        alignment=TA_CENTER, spaceAfter=4)))
    story.append(Paragraph("Rapid Study Guide", ParagraphStyle(
        name="BrandTitle", fontName="Helvetica-Bold", fontSize=26, textColor=NAVY,
        alignment=TA_CENTER, spaceAfter=16)))
    story.append(HRFlowable(width="35%", thickness=1, color=GOLD, hAlign="CENTER", spaceAfter=20))
    story.append(Paragraph(
        "Theory, structure, and clinical interpretation - condensed for fast, working fluency "
        "and for reading the clinical assessment reports produced by this tool.",
        ParagraphStyle(name="BrandSub", fontName="Helvetica", fontSize=11, textColor=SLATE,
                       alignment=TA_CENTER, leading=15)))
    story.append(PageBreak())

    # ---------- What is the Enneagram? ----------
    story.append(Paragraph("What Is the Enneagram?", ss["GTitle"]))
    story.append(Paragraph(
        "The Enneagram is a model of nine interconnected personality patterns, each organized "
        "around a specific core fear and core desire that quietly drives attention, emotion, and "
        "behavior. Its roots are in older philosophical and spiritual traditions; it was shaped into "
        "a psychological framework in the 20th century (notably by Oscar Ichazo and Claude Naranjo) "
        "and later systematized clinically by Don Riso and Russ Hudson, whose work this tool draws "
        "on most directly (the nine types, wings, arrows, and levels of development).", ss["GBody"]))
    story.append(Paragraph(
        "Unlike trait models (e.g. Big Five) that describe <i>how much</i> of a trait someone has, "
        "the Enneagram describes a <i>motivational story</i>: what someone is unconsciously "
        "organizing their life to avoid (the fear) and to secure (the desire). Two people can look "
        "similar on the surface and be completely different types if their underlying motivation "
        "differs - which is why self-report alone is a starting hypothesis, not a verdict.", ss["GBody"]))
    story.append(Paragraph(
        "In this tool specifically, the Enneagram is used as a <b>clinical conversation aid</b>: a "
        "structured way to surface a client's likely core pattern so you and the client have a "
        "shared vocabulary to explore it together - not as a validated diagnostic instrument.",
        ss["GBody"]))

    story.append(Paragraph("Key Terms", ss["GSub"]))
    terms = [
        ("Type", "One of the nine core personality patterns (1-9). Each is a coherent strategy for managing one core fear."),
        ("Core Fear", "The specific threat a type is organized to avoid (e.g. Type 1 fears being bad/wrong). Drives most of the type's compulsive behavior."),
        ("Core Desire", "The positive state a type is organized to secure (e.g. Type 1 wants to be good/have integrity). The flip side of the core fear."),
        ("Core Motivation", "A one-line summary of the ongoing internal project the fear and desire together produce."),
        ("Basic Pattern", "How the fear/desire combination actually plays out day to day - the type's habitual way of thinking, feeling, and coping."),
        ("Center of Intelligence", "One of three groups (Body/Heart/Head) types belong to, based on which core emotion (anger/shame/fear) they are organized around."),
        ("Wing", "One of the two numerically adjacent types that flavors the primary type without changing its core motivation."),
        ("Arrows (Growth / Stress)", "Two other types whose behaviors a person tends to 'borrow' - growth (integration) under security and self-awareness, stress (disintegration) under pressure. Not a change of core type."),
        ("Levels of Health", "A healthy / average / unhealthy spectrum describing how rigidly or compulsively a type's pattern is currently being lived out, independent of which type it is."),
        ("Tritype", "The single highest-scoring type within each of the three centers, combined - gives a 3-number fuller picture than the primary type alone."),
        ("Instinctual Variant (sp / so / sx)", "Which of three instinctual drives - self-preservation, social, or sexual/one-to-one - gets a person's attention first, independent of type."),
        ("Functioning Score", "A general self-report wellbeing/capacity indicator used in this tool's report. Not part of Enneagram theory itself - a separate mood/capacity check."),
    ]
    trows = [row_of(["Term", "Definition"], ss, header=True)] + [row_of([k, v], ss) for k, v in terms]
    ttbl2 = Table(trows, colWidths=[1.7 * inch, 4.8 * inch], repeatRows=1)
    ttbl2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(ttbl2)
    story.append(PageBreak())

    # ---------- Nine types at a glance ----------
    story.append(Paragraph("The Nine Types at a Glance", ss["GTitle"]))
    story.append(Paragraph(
        "Every type is a strategy for managing its core fear. When behavior is confusing, "
        "ask: <i>what fear is this protecting against?</i>", ss["GBody"]))
    rows = [row_of(["#", "Name", "Core Fear", "Core Desire"], ss, header=True)]
    for t in range(1, 10):
        p = TYPE_PROFILES[t]
        rows.append(row_of([t, p["name"], p["core_fear"], p["core_desire"]], ss))
    tbl = Table(rows, colWidths=[0.3 * inch, 1.0 * inch, 2.7 * inch, 2.5 * inch], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(tbl)

    # ---------- Centers ----------
    story.append(Paragraph("Centers of Intelligence", ss["GSub"]))
    story.append(Paragraph(
        "The center tells you <b>what emotion is being avoided</b>; the type tells you <b>how</b>.",
        ss["GBody"]))
    crows = [row_of(["Center", "Types", "Core Emotion", "Summary"], ss, header=True)]
    for center, _members in CENTERS.items():
        crows.append(row_of([center.replace(" Center", ""), CENTER_TYPES_LABEL[center],
                              CENTER_EMOTION[center], CENTER_SUMMARY[center]], ss))
    ctbl = Table(crows, colWidths=[1.0 * inch, 0.7 * inch, 0.9 * inch, 3.9 * inch], repeatRows=1)
    ctbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(ctbl)
    story.append(PageBreak())

    # ---------- Harmonic & Hornevian Triads ----------
    story.append(Paragraph("Harmonic & Hornevian Triads", ss["GTitle"]))
    story.append(Paragraph(
        "Two further three-way groupings (developed by Riso and Hudson) cut across the Centers of "
        "Intelligence above - they classify types by <i>coping style</i> rather than by which core "
        "emotion they organize around.", ss["GBody"]))

    story.append(Paragraph("Harmonic Triads - response to frustration/difficulty", ss["GSub"]))
    hrows = [row_of(["Triad", "Types", "How they cope"], ss, header=True)]
    for name, members in HARMONIC_TRIADS.items():
        hrows.append(row_of([name, ", ".join(str(m) for m in members), HARMONIC_TRIAD_DESC[name]], ss))
    htbl = Table(hrows, colWidths=[1.3 * inch, 0.7 * inch, 4.6 * inch], repeatRows=1)
    htbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(htbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Hornevian Groups - how needs are pursued", ss["GSub"]))
    story.append(Paragraph(
        "<i>Named for psychoanalyst Karen Horney's \"moving toward / against / away\" framework; "
        "Horney did not map this to the Enneagram herself - later Enneagram teachers found the "
        "alignment and adopted the names.</i>", ss["GSmall"]))
    nrows = [row_of(["Group", "Types", "How they pursue needs"], ss, header=True)]
    for name, members in HORNEVIAN_GROUPS.items():
        nrows.append(row_of([name, ", ".join(str(m) for m in members), HORNEVIAN_GROUP_DESC[name]], ss))
    ntbl = Table(nrows, colWidths=[1.3 * inch, 0.7 * inch, 4.6 * inch], repeatRows=1)
    ntbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(ntbl)
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<b>Note:</b> these triads are most associated with the Riso-Hudson school specifically and "
        "receive some criticism from other Enneagram lineages - treat them as a useful lens, not a "
        "universally agreed-upon layer of the model.", ss["GSmall"]))
    story.append(PageBreak())

    # ---------- Wings / Arrows / Instincts ----------
    story.append(Paragraph("Wings, Arrows & Instincts", ss["GTitle"]))
    story.append(Paragraph(
        "<b>Wings</b> - a neighboring type that flavors the core pattern without changing it. "
        "Don't overweight this; it's seasoning, not a second type.", ss["GBody"]))
    wrows = [row_of(["Type", "Wing Options"], ss, header=True)]
    for t in range(1, 10):
        a, b = WINGS[t]
        wrows.append(row_of([f"{t} {TYPE_NAMES[t]}", f"{a} {TYPE_NAMES[a]}  /  {b} {TYPE_NAMES[b]}"], ss))
    wtbl = Table(wrows, colWidths=[1.6 * inch, 4.9 * inch], repeatRows=1)
    wtbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(wtbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Arrows</b> - lines to two other types describing <i>borrowed behavior</i>, not a change "
        "of core type. The stress arrow often explains a presenting complaint (\"why am I acting "
        "like a 4\" - if core type is 1, that's stress, not a new identity).", ss["GBody"]))
    arows = [row_of(["Type", "Growth (Integration) →", "Stress (Disintegration) →"], ss, header=True)]
    for t in range(1, 10):
        g, d = INTEGRATION_ARROW[t], DISINTEGRATION_ARROW[t]
        arows.append(row_of([f"{t} {TYPE_NAMES[t]}", f"{g} {TYPE_NAMES[g]}", f"{d} {TYPE_NAMES[d]}"], ss))
    atbl = Table(arows, colWidths=[1.6 * inch, 2.45 * inch, 2.45 * inch], repeatRows=1)
    atbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(atbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Core Type vs. Wing vs. Arrows - the distinction", ss["GSub"]))
    story.append(Paragraph(
        "<b>Core Type</b> is the fixed, lifelong motivational pattern (the fear/desire pair) - it "
        "does not change. <b>Wing</b> is a fixed, secondary flavor from one of the two adjacent "
        "types - also stable over time, just a seasoning on the core pattern. <b>Integration "
        "(Growth) direction</b> and <b>Disintegration (Stress) direction</b> are fixed target types "
        "whose <i>behaviors</i> get borrowed situationally - under security/growth, or under "
        "pressure - without the person's core type or wing ever changing.", ss["GBody"]))
    story.append(Paragraph(
        "<b>Worked example - a 4w5:</b> Core Type 4 (The Individualist) means the fear of having no "
        "identity/significance and the desire to find and express a unique self drive everything. "
        "Wing 5 colors that Four pattern with a more withdrawn, private, intellectualized flavor "
        "than a 4w3 would have (a 4w3 would lean more image-conscious and ambitious). This person's "
        f"fixed arrows are {INTEGRATION_ARROW[4]} (growth) and {DISINTEGRATION_ARROW[4]} (stress).",
        ss["GBody"]))
    story.append(Paragraph(
        f"Under real security, they may act more like a healthy {INTEGRATION_ARROW[4]} "
        f"({TYPE_NAMES[INTEGRATION_ARROW[4]]}) - more disciplined, objective, able to act on "
        f"feeling rather than be ruled by it. Under real stress, they may act more like an unhealthy "
        f"{DISINTEGRATION_ARROW[4]} ({TYPE_NAMES[DISINTEGRATION_ARROW[4]]}) - clingy, "
        f"approval-seeking, losing track of their own needs in a relationship. They are still, "
        f"throughout, a 4w5 - the core identity and the wing never change.", ss["GBody"]))
    story.append(Paragraph(f"<i>{ARROW_CLARIFICATION}</i>", ss["GSmall"]))
    story.append(Spacer(1, 10))

    story.append(Paragraph(
        "<b>Instinctual Variants</b> - independent of type; describes where attention goes first. "
        "Type + dominant instinct matters more than type alone.", ss["GBody"]))
    irows = [
        row_of(["Self-Preservation (sp)", "Safety, resources, body, routine, comfort"], ss),
        row_of(["Social (so)", "Group belonging, status, community, shared cause"], ss),
        row_of(["Sexual / One-to-One (sx)", "Intensity, chemistry, merging, one key relationship"], ss),
    ]
    itbl = Table([row_of(["Instinct", "Focus"], ss, header=True)] + irows, colWidths=[2.0 * inch, 4.5 * inch])
    itbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(itbl)
    story.append(PageBreak())

    # ---------- Levels of health ----------
    story.append(Paragraph("Levels of Health & Tritype", ss["GTitle"]))
    story.append(Paragraph(
        "Every type has a healthy/average/unhealthy range. The <b>pattern stays constant</b>; what "
        "changes is how rigid and compulsive vs. self-aware and flexible it is. Clinically: not "
        "\"which type\" but \"how stuck in it, right now.\"", ss["GBody"]))
    lrows = [row_of(["Score Range", "Band", "Meaning"], ss, header=True)]
    for low, high, label, desc in LEVEL_BANDS:
        lrows.append(row_of([f"{low}-{high}", label, desc], ss))
    ltbl = Table(lrows, colWidths=[0.8 * inch, 1.6 * inch, 4.1 * inch])
    ltbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(ltbl)
    story.append(Spacer(1, 10))

    story.append(Paragraph("The Traditional Nine Levels (Riso-Hudson)", ss["GSub"]))
    story.append(Paragraph(
        "The assessment's percentage bands above are this tool's own scale. Riso and Hudson's "
        "original framework instead describes nine type-specific levels, grouped the same way "
        "(healthy/average/unhealthy) but measured quite differently:", ss["GBody"]))
    nlrows = [row_of(["Level", "Band", "Name"], ss, header=True)]
    for lvl, band, name in RISO_HUDSON_LEVELS:
        nlrows.append(row_of([str(lvl), band, name], ss))
    nltbl = Table(nlrows, colWidths=[0.6 * inch, 1.1 * inch, 4.8 * inch], repeatRows=1)
    nltbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(nltbl)
    story.append(Spacer(1, 8))
    story.append(Paragraph(f"<i>{FUNCTIONING_VS_LEVELS_NOTE}</i>", ss["GSmall"]))

    story.append(PageBreak())

    story.append(Paragraph("Tritype / Trifix", ss["GTitle"]))
    story.append(Paragraph(
        "<b>Tritype</b> - the highest-scoring type within each of the three centers, taken together, "
        "written as three numbers (e.g. 4-6-8). Gives a fuller picture than primary type alone (a "
        "4w5 with 1/9 support behaves differently than a 4w5 with 8/3 support). The <b>trifix</b> is "
        "the same three numbers with their dominant instinct attached per fix in more advanced "
        "tritype theory - an extension on top of the base tritype, and less universally agreed-upon "
        "than the core nine types themselves.", ss["GBody"]))

    story.append(Paragraph("How It All Fits Together", ss["GSub"]))
    story.append(Paragraph(
        "A complete profile layers: <b>Core Type</b> (the fear/desire engine) → <b>Wing</b> (flavor) "
        "→ <b>Arrows</b> (situational borrowed behavior) → <b>Center of Intelligence</b> + "
        "<b>Harmonic Triad</b> + <b>Hornevian Group</b> (three independent coping/style lenses on the "
        "same core type) → <b>Instinctual Stacking</b> (where attention goes first, second, least) → "
        "<b>Tritype</b> (the fuller 3-center picture) → <b>Level of Development</b> (how rigidly or "
        "freely all of the above is currently being lived out).", ss["GBody"]))
    story.append(Paragraph(
        "<b>Integrated example:</b> A client scores primary Type 6 (Loyalist), wing 7, tritype "
        "6-3-9, instinct stack sp/so/sx, functioning score 55% (Average). Reading this together: "
        "core motivation is security/support (6); the 7-wing adds restlessness and a search for "
        "options rather than pure caution (6w7, vs. a more serious 6w5); Head Center + Competency "
        "harmonic (problem-solves rather than melting down) + Compliant hornevian (works within "
        "systems/duty rather than pushing back) describes the coping style; sp-dominant means safety "
        "and routine get attention before status (so) or intensity (sx); the 3 and 9 fixes add "
        "achievement-pressure and conflict-avoidance threads alongside the core anxiety; and Average "
        "functioning suggests the ordinary mix of flexibility and defensiveness, not crisis or "
        "mastery. None of this is a diagnosis - it's a shared map for the conversation with the "
        "client.", ss["GBody"]))

    story.append(PageBreak())

    # ---------- Per-type deep pages (2 types per page via side-by-side tables) ----------
    story.append(Paragraph("The Nine Types — Full Reference", ss["GTitle"]))
    for t in range(1, 10):
        p = TYPE_PROFILES[t]
        color_hex = TYPE_COLORS_HEX[t]
        story.append(Paragraph(
            f"Type {t}: {p['name']}", ParagraphStyle(
                name=f"T{t}Title", fontName="Helvetica-Bold", fontSize=12.5,
                textColor=colors.HexColor(color_hex), spaceBefore=12, spaceAfter=3)))
        story.append(Paragraph(f"<i>{p['alt_names']}</i>", ss["GSmall"]))

        rows = [
            ["Core Fear", p["core_fear"]],
            ["Core Desire", p["core_desire"]],
            ["Motivation", p["core_motivation"]],
            ["Healthy", p["healthy"]],
            ["Average", p["average"]],
            ["Unhealthy", p["unhealthy"]],
            ["Under Stress", p["stress_behaviors"]],
            ["Growth →", p["growth_direction"]],
            ["Stress →", p["stress_direction"]],
            ["Clinical Note", p["therapy_notes"]],
            ["Ask", " / ".join(p["questions_to_explore"][:2])],
        ]
        body_rows = [[Paragraph(f"<b>{k}</b>", ss["GCellBold"]), Paragraph(v, ss["GCell"])] for k, v in rows]
        ttbl = Table(body_rows, colWidths=[0.95 * inch, 5.45 * inch])
        ttbl.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
            ("BACKGROUND", (0, 0), (0, -1), BG_PANEL),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("TOPPADDING", (0, 0), (-1, -1), 3.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(ttbl)
        if t != 9:
            story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ---------- Reading the clinical report ----------
    story.append(Paragraph("Reading the Clinical Report", ss["GTitle"]))
    report_notes = [
        ("Clinical Summary table", "Primary type, wing, tritype, dominant instinct, growth/stress arrows. Read this first for orientation."),
        ("Radar + ranked bar chart", "Shows relative strength across all 9. A flat radar (close scores) = ambiguous profile, worth a follow-up conversation. A sharp spike = high internal consistency."),
        ("Type deep-dive page", "Healthy/average/unhealthy descriptions - use to gauge where on the spectrum the client is now, not just their label."),
        ("Clinical Notes + Questions", "Session starting points, written to open the defense mechanism directly."),
        ("Instinct chart", "Cross-reference with type - often explains why a client doesn't match the textbook picture of their type."),
        ("Functioning gauge", "A general self-report wellbeing indicator, not part of the Enneagram model itself - a mood/capacity check, not a diagnosis."),
        ("Appendices (full Q&A)", "Go here when a score surprises you - rereading specific high/low-rated statements often explains the aggregate number."),
    ]
    rrows = [row_of(["Section", "How to use it"], ss, header=True)] + \
            [row_of([k, v], ss) for k, v in report_notes]
    rtbl = Table(rrows, colWidths=[1.7 * inch, 4.8 * inch], repeatRows=1)
    rtbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE_GRAY),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, BG_PANEL]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(rtbl)
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "<b>Caution:</b> the instrument estimates a self-reported pattern, not a verified type. "
        "Treat the primary type as a strong hypothesis to explore with the client, not a verdict - "
        "especially when scores are close or the client is early in self-awareness.", ss["GBody"]))

    story.append(PageBreak())

    # ---------- References ----------
    story.append(Paragraph("References & Source Notes", ss["GTitle"]))
    story.append(Paragraph(
        "This guide distinguishes three layers: (1) foundational Enneagram theory shared across "
        "schools (nine types, core fear/desire, centers); (2) concepts specific to the Riso-Hudson "
        "lineage (Harmonic/Hornevian triads, the Nine Levels of Development, arrows terminology); "
        "and (3) this tool's own original scoring instrument, which is not independently validated "
        "research. Nothing here should be read as a clinically validated diagnostic finding.",
        ss["GBody"]))
    refs = [
        "The Enneagram Institute - \"The Levels of Development\" (enneagraminstitute.com) - "
        "primary reference for the traditional Nine Levels and their healthy/average/unhealthy bands.",
        "Don Riso & Russ Hudson, \"Personality Types\" and \"The Wisdom of the Enneagram\" - "
        "foundational texts for Levels of Development, Harmonic Triads, and arrows terminology as "
        "used in this guide.",
        "Truity - \"What are Enneagram Harmonic Groups?\" (truity.com/blog) - plain-language summary "
        "of the Harmonic Triads consistent with the Enneagram Institute's framing.",
        "Karen Horney's \"moving toward / against / away\" model, later aligned to the Enneagram by "
        "Riso and Hudson as the Hornevian Groups (Horney herself did not describe this mapping).",
    ]
    for r in refs:
        story.append(Paragraph(f"• {r}", ss["GSmall"]))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<i>Note on reliability: published research on Enneagram assessment instruments generally "
        "shows weaker psychometric validation than established trait models (e.g. the Five-Factor "
        "Model). Treat any Enneagram-based report, including this tool's, as a structured "
        "self-report conversation aid rather than a validated psychological measure.</i>", ss["GSmall"]))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    buf.seek(0)
    return buf.getvalue()


if __name__ == "__main__":
    pdf = build()
    out_path = "Enneagram_Study_Guide.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf)
    print(f"Wrote {len(pdf)} bytes to {out_path}")
