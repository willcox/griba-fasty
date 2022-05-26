from fastapi import HTTPException, status, Response, APIRouter
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..oauth2 import dbauth
from ..database import dbcon
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter(
        prefix="/posts",
        tags=['Posts']
    );

# @router.get("/votes")
@router.get("/votes", response_model=List[schemas.PostJoin])
async def list_posts_votes(db: Session = dbcon, current_user: int = dbauth, 
                            limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all();
    
    return posts;

@router.get("/votes/{id}", response_model=schemas.PostJoin)
async def get_posts(id: int, db: Session = dbcon, current_user: int = dbauth):
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes_count")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first();
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found");

    return posts;

@router.get("/", response_model=List[schemas.Post])
async def list_posts(db: Session = dbcon, current_user: int = dbauth, 
                     limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all();
    # return {"data": posts};
    return posts;

@router.get("/{id}", response_model=schemas.Post)
async def get_posts(id: int, db: Session = dbcon, current_user: int = dbauth):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    posts = db.query(models.Post).filter(models.Post.id == id).first();
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found");
    # return {"data": posts};
    return posts;

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def add_posts(post: schemas.PostCreate, db: Session = dbcon, current_user: int = dbauth):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published);
    new_post = models.Post(owner_id = current_user.id, **post.dict());
    db.add(new_post);
    db.commit();
    db.refresh(new_post);
    # return {"data": new_post};
    return new_post;

@router.put("/{id}", response_model=schemas.Post)
async def update_posts(id: int, upost: schemas.PostCreate, db: Session = dbcon, current_user: int = dbauth):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s returning *""", 
    # (post.title, post.content, post.published, str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id);
    post = post_query.first();
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found");

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authaurized to perform requested action !");
        
    # post_query.update({'title' : '...', 'content' : '...'}, synchronize_session=False);
    post_query.update(upost.dict(), synchronize_session=False);
    db.commit()
    
    # return {"data": post_query.first()};
    return post_query.first();

@router.delete("/{id}")
async def delete_posts(id: int, db: Session = dbcon, current_user: int = dbauth):
    # cursor.execute("""DELETE from posts WHERE id = %s returning *""", (str(id),))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id);
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found !");

    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authaurized to perform requested action !");
        
    post.delete(synchronize_session=False);
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT);