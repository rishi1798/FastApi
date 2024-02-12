from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from typing import Optional,List
from random import randrange
import mysql.connector
from .database import engine,get_db
from . import models,schemas,utils,auth
from sqlalchemy.orm import Session
from .routers import post,user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# pip install mysql-connector-python ///// first install this make settings as below
mydb = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="satish@123",
    database="test_db"
)


# pydantic model define the structure of the request and response so suppose if  a user want to create a post the request will
# go only if it has a title and content in the body as do not want to give the client the freedom to send the data whatever he wants

# sqlalchemy model are responsible for denining the columns of our posts table within mysql and is used to query,create,update,delete entries within the database


    
    
my_posts = [
            {"title":"title of post 1","content":"content of post 1","id":1},
            {"title":"favourite foods","content":"I like pizza","id":2}
        ]



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get('/sqlalchemy')
def test_posts(db:Session = Depends(get_db)):
    '''Here db is the database object and get_db function is creating the database session for our api endpoint'''
    
    posts = db.query(models.Post).all()
    print(db.query(models.Post))  # this will print the sql query to select the data from the database as SELECT posts.id AS posts_id, posts.title AS posts_title, posts.content AS posts_content, posts.published AS posts_published, posts.created_at AS posts_created_at FROM posts
    return {"data":"success"}


@app.get("/")
def root():
    cursor = mydb.cursor()
    cursor.execute('select * from employee')
    result = cursor.fetchall()
    return {"employee":result}



        

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        

