from urllib import response
from fastapi import APIRouter, Depends, HTTPException, status

from ..database import get_db
from sqlalchemy.orm import Session

from ..userSchema import UserLogin
from .. import utils, models


router = APIRouter(
    tags=['Authentication']
)


@router.get("/login")
def login(user_detail: UserLogin, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(
        models.User.username == user_detail.username)

    userData = user_query.first()
    if not userData:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with username {user_detail.username} not found")

    auth_passowrd = user_detail.password
    hashed_password = userData.password
    if utils.verify_password(hashed_password, auth_passowrd):
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Password does not match")
