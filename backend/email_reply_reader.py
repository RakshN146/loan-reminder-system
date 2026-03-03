import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime

from database import SessionLocal
from models import EmailLog, Loan, LoanStatus


IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
IMAP_USER = os.getenv("IMAP_USER")
IMAP_PASS = os.getenv("IMAP_PASS")


# ------------------------------------------------
# Detect Reply Intent (AI-like rule engine)
# ------------------------------------------------
def detect_reply_intent(body: str) -> str:
    body_lower = body.lower()

    payment_keywords = [
        "paid",
        "payment done",
        "i have paid",
        "amount transferred",
        "upi sent",
        "transfer completed"
    ]

    negative_keywords = [
        "cannot pay",
        "not able",
        "need more time",
        "financial issue",
        "delay"
    ]

    for word in payment_keywords:
        if word in body_lower:
            return "PAID_CONFIRMED"

    for word in negative_keywords:
        if word in body_lower:
            return "ESCALATION_REQUIRED"

    return "UNKNOWN"


# ------------------------------------------------
# Fetch Unread Replies
# ------------------------------------------------
def fetch_unread_replies():

    mail = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    mail.login(IMAP_USER, IMAP_PASS)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')

    if status != "OK":
        mail.logout()
        return

    db = SessionLocal()

    for num in messages[0].split():
        status, msg_data = mail.fetch(num, "(RFC822)")
        if status != "OK":
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        from email.utils import parseaddr
        from_email = parseaddr(msg.get("From"))[1]

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        # Try to match loan by email
        loan = db.query(Loan).filter(Loan.email == from_email).first()

        if not loan:
            print(f"Ignoring unrelated email from: {from_email}")
            continue

        intent = detect_reply_intent(body)

        # Auto-update loan if paid
        intent = detect_reply_intent(body)

        if intent == "PAID" and loan:

            # 🔹 1. Save reply log first
            reply_log = EmailLog(
                loan_id=loan.id,
                recipient_email=from_email,
                subject=subject,
                body=body,
                status="REPLY",
                email_type="CLIENT_REPLY",
                sent_at=datetime.utcnow()
            )

            db.add(reply_log)

            # 🔹 2. Update loan status
            loan.status = LoanStatus.PAID
            loan.payment_date = date.today()

            db.commit()

            print(f"Auto-marked loan {loan.id} as PAID")

        # Save log
        log = EmailLog(
            loan_id=loan.id,
            recipient_email=from_email,
            subject=subject,
            body=body,
            status="REPLY",
            email_type=intent,
            sent_at=datetime.utcnow()
        )

        db.add(log)
        db.commit()

    db.close()
    mail.logout()