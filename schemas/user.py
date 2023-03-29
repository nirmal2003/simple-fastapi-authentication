from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenDate(BaseModel):
    id: int or None = None
    

class Register(BaseModel):
    name: str
    email: str
    password: str
    

class Login(BaseModel):
    email: str
    password: str
    

class CurrentUser(BaseModel):
    id: int
    name: str
    email: str
