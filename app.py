import random
import uuid
import streamlit as st

from enneagram.questions import (
    TYPE_ITEMS, INSTINCT_ITEMS, FUNCTIONING_ITEMS, TYPE_NAMES,
)
from enneagram.scoring import score_types, score_instincts, score_functioning, band_for_score
from enneagram.content import TYPE_PROFILES, LEVEL_BANDS
from enneagram.report import generate_pdf_report, TYPE_COLORS_HEX
from enneagram.report_intervention import generate_intervention_pdf
from enneagram.groq_utils import generate_intervention_content
from enneagram.email_utils import send_report_email, send_intervention_email, THERAPIST_EMAIL
from enneagram.persistence import save_session, load_session, delete_session

st.set_page_config(
    page_title="Enneagram Clinical Assessment",
    page_icon="🜸",
    layout="centered",
    initial_sidebar_state="collapsed",
)

LIKERT_OPTIONS = {
    1: "Not at all like me",
    2: "A little like me",
    3: "Somewhat like me",
    4: "Mostly like me",
    5: "Very much like me",
}
FUNC_LIKERT_OPTIONS = {
    1: "Never / Not true",
    2: "Rarely",
    3: "Sometimes",
    4: "Often",
    5: "Almost always / Very true",
}

TYPE_PAGE_SIZE = 18
INSTINCT_PAGE_SIZE = 27
FUNCTIONING_PAGE_SIZE = 15

# ---------------------------------------------------------------------------
# Premium / clinical styling
# ---------------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

.block-container { padding-top: 2.2rem; max-width: 760px; }

h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1B2A4A !important; }

