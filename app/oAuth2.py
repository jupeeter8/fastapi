from jose import JWTError, jwt
from datetime import timedelta, datetime
from . import userSchema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECERET_KEY = 'a390fbb22890622aefbe7da5cb9bc0a3fd083e93e14c4bb2e40cd91826014ae5'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_acces_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECERET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECERET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        id: int = payload.get("id")
        if username is None or id is None:
            print("i am herer")
            raise credentials_exception
        token_data = userSchema.TokenData(username=username, id=id)

    except JWTError:
        print("i am herer 2")
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate the user", headers={"WWW-Authenticate":  "Bearer"})

    return verify_token(token, credentials_exception)
