from fastapi import APIRouter, Depends
from controllers.admin import get_users
from utils.user import verify_access_admin_token

from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix='/admin')

@router.get('/user')
def get_all_users(admin: dict = Depends(verify_access_admin_token), db: Session = Depends(get_db)):
    users = get_users(db)
    return users