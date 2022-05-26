from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint


# *************** USER **************
class UserBase(BaseModel):
    email: EmailStr;
    password: str;

class UserCreate(UserBase):
    pass;

class User(BaseModel):
    id: int;
    email: EmailStr;
    created_at: datetime;
    
    class Config:
        orm_mode = True;

# *************** POST **************
class PostBase(BaseModel):
    title: str;
    content: str;
    published: bool = True;

class PostCreate(PostBase):
    pass;

class Post(PostBase):
    id: int;
    created_at: datetime;
    owner_id : int;
    owner: User;
    
    class Config:
        orm_mode = True;

class PostJoin(BaseModel):
    Post: Post;
    votes_count: int;
    
    class Config:
        orm_mode = True;

# *************** TOKEN **************
class Token(BaseModel):
    access_token: str;
    type_token: str;

class TokenData(BaseModel):
    id: Optional[str] = None;

# *************** TOKEN **************
class Vote(BaseModel):
    post_id: int;
    star: conint(le=1);
    