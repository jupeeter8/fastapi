from jose import JWTError, jwt
from datetime import timedelta, datetime

SECERET_KEY = 'a390fbb22890622aefbe7da5cb9bc0a3fd083e93e14c4bb2e40cd91826014ae5'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_acces_tocken(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECERET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
