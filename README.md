# Enneagram Clinical Assessment

A self-hosted Streamlit tool for a therapist to administer a 150-item Enneagram
assessment (core type, instinctual variant, and a general functioning indicator),
score it, and generate a premium, clinically-styled PDF report with charts,
explanations, growth/stress pathways, and the full question-by-question
transcript — emailed only to the therapist's own inbox via Resend.

**This is a clinical support tool for use alongside a licensed therapist, not a
stand-alone diagnostic instrument.** All assessment items were written
independently for this project.

## Features
- 108-item core type scale (12 per type), 27-item instinctual variant scale, 15-item functioning scale
- Automatic scoring: primary type, wing, tritype, instinct stack, growth/stress arrows
- On-screen results summary for in-session discussion
- Premium clinical-style PDF report (cover page, radar + bar charts, type deep-dive, full Q&A appendix)
- One-click email delivery of the PDF via [Resend](https://resend.com), sent only to the therapist's address
- No database — nothing is persisted outside of the generated PDF/email

## Local setup
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .streamlit/secrets.toml.example .streamlit/secrets.toml   # then fill in your Resend key
streamlit run app.py
```

## Deploying
1. Push this repo to GitHub (keep `.streamlit/secrets.toml` out of git — it's gitignored).
2. On [share.streamlit.io](https://share.streamlit.io), create a new app pointing at this repo / `app.py`.
3. In the app's **Settings → Secrets**, paste the contents of `secrets.toml.example` with your real values:
   - `RESEND_API_KEY` — from your Resend dashboard
   - `RESEND_FROM_ADDRESS` — a sender verified on your Resend account/domain
4. The report always sends to the address hard-coded in `enneagram/email_utils.py`
   (`THERAPIST_EMAIL`) — update that constant if it ever needs to change.

## Project structure
```
app.py                     Streamlit UI / flow
enneagram/
  questions.py              Item bank (type, instinct, functioning scales)
  scoring.py                Scoring logic
  content.py                Per-type clinical profiles, levels, centers
  report.py                 PDF report generation (reportlab + matplotlib)
  email_utils.py            Resend email delivery
.streamlit/
  config.toml                Theme
  secrets.toml.example       Template for required secrets
```