.brand-kicker {
    letter-spacing: 3px; font-size: 0.78rem; font-weight: 600;
    color: #B8975A; text-transform: uppercase; margin-bottom: 0.2rem;
}
.brand-title {
    font-family: 'Playfair Display', serif; font-weight: 700;
    font-size: 2.1rem; color: #1B2A4A; margin-top: 0; margin-bottom: 0.3rem;
}
.brand-sub { color: #4A5568; font-size: 0.98rem; margin-bottom: 1.4rem; }

hr.gold { border: none; border-top: 1.5px solid #B8975A; width: 56px; margin: 0.4rem 0 1.4rem 0; }

.card {
    background: #FFFFFF; border: 1px solid #E3E6EC; border-radius: 10px;
    padding: 1.4rem 1.5rem; margin-bottom: 1.1rem;
    box-shadow: 0 1px 3px rgba(27,42,74,0.04);
}
.q-counter {
    font-size: 0.75rem; color: #B8975A; font-weight: 600; letter-spacing: 1px;
    text-transform: uppercase; margin-bottom: 0.2rem;
}
.q-text { font-size: 1.02rem; color: #1F2430; font-weight: 500; margin-bottom: 0.5rem; }

.progress-wrap { margin: 0.6rem 0 1.6rem 0; }

div[data-testid="stRadio"] label { font-size: 0.92rem; }

.stButton > button {
    background-color: #1B2A4A; color: white; border-radius: 6px;
    padding: 0.55rem 1.6rem; font-weight: 600; border: none;
}
.stButton > button:hover { background-color: #2C3E60; color: white; }

.footer-note { color: #8A94A6; font-size: 0.78rem; text-align: center; margin-top: 2.4rem; }

.summary-pill {
    display: inline-block; background: #1B2A4A; color: white; font-weight: 600;
    padding: 6px 16px; border-radius: 20px; font-size: 0.95rem; margin-bottom: 0.6rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def header(kicker, title, sub=None):
    st.markdown(f'<div class="brand-kicker">{kicker}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="brand-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="brand-sub">{sub}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="gold">', unsafe_allow_html=True)


def _get_or_create_token():
    params = st.query_params
    token = params.get("sid")
    if not token:
        token = uuid.uuid4().hex
        st.query_params["sid"] = token
    return token


def init_state():
    ss = st.session_state

    if "sid" not in ss:
        ss["sid"] = _get_or_create_token()

    # A fresh session_state (e.g. after a refresh or a dropped connection)
    # won't have "_restored" set yet - try to recover progress from disk
    # using the token that's still sitting in the browser's URL.
    if not ss.get("_restored"):
        ss["_restored"] = True
        saved = load_session(ss["sid"])
        if saved:
            for k, v in saved.items():
                ss[k] = v
            # Pre-seed the individual widget keys too, so the radio buttons
            # themselves render with the client's prior answers already
            # selected, not just our bookkeeping dicts.
            for idx, val in saved.get("type_answers", {}).items():
                ss[f"type_{idx}"] = val
            for idx, val in saved.get("instinct_answers", {}).items():
                ss[f"inst_{idx}"] = val
            for idx, val in saved.get("functioning_answers", {}).items():
                ss[f"func_{idx}"] = val

    ss.setdefault("stage", "intro")
    ss.setdefault("client_name", "")
    ss.setdefault("client_notes", "")
    ss.setdefault("type_answers", {})
    ss.setdefault("instinct_answers", {})
    ss.setdefault("functioning_answers", {})
    ss.setdefault("type_page", 0)
    ss.setdefault("instinct_page", 0)
    ss.setdefault("functioning_page", 0)
    if "type_order" not in ss:
        order = list(range(len(TYPE_ITEMS)))
        random.Random(42).shuffle(order)
        ss["type_order"] = order
    if "instinct_order" not in ss:
        order = list(range(len(INSTINCT_ITEMS)))
        random.Random(7).shuffle(order)
        ss["instinct_order"] = order


def persist_progress():
    try:
        save_session(st.session_state["sid"], st.session_state)
    except Exception:
        pass  # a save hiccup should never block the assessment itself


def progress_bar(current, total, label):
    pct = current / total if total else 0
    st.progress(min(pct, 1.0), text=label)


def intro_page():
    header("Confidential Clinical Tool", "Enneagram Assessment",
           "A structured self-report instrument designed to support therapeutic "
           "exploration of personality pattern, motivation, and growth path.")
    st.markdown(
        '<div class="card">'
        '<p style="margin:0 0 .6rem 0;">This assessment includes three parts:</p>'
        '<ol style="margin:0 0 .8rem 1.1rem; padding:0; color:#1F2430;">'
        '<li>108 statements about your core personality pattern (Enneagram type)</li>'
        '<li>27 statements about your instinctual focus (self-preservation / social / one-to-one)</li>'
        '<li>15 statements about your current overall functioning</li>'
        '</ol>'
        '<p style="margin:0; color:#4A5568; font-size:0.9rem;">'
        'Answer honestly and quickly, based on your general tendencies rather than how you '
        'wish to be or how you act in just one context. There are no right or wrong answers. '
        f'Your results will be compiled into a confidential clinical report and sent only to '
        f'your therapist&rsquo;s secure inbox.</p>'
        '<p style="margin:0.6rem 0 0 0; color:#8A94A6; font-size:0.82rem;">'
        'Your progress saves automatically as you go — it&rsquo;s safe to refresh the page, '
        'go back, or reconnect without losing your answers, as long as you use the same link/tab.</p>'
        '</div>', unsafe_allow_html=True)

    with st.form("client_info_form"):
        name = st.text_input("Client name (or identifier) — optional, shown only in the report")
        notes = st.text_area("Any context your therapist should know before you begin? (optional)", height=80)
        consent = st.checkbox(
            "I understand this is a self-report tool to support therapy, not a medical or "
            "psychiatric diagnosis, and I consent to my responses being compiled into a report "
            "for my therapist.")
        submitted = st.form_submit_button("Begin Assessment →")
    if submitted:
        if not consent:
            st.error("Please confirm the consent checkbox to continue.")
        else:
            st.session_state["client_name"] = name
            st.session_state["client_notes"] = notes
            st.session_state["stage"] = "type"
            st.rerun()


def likert_block(item_text, counter_label, key, options):
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f'<div class="q-counter">{counter_label}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="q-text">{item_text}</div>', unsafe_allow_html=True)
    val = st.radio(
        label="", options=list(options.keys()),
        format_func=lambda k: f"{k} — {options[k]}",
        key=key, horizontal=True, index=None,
        label_visibility="collapsed",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return val


def type_page():
    order = st.session_state["type_order"]
    page = st.session_state["type_page"]
    total_pages = -(-len(order) // TYPE_PAGE_SIZE)
    start = page * TYPE_PAGE_SIZE
    chunk = order[start:start + TYPE_PAGE_SIZE]

    header("Part 1 of 3", "Core Personality Pattern",
           "Rate how much each statement sounds like you in general.")
    progress_bar(start, len(order), f"Part 1 · {start}/{len(order)} statements")

    answers = st.session_state["type_answers"]
    for i, idx in enumerate(chunk):
        _, text = TYPE_ITEMS[idx]
        val = likert_block(text, f"Statement {start + i + 1} of {len(order)}", f"type_{idx}", LIKERT_OPTIONS)
        if val is not None:
            answers[idx] = val

    cols = st.columns([1, 1])
    with cols[0]:
        if page > 0 and st.button("← Back"):
            st.session_state["type_page"] -= 1
            st.rerun()
    with cols[1]:
        all_answered = all(idx in answers for idx in chunk)
        label = "Continue →" if page < total_pages - 1 else "Continue to Part 2 →"
        if st.button(label, disabled=not all_answered, type="primary"):
            if page < total_pages - 1:
                st.session_state["type_page"] += 1
            else:
                st.session_state["stage"] = "instinct"
            st.rerun()
        if not all_answered:
            st.caption("Please answer every statement on this page to continue.")


def instinct_page():
    order = st.session_state["instinct_order"]
    header("Part 2 of 3", "Instinctual Focus",
           "Rate how much each statement sounds like you in general.")
    progress_bar(0, 1, "Part 2 · Instinctual focus")

    answers = st.session_state["instinct_answers"]
    for i, idx in enumerate(order):
        _, text = INSTINCT_ITEMS[idx]
        val = likert_block(text, f"Statement {i + 1} of {len(order)}", f"inst_{idx}", LIKERT_OPTIONS)
        if val is not None:
            answers[idx] = val

    cols = st.columns([1, 1])
    with cols[0]:
        if st.button("← Back"):
            st.session_state["stage"] = "type"
            st.session_state["type_page"] = max(0, -(-len(st.session_state["type_order"]) // TYPE_PAGE_SIZE) - 1)
            st.rerun()
    with cols[1]:
        all_answered = all(idx in answers for idx in order)
        if st.button("Continue to Part 3 →", disabled=not all_answered, type="primary"):
            st.session_state["stage"] = "functioning"
            st.rerun()
        if not all_answered:
            st.caption("Please answer every statement to continue.")


def functioning_page():
    header("Part 3 of 3", "Current Functioning",
           "Rate how often each statement is true for you right now.")
    progress_bar(0, 1, "Part 3 · Current functioning")

    answers = st.session_state["functioning_answers"]
    for i, text in enumerate(FUNCTIONING_ITEMS):
        val = likert_block(text, f"Statement {i + 1} of {len(FUNCTIONING_ITEMS)}", f"func_{i}", FUNC_LIKERT_OPTIONS)
        if val is not None:
            answers[i] = val

    cols = st.columns([1, 1])
    with cols[0]:
        if st.button("← Back"):
            st.session_state["stage"] = "instinct"
            st.rerun()
    with cols[1]:
        all_answered = len(answers) == len(FUNCTIONING_ITEMS)
        if st.button("See Results →", disabled=not all_answered, type="primary"):
            st.session_state["stage"] = "results"
            st.rerun()
        if not all_answered:
            st.caption("Please answer every statement to continue.")


def results_page():
    header("Results", "Your Clinical Profile Summary",
           "This on-screen summary is a starting point for discussion with your therapist. "
           "A complete report has been prepared below.")

    type_result = score_types(st.session_state["type_answers"])
    instinct_result = score_instincts(st.session_state["instinct_answers"])
    functioning_score = score_functioning(st.session_state["functioning_answers"])

    primary = type_result["primary_type"]
    wing = type_result["wing"]
    prof = TYPE_PROFILES[primary]

    st.markdown(
        f'<div class="summary-pill">Primary Type {primary} · {prof["name"]} '
        f'&nbsp;(Wing {wing})</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"**Core fear:** {prof['core_fear']}")
    st.markdown(f"**Core desire:** {prof['core_desire']}")
    st.markdown(f"**Basic pattern:** {prof['basic_pattern']}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("Type Scores")
    chart_data = {TYPE_NAMES[t]: v for t, v in sorted(type_result["normalized"].items())}
    st.bar_chart(chart_data)

    band_label, band_desc = band_for_score(functioning_score, LEVEL_BANDS)
    st.subheader("Overall Functioning Indicator")
    st.metric("Functioning score", f"{functioning_score:.0f}%", band_label)
    st.caption(band_desc)

    st.subheader("Instinctual Stack")
    for inst, val in instinct_result["stack"]:
        st.write(f"**{inst.upper()}** — {val:.0f}%")

    st.divider()
    st.markdown("#### Report 1 — Client Assessment Report")
    st.caption(
        f"The complete PDF report — including all charts, clinical notes, growth/stress "
        f"pathways, and the full item-by-item question/answer transcript — will be emailed "
        f"only to the practitioner's secure inbox ({THERAPIST_EMAIL}). It is never sent to the client.")

    if st.button("Generate PDF Report", type="primary"):
        with st.spinner("Building report…"):
            pdf_bytes = generate_pdf_report(
                client_info={"name": st.session_state["client_name"]},
                type_result=type_result,
                instinct_result=instinct_result,
                functioning_score=functioning_score,
                type_answers=st.session_state["type_answers"],
                instinct_answers=st.session_state["instinct_answers"],
                functioning_answers=st.session_state["functioning_answers"],
            )
        st.session_state["pdf_bytes"] = pdf_bytes
        st.success("Client report generated.")

    if st.session_state.get("pdf_bytes"):
        st.download_button(
            "Download Client Report PDF", data=st.session_state["pdf_bytes"],
            file_name=f"Enneagram_Report_{st.session_state['client_name'] or 'client'}.pdf",
            mime="application/pdf",
        )

    st.divider()
    st.markdown("#### Report 2 — Intervention & Session Planning Report (Practitioner Only)")
    st.caption(
        "Confidential, practitioner-only material: psychological formulation, strengths, "
        "development areas, session questions, discussion topics, choice-based scenarios, "
        "suggested interventions, and a session roadmap — personalized from this client's "
        "actual results via Groq. Never intended for the client."
    )

    groq_key = st.secrets.get("GROQ_API_KEY", "")
    groq_model = st.secrets.get("GROQ_MODEL", "")
    if st.button("Generate Intervention Report"):
        if not groq_key:
            st.error(
                "GROQ_API_KEY is not configured. Get a free key at "
                "https://console.groq.com/keys (sign up, then 'Create API Key') and add it "
                "to Streamlit secrets as GROQ_API_KEY."
            )
        else:
            try:
                with st.spinner("Generating personalized intervention content…"):
                    ai_content = generate_intervention_content(
                        client_name=st.session_state["client_name"],
                        type_result=type_result,
                        instinct_result=instinct_result,
                        functioning_score=functioning_score,
                        type_answers=st.session_state["type_answers"],
                        instinct_answers=st.session_state["instinct_answers"],
                        api_key=groq_key,
                        model=groq_model or None,
                    )
                    intervention_pdf = generate_intervention_pdf(
                        client_info={"name": st.session_state["client_name"]},
                        type_result=type_result,
                        instinct_result=instinct_result,
                        functioning_score=functioning_score,
                        ai_content=ai_content,
                    )
                st.session_state["intervention_pdf_bytes"] = intervention_pdf
                st.success("Intervention report generated.")
            except Exception as e:
                st.error(f"Could not generate intervention report: {e}")

    if st.session_state.get("intervention_pdf_bytes"):
        st.download_button(
            "Download Intervention Report PDF", data=st.session_state["intervention_pdf_bytes"],
            file_name=f"Enneagram_Intervention_Report_{st.session_state['client_name'] or 'client'}.pdf",
            mime="application/pdf",
        )

    st.divider()
    st.markdown("#### Email Reports to Practitioner")
    if st.session_state.get("pdf_bytes"):
        api_key = st.secrets.get("RESEND_API_KEY", "")
        from_addr = st.secrets.get("RESEND_FROM_ADDRESS", "")
        if not st.session_state.get("intervention_pdf_bytes"):
            st.caption("Only the client report has been generated — it will be sent alone. "
                       "Generate the intervention report above first if you want both sent together.")
        if st.button("Email Report(s) to Practitioner"):
            if not api_key or not from_addr:
                st.error("Email is not configured yet. Add RESEND_API_KEY and RESEND_FROM_ADDRESS to secrets.")
            else:
                try:
                    with st.spinner("Sending email…"):
                        send_report_email(api_key, st.session_state["pdf_bytes"],
                                           st.session_state["client_name"], from_addr)
                        if st.session_state.get("intervention_pdf_bytes"):
                            send_intervention_email(
                                api_key, st.session_state["intervention_pdf_bytes"],
                                st.session_state["client_name"], from_addr)
                    st.success(f"Report(s) emailed to {THERAPIST_EMAIL}.")
                    delete_session(st.session_state["sid"])
                except Exception as e:
                    st.error(f"Could not send email: {e}")
    else:
        st.caption("Generate the client report above first.")

    st.markdown('<div class="footer-note">Confidential — for use between client and practitioner only.</div>',
                unsafe_allow_html=True)


def access_gate():
    """If APP_ACCESS_CODE is set in secrets, require it before showing the app."""
    required_code = st.secrets.get("APP_ACCESS_CODE", "")
    if not required_code:
        return True
    if st.session_state.get("authed"):
        return True

    header("Private Access", "Enneagram Clinical Assessment",
           "This assessment link is restricted. Please enter the access code "
           "provided by your therapist to continue.")
    with st.form("access_form"):
        code = st.text_input("Access code", type="password")
        submitted = st.form_submit_button("Enter →")
    if submitted:
        if code == required_code:
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error("Incorrect access code.")
    return False


def main():
    init_state()
    if not access_gate():
        persist_progress()
        return
    stage = st.session_state["stage"]
    if stage == "intro":
        intro_page()
    elif stage == "type":
        type_page()
    elif stage == "instinct":
        instinct_page()
    elif stage == "functioning":
        functioning_page()
    elif stage == "results":
        results_page()
    persist_progress()


if __name__ == "__main__":
    main()
