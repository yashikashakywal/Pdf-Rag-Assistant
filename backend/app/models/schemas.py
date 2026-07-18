from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="At least 8 characters")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8, description="At least 8 characters")


class MessageResponse(BaseModel):
    message: str


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask about your documents")


class Source(BaseModel):
    file: str
    page: int


class AnswerResponse(BaseModel):
    answer: str
    sources: list[Source]


class UploadResponse(BaseModel):
    message: str
    filename: str
    pages: int
    chunks: int


class ErrorResponse(BaseModel):
    detail: str
