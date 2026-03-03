from pydantic import BaseModel
from datetime import date


class LoanCreate(BaseModel):
    client_name: str
    email: str
    amount: float
    due_date: date


class LoanResponse(LoanCreate):
    id: int
    status: str

    class Config:
        from_attributes = True


from pydantic import BaseModel, EmailStr


# -------------------------
# USER SCHEMAS
# -------------------------
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str