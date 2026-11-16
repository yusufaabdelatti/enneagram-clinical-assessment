import random
import uuid
import streamlit as st

from enneagram.questions import (
    TYPE_ITEMS, INSTINCT_ITEMS, FUNCTIONING_ITEMS, TYPE_NAMES,
)
from enneagram.questions_ar import (
    TYPE_ITEMS_AR, INSTINCT_ITEMS_AR, FUNCTIONING_ITEMS_AR, TYPE_NAMES_AR,
    LIKERT_OPTIONS_AR, FUNC_LIKERT_OPTIONS_AR,
)
from enneagram.i18n import t
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

LIKERT_OPTIONS_EN = {
    1: "Not at all like me",
    2: "A little like me",
    3: "Somewhat like me",
    4: "Mostly like me",
    5: "Very much like me",
}
FUNC_LIKERT_OPTIONS_EN = {
    1: "Never / Not true",
    2: "Rarely",
    3: "Sometimes",
    4: "Often",
    5: "Almost always / Very true",
}

TYPE_PAGE_SIZE = 18
INSTINCT_PAGE_SIZE = 27
FUNCTIONING_PAGE_SIZE = 15


def L():
    return st.session_state.get("lang", "en")


def likert_options():
    return LIKERT_OPTIONS_AR if L() == "ar" else LIKERT_OPTIONS_EN


def func_likert_options():
    return FUNC_LIKERT_OPTIONS_AR if L() == "ar" else FUNC_LIKERT_OPTIONS_EN


def type_item_text(idx):
    return TYPE_ITEMS_AR[idx] if L() == "ar" else TYPE_ITEMS[idx][1]


def instinct_item_text(idx):
    return INSTINCT_ITEMS_AR[idx] if L() == "ar" else INSTINCT_ITEMS[idx][1]


def functioning_item_text(idx):
    return FUNCTIONING_ITEMS_AR[idx] if L() == "ar" else FUNCTIONING_ITEMS[idx]


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

