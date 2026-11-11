"""Email delivery via Resend. The PDF report is sent ONLY to the therapist's
own inbox - never to the client - regardless of what is entered in the form."""

import base64
import resend

THERAPIST_EMAIL = "yusuf.a.abdelatti@gmail.com"


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
