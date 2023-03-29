from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from models.models import Users, Admin
from database import get_db

from datetime import datetime, timedelta
from jose import JWTError, jwt


SECRETE_KEY = "241535154b578b5687b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(password, hash_password):
    return pwd_context.verify(password, hash_password)
    

def get_hash_pass(password):
    return pwd_context.hash(password)


def get_user_dict(user):
    column_order = ['id', 'name', 'email']
    
    user_dict = {key: value for key, value in user.__dict__.items() if not key.startswith('_') and key != 'password'}

    ordered_dict = {key: user_dict[key] for key in column_order}
    
    return { 'user': ordered_dict }


def check_valid_user(user_id, db: Session):
    user_details = db.query(Users).filter(Users.id == user_id).first()
    
    if not user_details:
        return False
    return True
    

def check_valid_admin(user_id, db: Session):
    user_details = db.query(Admin).filter(Admin.user_id == user_id).first()

    if not user_details:
        return False

    return True
    

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRETE_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


def verify_access_token(request: Request, db: Session = Depends(get_db)):
        token = request.cookies['token']
        decode_token = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])

        if not decode_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_id = decode_token.get('id')
        valid_user = check_valid_user(user_id, db)

        if not valid_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        
        return decode_token
    

def verify_access_admin_token(request: Request, db: Session = Depends(get_db)):
    try:
        token = request.cookies['token']
        decode_token = jwt.decode(token, SECRETE_KEY, algorithms=[ALGORITHM])

        if not decode_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        user_id = decode_token.get('id')
        valid_user = check_valid_user(user_id, db)
        isAdmin = check_valid_admin(user_id, db)

        print(isAdmin)

        decode_token.update({ "admin": isAdmin })

        if not valid_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid user")
        if not isAdmin:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access debied")
        
        return decode_token
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access Denied")