RTL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stMarkdown, .stRadio, .stTextInput, .stTextArea,
p, span, div, label {
    font-family: 'Cairo', 'Inter', sans-serif !important;
}
.block-container { direction: rtl; text-align: right; }
.brand-kicker, .brand-title, .brand-sub, .q-counter, .q-text, .footer-note { text-align: right; }
div[data-testid="stRadio"] > div { flex-direction: row-reverse; justify-content: flex-end; }
div[data-testid="stForm"] label, .stTextInput label, .stTextArea label, .stCheckbox label { text-align: right; }
.stProgress { direction: ltr; }
</style>
"""


def inject_rtl_if_needed():
    if L() == "ar":
        st.markdown(RTL_CSS, unsafe_allow_html=True)


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
    ss.setdefault("lang", "en")
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


def language_toggle():
    options = ["English", "العربية"]
    current = 0 if L() == "en" else 1
    choice = st.radio(t("lang_label", L()), options, index=current, horizontal=True, key="lang_radio")
    new_lang = "en" if choice == "English" else "ar"
    if new_lang != st.session_state.get("lang"):
        st.session_state["lang"] = new_lang
        st.rerun()


def intro_page():
    language_toggle()
    inject_rtl_if_needed()
    lang = L()
    header(t("intro_kicker", lang), t("intro_title", lang), t("intro_sub", lang))

    st.markdown(
        f'<div class="card">'
        f'<p style="margin:0 0 .6rem 0;">{t("intro_card_intro", lang)}</p>'
        f'<ol style="margin:0 0 .8rem 1.1rem; padding:0; color:#1F2430;">'
        f'<li>{t("intro_li_1", lang)}</li>'
        f'<li>{t("intro_li_2", lang)}</li>'
        f'<li>{t("intro_li_3", lang)}</li>'
        f'</ol>'
        f'<p style="margin:0; color:#4A5568; font-size:0.9rem;">{t("intro_card_outro", lang)}</p>'
        f'<p style="margin:0.6rem 0 0 0; color:#8A94A6; font-size:0.82rem;">{t("intro_autosave_note", lang)}</p>'
        f'</div>', unsafe_allow_html=True)

    with st.form("client_info_form"):
        name = st.text_input(t("name_label", lang))
        notes = st.text_area(t("notes_label", lang), height=80)
        consent = st.checkbox(t("consent_label", lang))
        submitted = st.form_submit_button(t("begin_button", lang))
    if submitted:
        if not consent:
            st.error(t("consent_error", lang))
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
    inject_rtl_if_needed()
    lang = L()
    order = st.session_state["type_order"]
    page = st.session_state["type_page"]
    total_pages = -(-len(order) // TYPE_PAGE_SIZE)
    start = page * TYPE_PAGE_SIZE
    chunk = order[start:start + TYPE_PAGE_SIZE]

    header(t("part1_kicker", lang), t("part1_title", lang), t("part1_sub", lang))
    progress_bar(start, len(order), f"{t('part1_kicker', lang)} · {start}/{len(order)}")

    answers = st.session_state["type_answers"]
    opts = likert_options()
    for i, idx in enumerate(chunk):
        text = type_item_text(idx)
        counter = f"{t('statement_label', lang)} {start + i + 1} {t('of', lang)} {len(order)}"
        val = likert_block(text, counter, f"type_{idx}", opts)
        if val is not None:
            answers[idx] = val

    cols = st.columns([1, 1])
    with cols[0]:
        if page > 0 and st.button(t("back_button", lang)):
            st.session_state["type_page"] -= 1
            st.rerun()
    with cols[1]:
        all_answered = all(idx in answers for idx in chunk)
        label = t("continue_button", lang) if page < total_pages - 1 else t("continue_part2", lang)
        if st.button(label, disabled=not all_answered, type="primary"):
            if page < total_pages - 1:
                st.session_state["type_page"] += 1
            else:
                st.session_state["stage"] = "instinct"
            st.rerun()
        if not all_answered:
            st.caption(t("answer_all_caption", lang))


def instinct_page():
    inject_rtl_if_needed()
    lang = L()
    order = st.session_state["instinct_order"]
    header(t("part2_kicker", lang), t("part2_title", lang), t("part1_sub", lang))
    progress_bar(0, 1, t("part2_kicker", lang))

    answers = st.session_state["instinct_answers"]
    opts = likert_options()
    for i, idx in enumerate(order):
        text = instinct_item_text(idx)
        counter = f"{t('statement_label', lang)} {i + 1} {t('of', lang)} {len(order)}"
        val = likert_block(text, counter, f"inst_{idx}", opts)
        if val is not None:
            answers[idx] = val

    cols = st.columns([1, 1])
    with cols[0]:
        if st.button(t("back_button", lang)):
            st.session_state["stage"] = "type"
            st.session_state["type_page"] = max(0, -(-len(st.session_state["type_order"]) // TYPE_PAGE_SIZE) - 1)
            st.rerun()
    with cols[1]:
        all_answered = all(idx in answers for idx in order)
        if st.button(t("continue_part3", lang), disabled=not all_answered, type="primary"):
            st.session_state["stage"] = "functioning"
            st.rerun()
        if not all_answered:
            st.caption(t("answer_all_caption_single", lang))


def functioning_page():
    inject_rtl_if_needed()
    lang = L()
    header(t("part3_kicker", lang), t("part3_title", lang), t("part3_sub", lang))
    progress_bar(0, 1, t("part3_kicker", lang))

    answers = st.session_state["functioning_answers"]
    opts = func_likert_options()
    for i in range(len(FUNCTIONING_ITEMS)):
        text = functioning_item_text(i)
        counter = f"{t('statement_label', lang)} {i + 1} {t('of', lang)} {len(FUNCTIONING_ITEMS)}"
        val = likert_block(text, counter, f"func_{i}", opts)
        if val is not None:
            answers[i] = val

    cols = st.columns([1, 1])
    with cols[0]:
        if st.button(t("back_button", lang)):
            st.session_state["stage"] = "instinct"
            st.rerun()
    with cols[1]:
        all_answered = len(answers) == len(FUNCTIONING_ITEMS)
        if st.button(t("see_results_button", lang), disabled=not all_answered, type="primary"):
            st.session_state["stage"] = "results"
            st.rerun()
        if not all_answered:
            st.caption(t("answer_all_caption_single", lang))


def results_page():
    inject_rtl_if_needed()
    lang = L()
    header(t("results_kicker", lang), t("results_title", lang), t("results_sub", lang))

    type_result = score_types(st.session_state["type_answers"])
    instinct_result = score_instincts(st.session_state["instinct_answers"])
    functioning_score = score_functioning(st.session_state["functioning_answers"])

    primary = type_result["primary_type"]
    wing = type_result["wing"]
    prof = TYPE_PROFILES[primary]
    name_display = f'{prof["name"]} ({TYPE_NAMES_AR[primary]})' if lang == "ar" else prof["name"]

    st.markdown(
        f'<div class="summary-pill">Primary Type {primary} · {name_display} '
        f'&nbsp;(Wing {wing})</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown(f"**{t('core_fear_label', lang)}:** {prof['core_fear']}")
    st.markdown(f"**{t('core_desire_label', lang)}:** {prof['core_desire']}")
    st.markdown(f"**{t('basic_pattern_label', lang)}:** {prof['basic_pattern']}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader(t("type_scores_header", lang))
    chart_data = {TYPE_NAMES[t_]: v for t_, v in sorted(type_result["normalized"].items())}
    st.bar_chart(chart_data)

    band_label, band_desc = band_for_score(functioning_score, LEVEL_BANDS)
    st.subheader(t("functioning_header", lang))
    st.metric(t("functioning_metric_label", lang), f"{functioning_score:.0f}%", band_label)
    st.caption(band_desc)

    st.subheader(t("instinct_stack_header", lang))
    for inst, val in instinct_result["stack"]:
        st.write(f"**{inst.upper()}** — {val:.0f}%")

    st.divider()
    st.markdown(f"#### {t('report1_header', lang)}")
    st.caption(
        f"The complete PDF report — including all charts, clinical notes, growth/stress "
        f"pathways, and the full item-by-item question/answer transcript — will be emailed "
        f"only to the practitioner's secure inbox ({THERAPIST_EMAIL}). It is never sent to the client.")

    if st.button(t("generate_pdf_button", lang), type="primary"):
        with st.spinner("Building report…"):
            pdf_bytes = generate_pdf_report(
                client_info={"name": st.session_state["client_name"]},
                type_result=type_result,
                instinct_result=instinct_result,
                functioning_score=functioning_score,
                type_answers=st.session_state["type_answers"],
                instinct_answers=st.session_state["instinct_answers"],
                functioning_answers=st.session_state["functioning_answers"],
                answer_language=lang,
            )
        st.session_state["pdf_bytes"] = pdf_bytes
        st.success("Client report generated.")

    if st.session_state.get("pdf_bytes"):
        st.download_button(
            t("download_client_pdf", lang), data=st.session_state["pdf_bytes"],
            file_name=f"Enneagram_Report_{st.session_state['client_name'] or 'client'}.pdf",
            mime="application/pdf",
        )

    st.divider()
    st.markdown(f"#### {t('report2_header', lang)}")
    st.caption(
        "Confidential, practitioner-only material: psychological formulation, strengths, "
        "development areas, session questions, discussion topics, choice-based scenarios, "
        "suggested interventions, and a session roadmap — personalized from this client's "
        "actual results via Groq. Never intended for the client. Always generated in English."
    )

    groq_key = st.secrets.get("GROQ_API_KEY", "")
    groq_model = st.secrets.get("GROQ_MODEL", "")
    if st.button(t("generate_intervention_button", lang)):
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
            t("download_intervention_pdf", lang), data=st.session_state["intervention_pdf_bytes"],
            file_name=f"Enneagram_Intervention_Report_{st.session_state['client_name'] or 'client'}.pdf",
            mime="application/pdf",
        )

    st.divider()
    st.markdown(f"#### {t('email_header', lang)}")
    if st.session_state.get("pdf_bytes"):
        api_key = st.secrets.get("RESEND_API_KEY", "")
        from_addr = st.secrets.get("RESEND_FROM_ADDRESS", "")
        if not st.session_state.get("intervention_pdf_bytes"):
            st.caption("Only the client report has been generated — it will be sent alone. "
                       "Generate the intervention report above first if you want both sent together.")
        if st.button(t("email_button", lang)):
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

    st.markdown(f'<div class="footer-note">{t("footer_note", lang)}</div>', unsafe_allow_html=True)


def access_gate():
    """If APP_ACCESS_CODE is set in secrets, require it before showing the app."""
    required_code = st.secrets.get("APP_ACCESS_CODE", "")
    if not required_code:
        return True
    if st.session_state.get("authed"):
        return True

    lang = L()
    inject_rtl_if_needed()
    header(t("access_kicker", lang), t("access_title", lang), t("access_sub", lang))
    with st.form("access_form"):
        code = st.text_input(t("access_code_label", lang), type="password")
        submitted = st.form_submit_button(t("access_enter_button", lang))
    if submitted:
        if code == required_code:
            st.session_state["authed"] = True
            st.rerun()
        else:
            st.error(t("access_error", lang))
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
