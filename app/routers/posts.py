from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

from ..postsSchema import Post, PostResponse, updatePost
from .. import models
from typing import List

router = APIRouter(
    tags = ['Posts']
)
# TODO Add a prefix for repeating routes


@router.get("/posts", response_model=List[PostResponse])
def retrive_post(db: Session = Depends(get_db)):
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@router.post("/posts", response_model=PostResponse)
def new_post(new_post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""insert into posts (title, content) values (%s, %s) returning * """,
    #                (new_post.title, new_post.content))
    # post = cursor.fetchone()
    # conn.commit()

    post = models.Post(**new_post.dict())

    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@ router.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)
    # if post:
    #     return {"data": post}
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post:
        return post
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")


@ router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db)):
    '''post = delete_post(id)
    if post:
        return {"deleted": post}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exits")'''

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} does not exit")

    post.delete(synchronize_session=False)
    db.commit()


@router.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def update_post(id: int, updatePost: updatePost, db:  Session = Depends(get_db)):
    ''' post = find_post(id)
    if post:
        if updatePost.title is not None:
            cursor.execute(
                """UPDATE posts SET title = %s WHERE id = %s RETURNING *""", (updatePost.title, str(id)))
        if updatePost.content is not None:
            cursor.execute(
                """UPDATE posts SET content = %s WHERE id = %s RETURNING *""", (updatePost.content, str(id)))
        udPost = cursor.fetchone()
        conn.commit()
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Post Does Not Exist")
        # response: Response = status.HTTP_201_CREATED
    return {"message": udPost }'''

    post_q = db.query(models.Post).filter(models.Post.id == id)
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

    post_q.update(postData, synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
