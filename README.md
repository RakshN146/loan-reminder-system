# 📧 Loan Reminder System

A full-stack Loan Reminder System that helps manage loans, send automated reminder emails, and track client replies.

---

## 🚀 Features

- 🔐 User Authentication (JWT-based login system)
- 📊 Dashboard with loan analytics
- 📝 Create and manage loans
- 📬 Send reminder emails manually
- ⏰ Automated daily email scheduler
- 📥 Track client email replies
- ✅ Auto-mark loan as PAID when payment confirmation detected
- 📈 Analytics summary (Total, Due, Overdue, Paid, Emails Sent, etc.)

---

## 🛠 Tech Stack

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT Authentication
- APScheduler (Daily email scheduler)
- SMTP (Email sending)

### Frontend
- React (Vite)
- Axios
- React Router
- CSS styling

---

## 📂 Project Structure

```
loan-reminder-system/
│
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   └── ...
│
├── loan-frontend/
│   ├── src/
│   ├── pages/
│   ├── components/
│   └── ...
│
└── README.md
```

---

## ⚙️ How To Run Locally

### 1️⃣ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Backend runs at:
```
http://127.0.0.1:8000
```

---

### 2️⃣ Frontend Setup

```bash
cd loan-frontend
npm install
npm run dev
```

Frontend runs at:
```
http://localhost:5173
```

---

## 📊 Dashboard Includes

- Total Loans
- Upcoming Loans
- Due Loans
- Overdue Loans
- Paid Loans
- Emails Sent
- Unread Replies

---

## 🔮 Future Improvements

- Email templates customization
- Payment gateway integration
- Admin / Multi-user roles
- Cloud deployment (AWS / Render / Railway)
- Charts & advanced analytics

---

## 👨‍💻 Developed By

Rakshan R Nayak  
MSc Data Science  
Full-Stack Developer

---

⭐ If you like this project, feel free to star the repository!