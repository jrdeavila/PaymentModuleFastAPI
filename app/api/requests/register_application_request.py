from pydantic import BaseModel, EmailStr, Field


class RegisterApplicationRequest(BaseModel):
    name: str = Field(
        ..., example="My Application", description="The name of the application."
    )
    username: str = Field(
        ..., example="my-application", description="The username of the application."
    )
    email: EmailStr = Field(
        ..., example="example@gmail.com", description="The email of the application."
    )
    password: str = Field(
        ..., example="my-password", description="The password of the application."
    )
