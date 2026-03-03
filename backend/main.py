from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from database import SessionLocal, engine
from models import Base, Loan, LoanStatus, User, EmailLog
from scheduler import start_scheduler, shutdown_scheduler
import schemas
import auth

from services.loan_status_service import update_all_loan_statuses
from email_service import send_email
from ai_email_generator import generate_loan_email
from email_reply_reader import fetch_unread_replies

from fastapi.middleware.cors import CORSMiddleware


# ---------------------------------------------
# Create Tables
# ---------------------------------------------
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------
# Scheduler Lifecycle
# ---------------------------------------------
@app.on_event("startup")
def on_startup():
    start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    shutdown_scheduler()


# ---------------------------------------------
# Database Dependency
# ---------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------
# ROOT
# ---------------------------------------------
@app.get("/")
def read_root():
    return {"message": "Loan Reminder API Running"}


# ---------------------------------------------
# REGISTER USER
# ---------------------------------------------
@app.post("/api/register")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = auth.hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}


# ---------------------------------------------
# LOGIN USER (Swagger Compatible)
# ---------------------------------------------
@app.post("/api/login", response_model=schemas.TokenResponse)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not auth.verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = auth.create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ---------------------------------------------
# CREATE LOAN (PROTECTED)
# ---------------------------------------------
@app.post("/api/loans")
def create_loan(
    loan: schemas.LoanCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):

    db_loan = Loan(
        client_name=loan.client_name,
        email=loan.email,
        amount=loan.amount,
        due_date=loan.due_date,
        status=LoanStatus.UPCOMING,
    )

    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


# ---------------------------------------------
# GET ALL LOANS
# ---------------------------------------------
@app.get("/api/loans")
def get_loans(db: Session = Depends(get_db)):
    return db.query(Loan).all()


# ---------------------------------------------
# RUN STATUS UPDATE (PROTECTED)
# ---------------------------------------------
@app.post("/api/run-status-update")
def run_status_update(
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    updated = update_all_loan_statuses(db)
    return {"updated_loans": updated}


# ---------------------------------------------
# MARK LOAN AS PAID (PROTECTED)
# ---------------------------------------------
@app.post("/api/mark-paid/{loan_id}")
def mark_loan_paid(
    loan_id: int,
    paid_amount: int,
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):

    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    today = date.today()

    loan.payment_date = today
    loan.paid_amount = paid_amount

    if today <= loan.due_date:
        loan.status = LoanStatus.PAID
    else:
        loan.status = LoanStatus.PAID_LATE

    db.commit()

    return {
        "message": "Loan marked as paid",
        "status": loan.status
    }


# ---------------------------------------------
# DASHBOARD SUMMARY (PROTECTED)
# ---------------------------------------------
@app.get("/api/dashboard-summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)):

    total_loans = db.query(func.count(Loan.id)).scalar()

    upcoming = db.query(func.count(Loan.id))\
        .filter(Loan.status == LoanStatus.UPCOMING).scalar()

    due = db.query(func.count(Loan.id))\
        .filter(Loan.status == LoanStatus.DUE).scalar()

    overdue = db.query(func.count(Loan.id))\
        .filter(Loan.status == LoanStatus.OVERDUE).scalar()

    paid = db.query(func.count(Loan.id))\
        .filter(Loan.status == LoanStatus.PAID).scalar()

    paid_late = db.query(func.count(Loan.id))\
        .filter(Loan.status == LoanStatus.PAID_LATE).scalar()

    emails_sent = db.query(func.count(EmailLog.id)).scalar()

    unread_replies = db.query(func.count(EmailLog.id))\
        .filter(EmailLog.email_type == "CLIENT_REPLY")\
        .scalar()

    return {
        "total_loans": total_loans,
        "upcoming": upcoming,
        "due": due,
        "overdue": overdue,
        "paid": paid,
        "paid_late": paid_late,
        "emails_sent": emails_sent,
        "unread_replies": unread_replies
    }

# ---------------------------------------------
# TEST EMAIL
# ---------------------------------------------
@app.post("/api/test-email")
def test_email():
    success = send_email(
        to_email="loan.reminder.system@gmail.com",
        subject="Test Email from Loan Reminder System",
        body="If you are reading this, SMTP is working successfully."
    )

    return {"message": "Email sent successfully" if success else "Email sending failed"}


# ---------------------------------------------
# TEST AI EMAIL
# ---------------------------------------------
@app.post("/api/test-ai-email")
def test_ai_email():
    content = generate_loan_email(
        client_name="Ravi Kumar",
        amount=50000,
        due_date="2026-03-15",
        status="OVERDUE"
    )
    return {"generated_email": content}

# ---------------------------------------------
# FETCH CLIENT EMAIL REPLIES (MANUAL)
# ---------------------------------------------
@app.post("/api/check-email-replies")
def check_email_replies(
    current_user: str = Depends(auth.get_current_user)
):
    fetch_unread_replies()
    return {"message": "Checked unread email replies"}


@app.get("/api/client-replies")
def get_client_replies(
    db: Session = Depends(get_db),
    current_user: str = Depends(auth.get_current_user)
):
    replies = db.query(EmailLog)\
        .filter(EmailLog.status == "REPLY")\
        .order_by(EmailLog.sent_at.desc())\
        .all()

    return replies