from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session

from app import oAuth2, userSchema
from ..database import get_db

from ..postsSchema import Post, PostResponse, updatePost
from .. import models
from typing import List, Optional

router = APIRouter(
    tags=['Posts']
)
# TODO Add a prefix for repeating routes


@router.get("/posts", response_model=List[PostResponse])
def retrive_post(db: Session = Depends(get_db), current_user_id: int = Depends(oAuth2.get_current_user),
                 limit: int = 5, search: Optional[str] = None):

    posts = db.query(models.Post).filter(models.Post.title.contains(
        search)if search else True).limit(limit).all()
    return posts


@router.post("/posts", response_model=PostResponse)  # Creating Post route
def new_post(new_post: Post, db: Session = Depends(get_db), current_user_id: int = Depends(oAuth2.get_current_user)):

    post_data = new_post.dict()
    post_data.update({'user_id': current_user_id})
    post = models.Post(**post_data)

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@ router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: str = Depends(oAuth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")


# Deleting post route
@ router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oAuth2.get_current_user)):

    # Querring all entries by the user with username = current_user.username and the provided post id

    post = db.query(models.Post).filter(
        models.Post.user_id == current_user_id, models.Post.id == id)

    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exit")

    post.delete(synchronize_session=False)
    db.commit()


@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def update_post(id: int, updatePost: updatePost, db:  Session = Depends(get_db), current_user_id: id = Depends(oAuth2.get_current_user), ):

    post_q = db.query(models.Post).filter(models.Post.user_id ==
                                          current_user_id, models.Post.id == id)
    post = post_q.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    postData = updatePost.dict()
    keyarr = []

    for i in postData:
        if postData[i] is None:
            keyarr.append(i)
    for i in keyarr:
        postData.pop(i)
    del (keyarr)

    # postData.update({'user': current_user})

    post_q.update(postData, synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
