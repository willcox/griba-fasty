from fastapi import HTTPException, status, APIRouter, Depends
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import dbcon
from sqlalchemy.orm import Session

router = APIRouter(
        tags=['Authentication']
    );

@router.post('/login', response_model=schemas.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = dbcon):
    # {
    #     "username": "user",
    #     "password": "pass"
    # }
    user = db.query(models.User).filter(models.User.email == credentials.username).first();

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials");

    if not utils.verify(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials");

    # access token
    access_token = oauth2.create_access_token(data = {"user_id": user.id});
    
    return {"type_token": "bearer", "access_token": access_token}