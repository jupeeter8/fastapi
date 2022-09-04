from .. import models, utils
from ..userSchema import User, CreatedUser

from fastapi import status, HTTPException, Depends, Response, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session

# TODO Add prefixes to path operations
router = APIRouter(
    tags=['Users']
)


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=CreatedUser)
def create_user(new_user: User, response: Response, db: Session = Depends(get_db)):

    userData = new_user.dict()
    userData['password'] = utils.hash_password(userData['password'])
    data = models.User(**userData)
    db.add(data)
    db.commit()
    db.refresh(data)
    return data

    # new_user.password = utils.hash_password(new_user.password)

    # user_data = models.User(**new_user.dict())
    # db.add(user_data)
    # db.commit()
    # db.refresh(user_data)

    # return user_data


@router.get("/users/{id}", response_model=CreatedUser)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} does not exist")
