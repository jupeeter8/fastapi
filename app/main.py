# from fastapi.params import Body
# from psycopg2 import connect
# from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from . import models
from .database import engine
from .routers.posts import router as post_route
from .routers.users import router as user_route
from .routers.auth import router as auth_route
from .config import envar


while True:
    try:
        models.Base.metadata.create_all(bind=engine)
        break
    except Exception as error:
        print("Connection failed: ", error)

app = FastAPI()


'''while True:
    try:
        conn = connect(host='localhost', database='fastapi',
                       user='postgres', password='password', port='5001', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as error:
        print("Connection failed: ", error)


def find_post(id: int):
    id = str(id)
    cursor.execute("""select * from posts where id = %s """, (id))
    post = cursor.fetchone()
    return post


def delete_post(id):
    cursor.execute(
        """delete from posts where id = %s returning * """, (str(id)))
    post = cursor.fetchone()
    conn.commit()
    return post'''


app.include_router(post_route)
app.include_router(user_route)
app.include_router(auth_route)


@ app.get('/')
def root():
    return {"messages": "Hello World"}
