from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Loan Reminder System is running 🚀"}