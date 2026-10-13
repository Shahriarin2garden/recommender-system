"""Authentication router - handles user registration and login."""

import os
import uuid
from datetime import datetime, timedelta
from typing import Optional

import bcrypt as _bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session

from app.database import get_db, get_redis
from app.models import User
from app.schemas import Token, UserCreate, UserResponse

router = APIRouter()

ENVIRONMENT = os.getenv("ENVIRONMENT", "development").lower()
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true" if ENVIRONMENT == "production" else "false").lower() in {"1", "true", "yes", "on"}
SECRET_KEY = os.getenv("JWT_SECRET")

if not SECRET_KEY:
    if ENVIRONMENT == "development":
        SECRET_KEY = "dev-only-insecure-jwt-secret-not-for-production"
    else:
        raise RuntimeError("FATAL: JWT_SECRET is required in non-development environment.")

if ENVIRONMENT != "development" and len(SECRET_KEY) < 32:
    raise RuntimeError("FATAL: Weak JWT_SECRET detected in non-development environment.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
revoked_tokens = set()


def _redis_token_key(jti: str) -> str:
    return f"revoked_token:{jti}"


def add_revoked_token(jti: str) -> None:
    revoked_tokens.add(jti)
    client = get_redis()
    if client is not None:
        client.setex(_redis_token_key(jti), 86400, "1")


def is_token_revoked(jti: Optional[str]) -> bool:
    if not jti:
        return False
    if jti in revoked_tokens:
        return True
    client = get_redis()
    if client is not None:
        return bool(client.get(_redis_token_key(jti)))
    return False


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.headers.get("Authorization")
        if not authorization:
            authorization = request.cookies.get("access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return _bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    return _bcrypt.hashpw(password[:72].encode(), _bcrypt.gensalt()).decode()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "jti": str(uuid.uuid4())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if is_token_revoked(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    try:
        db_user_id = int(user_id)
    except (TypeError, ValueError):
        raise credentials_exception

    user = db.query(User).filter(User.id == db_user_id).first()
    if user is None:
        raise credentials_exception
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=get_password_hash(user.password),
        cohort="A",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        secure=COOKIE_SECURE,
        samesite="lax",
        path="/",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/logout")
async def logout(response: Response, token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        if jti:
            add_revoked_token(jti)
    except jwt.PyJWTError:
        pass

    response.delete_cookie("access_token", httponly=True, secure=COOKIE_SECURE, samesite="lax", path="/")
    return {"message": "Logged out successfully"}
