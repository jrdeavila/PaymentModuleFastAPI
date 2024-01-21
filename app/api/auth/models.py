from pydantic import BaseModel


class ApplicationToken(BaseModel):
    access_token: str
    token_type: str
