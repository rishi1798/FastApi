from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import get_db
from typing import Optional,List


router = APIRouter(prefix="/posts",tags=['Posts'])

@router.get('/',response_model=List[schemas.Post])
def get_all_posts(db:Session = Depends(get_db),limit:int=4,skip:int=0, search:Optional[str]=""):  # limit arg will limit the number of post in the response pass limit key in the query parameter with its value default is 4
    # skip will skip the given number of posts so if skip is 2 then it will skip starting two posts. iseful in pagination
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

# The response_model parameter is used to define the model for the response, while response_class is used to define the response class, such as JSONResponse.
@router.post("/createposts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def createposts(post:schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # import ipdb
    # ipdb.set_trace()
    # post_dict = post.model_dump()
    # post_dict['id']=randrange(0,1000000)
    # my_posts.append(post_dict)
    
    # new_post = models.Post(title=post.title,content=post.content,published=post.published) same as **post.model_dump()
    
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    # new_post is a sql alchemy model and pydantic has no idea what to do of this . to convert this sql alchemy model into pydantic model by passing class Confing in schema.py class
    
    return new_post


@router.get("/{id}",response_model=schemas.Post)
def get_posts_by_id(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    # if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f'post with id {id} was not found'}
        # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
        
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post1 = post_query.first()
    
    if post1 == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
     
    if post1.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    
    post_query.update(post.model_dump(),synchronize_session=False)
    db.commit()
    
    
    return post_query.first()