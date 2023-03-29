from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import Users
from fastapi import HTTPException, Response
from utils.user import get_hash_pass, verify_password, get_user_dict

from utils.user import create_access_token
from datetime import datetime, timedelta


cookie_expires = datetime.utcnow() + timedelta(hours=1)


def create_user(db: Session, name, email, password, response):
    try:
        hash_password = get_hash_pass(password)
        db_user = Users(name=name, email=email, password=hash_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        access_token = create_access_token({"id": db_user.id})
        response.set_cookie(key="token", value=access_token)
        user_details = get_user_dict(db_user)
        return user_details
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Email already in use")


def login(db: Session, email, password, response):
    try:
        user = db.query(Users).filter(Users.email == email).first()

        if not user:
            return HTTPException(status_code=400, detail="user not found")

        valid_pass = verify_password(password, user.password)

        if not valid_pass:
            return HTTPException(status_code=400, detail="Wrong credentials")
        
        access_token = create_access_token({"id": user.id})
        if access_token:
            response.set_cookie(key="token", value=access_token, httponly=True)
            user_details = get_user_dict(user)
            return user_details

        return HTTPException(status_code=400, detail="user credentials error")
    except:
        raise HTTPException(status_code=500, detail="Internal server error")


def get_current_loggedin_user(db: Session, user_id):
    user = db.query(Users).filter(Users.id == user_id).first()

    user_details = get_user_dict(user)
    
    return user_details