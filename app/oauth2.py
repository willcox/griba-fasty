from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, models
from fastapi.security import OAuth2PasswordBearer
from .database import dbcon
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login');

# SECRET KEY
SECRET_KEY = settings.fasty_secret_key;
# Algorithm
ALGORITHM = settings.fasty_algorithm;
# Expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = settings.fasty_access_token_expire_minutes;

def create_access_token(data: dict):
    to_encode = data.copy();
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES);
    to_encode.update({"exp" : expire});

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM);

    return encoded_jwt;

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]);
        id: str = payload.get("user_id");

        if id is None:
            raise credentials_exception;
        token_data = schemas.TokenData(id = id);
        
    except JWTError:
        raise credentials_exception;

    return token_data;


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = dbcon):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentails",
                                          headers={"WWW-Authenticate" : "Bearer"});

    token = verify_access_token(token, credentials_exception);
    user = db.query(models.User).filter(models.User.id == token.id).first();
    
    return user;

# Auth syntax
dbauth = Depends(get_current_user);