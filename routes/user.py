from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
from database import get_db
from fastapi.security import HTTPBearer
from controllers.user import create_user, login, get_current_loggedin_user
from schemas.user import Login, Register
from utils.user import verify_access_token

router = APIRouter()

security_scheme = HTTPBearer()

@router.get('/')
def index(user: dict = Depends(verify_access_token), db: Session = Depends(get_db)):
    user = get_current_loggedin_user(db, user['id'])
    return user


@router.post('/register')
def user_create(user: Register, response: Response, db: Session = Depends(get_db)):
    db_user = create_user(db=db, name=user.name, email=user.email, password=user.password, response=response)
    return db_user
    

@router.post('/login')
def user_login(user: Login, response: Response, db: Session = Depends(get_db)):
    db_user = login(db=db, **user.dict(), response=response)
    return db_user

