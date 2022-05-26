from fastapi import HTTPException, status, APIRouter
from .. import models, schemas, utils
from ..database import dbcon
from sqlalchemy.orm import Session

router = APIRouter(
        prefix="/users",
        tags=['Users']
    );

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
async def add_users(user: schemas.UserCreate, db: Session = dbcon):
    # hash the password - user.password
    hashsed_password = utils.password_encode(user.password);
    user.password = hashsed_password;
    
    new_user = models.User(**user.dict());
    db.add(new_user);
    db.commit();
    db.refresh(new_user);

    return new_user;

@router.get("/{id}", response_model=schemas.User)
async def get_users(id: int, db: Session = dbcon):
    user = db.query(models.User).filter(models.User.id == id).first();
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} was not found");
    return user;
