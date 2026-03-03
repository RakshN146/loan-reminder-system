from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# 🔐 Secret config
SECRET_KEY = "supersecretkey123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# ----------------------------
# HASH PASSWORD
# ----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password[:72])


# ----------------------------
# VERIFY PASSWORD
# ----------------------------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password[:72], hashed_password)


# ----------------------------
# CREATE ACCESS TOKEN
# ----------------------------
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----------------------------
# GET CURRENT USER FROM TOKEN
# ----------------------------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        return username

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )