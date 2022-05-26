from fastapi import HTTPException, status, APIRouter
from .. import models, schemas, utils
from ..oauth2 import dbauth
from ..database import dbcon
from sqlalchemy.orm import Session

router = APIRouter(
        prefix="/votes",
        tags=['Votes']
    );

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = dbcon, current_user: int = dbauth):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first();
    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist !");

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id);
    found_vote = vote_query.first();
    
    if(vote.star == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post {vote.post_id}");

        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id);
        db.add(new_vote);
        db.commit();
        return {"message": "Successfully added vote !"};
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist !");

        vote_query.delete(synchronize_session=False);
        db.commit();
        return {"message": "Successfully deleted vote !"};