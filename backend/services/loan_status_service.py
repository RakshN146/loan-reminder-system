from datetime import date
from sqlalchemy.orm import Session
from models import Loan, LoanStatus, EmailLog
from ai_email_generator import generate_loan_email
from email_service import send_email
from services.compliance_service import can_send_email_now


# ---------------------------------------
# Calculate Loan Status
# ---------------------------------------
def calculate_loan_status(due_date: date, today: date | None = None) -> LoanStatus:
    reference_day = today or date.today()

    if due_date > reference_day:
        return LoanStatus.UPCOMING
    if due_date == reference_day:
        return LoanStatus.DUE
    return LoanStatus.OVERDUE


# ---------------------------------------
# Check if email already sent
# ---------------------------------------
def email_already_sent(db, loan_id, email_type):
    return db.query(EmailLog).filter(
        EmailLog.loan_id == loan_id,
        EmailLog.email_type == email_type
    ).first() is not None


# ---------------------------------------
# Send Reminder Helper
# ---------------------------------------
def send_reminder(db, loan, email_type, subject_line):

    # ✅ Compliance check
    if not can_send_email_now():
        print("Email blocked due to compliance rules.")
        return False

    email_body = generate_loan_email(
        client_name=loan.client_name,
        amount=loan.amount,
        due_date=str(loan.due_date),
        status=email_type
    )

    email_sent = send_email(
        to_email=loan.email,
        subject=subject_line,
        body=email_body
    )

    email_log = EmailLog(
        loan_id=loan.id,
        recipient_email=loan.email,
        subject=subject_line,
        body=email_body,
        status="SENT" if email_sent else "FAILED",
        email_type=email_type
    )

    db.add(email_log)

    return email_sent


# ---------------------------------------
# Main Automation Engine
# ---------------------------------------
def update_all_loan_statuses(db: Session, today: date | None = None) -> int:

    reference_day = today or date.today()
    loans = db.query(Loan).all()

    updates = 0

    for loan in loans:

        # ✅ Skip paid loans
        if loan.status in [LoanStatus.PAID, LoanStatus.PAID_LATE]:
            continue

        expected_status = calculate_loan_status(loan.due_date, reference_day)

        # Update status
        if loan.status != expected_status:
            loan.status = expected_status
            updates += 1

        days_until_due = (loan.due_date - reference_day).days

        # ----------------------------------
        # 1️⃣ UPCOMING Reminder (2 days before)
        # ----------------------------------
        if expected_status == LoanStatus.UPCOMING and days_until_due == 2:

            if not email_already_sent(db, loan.id, "REMINDER_2_DAYS"):
                send_reminder(
                    db,
                    loan,
                    "REMINDER_2_DAYS",
                    "Reminder: Loan due in 2 days"
                )

        # ----------------------------------
        # 2️⃣ Due Today
        # ----------------------------------
        # DUE → send due day email
        if expected_status == LoanStatus.DUE:

            if not email_already_sent(db, loan.id, "DUE_REMINDER"):
                send_reminder(
                    db,
                    loan,
                    email_type="DUE_REMINDER",
                    subject_line="🚨 Loan Due Today - Immediate Payment Required"
        )

        # ----------------------------------
        # 3️⃣ Overdue Escalations
        # ----------------------------------
        if expected_status == LoanStatus.OVERDUE:

            # Day 1 overdue
            if days_until_due == -1:
                if not email_already_sent(db, loan.id, "OVERDUE_DAY_1"):
                    send_reminder(
                        db,
                        loan,
                        "OVERDUE_DAY_1",
                        "Reminder: Payment 1 Day Overdue"
                    )

            # Day 3 overdue
            if days_until_due == -3:
                if not email_already_sent(db, loan.id, "OVERDUE_DAY_3"):
                    send_reminder(
                        db,
                        loan,
                        "OVERDUE_DAY_3",
                        "Warning: Payment 3 Days Overdue"
                    )

            # Day 5 overdue
            if days_until_due == -5:
                if not email_already_sent(db, loan.id, "OVERDUE_DAY_5"):
                    send_reminder(
                        db,
                        loan,
                        "OVERDUE_DAY_5",
                        "Final Warning: 5 Days Overdue"
                    )

    db.commit()
    return updates