from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
# PostBase is the base class containing the common fields for creating and updating posts.

class PostBase(BaseModel):
    title : str
    content : str
    published:bool = True
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime = datetime.now()
    
    class Config:
        orm_model = True


class Post(PostBase):
    id: int 
    owner_id:int
    created_at: datetime = datetime.now() 
    owner : UserOut # so type of created_at is datetime and set default value using  datetime.now()
    #  The Config class with orm_mode = True enables the pydantic model to be used as an ORM model for response.
    class Config:
            orm_mode = True
            
            
class UserCreate(BaseModel):
    email:EmailStr
    password:str
    

        
class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token : str
    token_type : str    
    
class TokenData(BaseModel):
    id:Optional[str]=None
    
    