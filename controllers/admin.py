from models.models import Users
from sqlalchemy.orm import Session


def get_users(db: Session):
    users = db.query(Users).all()
    return users