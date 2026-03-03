import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_loan_email(client_name: str, amount: float, due_date: str, status: str) -> str:
    """
    Generate AI-based loan reminder email based on loan status.
    """

    if status == "UPCOMING":
        tone = "polite and friendly reminder"
    elif status == "DUE":
        tone = "firm but professional reminder"
    elif status == "OVERDUE":
        tone = "strict and urgent warning tone"
    else:
        tone = "professional tone"

    prompt = f"""
    Write a professional loan repayment email.

    Client Name: {client_name}
    Loan Amount: ₹{amount}
    Due Date: {due_date}
    Status: {status}

    The email tone should be: {tone}

    Keep it concise, professional, and clear.
    Mention consequences politely if overdue.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professional banking loan recovery assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content