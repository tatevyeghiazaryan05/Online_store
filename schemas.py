from pydantic import BaseModel, EmailStr


class UserSignUpSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserNameChangeSchema(BaseModel):
    name: str


class UserPasswordChangeSchema(BaseModel):
    password: str


class AdminPasswordRecoverSchema(BaseModel):
    code: str
    new_password: str
