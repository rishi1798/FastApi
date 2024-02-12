from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .database import get_db
from . import schemas,models,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth",tags=['authentication'])

@router.post('/login',response_model=schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    print("1")
    # OAuth2PasswordRequestForm stores data in a dictionary in username and password field so whatever we pass it will go in username 
    # so we will use username instead of email and it do not expects data in json instead it required  data in form data so in postman send data in form data
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid1 credential")
    
    if not utils.verify(user_credential.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credential")
    
    
    access_token = oauth2.create_access_token(data={'user_id':user.id})
    return {"access_token":access_token,"token_type":"bearer"}