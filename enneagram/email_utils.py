"""Email delivery via Resend. Both the client report and the practitioner-only
intervention report are sent ONLY to the practitioner's own inbox - never to
the client - regardless of what is entered in the form.

There is currently one configured recipient (THERAPIST_EMAIL), which doubles
as the practitioner address since this tool never emails the client directly.
If a separate practitioner/admin recipient is ever wanted for the
intervention report, set PRACTITIONER_EMAIL below rather than inventing one
here - until then, both reports go to the same configured address."""

import base64
import resend

THERAPIST_EMAIL = "yusuf.a.abdelatti@gmail.com"
PRACTITIONER_EMAIL = THERAPIST_EMAIL


def send_report_email(api_key, pdf_bytes, client_name, from_address):
    resend.api_key = api_key
    encoded = base64.b64encode(pdf_bytes).decode("utf-8")
    safe_name = (client_name or "client").strip().replace(" ", "_") or "client"
    filename = f"Enneagram_Report_{safe_name}.pdf"

    params = {
        "from": from_address,
        "to": [THERAPIST_EMAIL],
        "subject": f"Enneagram Clinical Report — {client_name or 'Confidential Client'}",
        "html": (
            f"<p>A new Enneagram assessment report has been generated"
            f"{f' for <b>{client_name}</b>' if client_name else ''}.</p>"
            f"<p>The full report, including scoring, charts, clinical notes, and the complete "
            f"item-by-item responses, is attached as a PDF.</p>"
            f"<p style='color:#8A94A6;font-size:12px;'>This email was sent automatically by the "
            f"Enneagram Clinical Assessment tool.</p>"
        ),
        "attachments": [
            {"filename": filename, "content": encoded},
        ],
    }
    return resend.Emails.send(params)


def send_intervention_email(api_key, pdf_bytes, client_name, from_address):
    resend.api_key = api_key
    encoded = base64.b64encode(pdf_bytes).decode("utf-8")
    safe_name = (client_name or "client").strip().replace(" ", "_") or "client"
    filename = f"Enneagram_Intervention_Report_{safe_name}.pdf"

    params = {
        "from": from_address,
        "to": [PRACTITIONER_EMAIL],
        "subject": f"[CONFIDENTIAL] Enneagram Intervention Report — {client_name or 'Confidential Client'}",
        "html": (
            f"<p><b>Practitioner-only, confidential.</b> A personalized Intervention & Session "
            f"Planning Report has been generated"
            f"{f' for <b>{client_name}</b>' if client_name else ''}.</p>"
            f"<p>It includes a psychological formulation, strengths/development areas, session "
            f"questions, discussion topics, choice-based scenarios, suggested interventions, and a "
            f"session roadmap - all generated from this client's actual assessment results.</p>"
            f"<p style='color:#8A94A6;font-size:12px;'>This content is hypothesis-generating, not "
            f"diagnostic, and is not intended for distribution to the client. Sent automatically by "
            f"the Enneagram Clinical Assessment tool.</p>"
        ),
        "attachments": [
            {"filename": filename, "content": encoded},
        ],
    }
    return resend.Emails.send(params)
