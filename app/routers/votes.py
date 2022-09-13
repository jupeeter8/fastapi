from sqlalchemy.orm import Session
from fastapi import APIRouter, status, HTTPException, Depends


from .. database import get_db
from app import models, oAuth2
from .. votesSchema import VotesResposne

router = APIRouter(
    tags=['Voting']
)


@router.post('/vote', response_model=VotesResposne)
def votes(current_user_id: int = Depends(oAuth2.get_current_user), db: Session = Depends(get_db), post_id: int = None):
    """
    how bout gettin some votes sorry bitecvhes
    """
    if post_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Post can not have id of None")
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} not found")

    vote_query = db.query(models.Votes).filter(
        models.Votes.post_id == post_id, models.Votes.user_id == current_user_id)
    vote = vote_query.first()
    if not vote:
        vote_data = models.Votes(
            post_id=post_id, user_id=current_user_id, vote_value=1)
        db.add(vote_data)
        db.commit()
        db.refresh(vote_data)
        return vote_data

    else:

        if vote.vote_value == 1:
            vote.vote_value = 0
        else:
            vote.vote_value = 1

        db.commit()
        db.refresh(vote)
        return vote
