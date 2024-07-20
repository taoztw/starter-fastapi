from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class UserPost(BaseModel):
    email: EmailStr
    password_hash: str = Field(min_length=8, max_length=128)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class VerifyEmailCode(BaseModel):
    email: EmailStr()
    code: str


class SendEmail(BaseModel):
    email: EmailStr


class ResetPassword(BaseModel):
    reset_token: str
    new_password: str
