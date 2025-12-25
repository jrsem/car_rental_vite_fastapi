from fastapi import APIRouter, Depends
from app.db.models import User
from app.db.dependencies import get_session
from app.utilities import get_pwd_hash,verify_password,create_access_token
from app.schemas import registerSchema ,tokenSchema
from sqlalchemy.orm import Session
from app.schemas import userResponse
from datetime import timedelta,datetime,timezone
import os
from fastapi.security import OAuth2PasswordRequestForm
from app.exceptions import raise_not_found_exception

auth_routes=APIRouter(prefix="/api/v1/auth",tags=["Auth"])


@auth_routes.post("/register", response_model=userResponse)

def register(form_data:registerSchema, db:Session=Depends(get_session)):   
    """
     This endpoint to register a user.
    """
   
    db_user=db.query(User).filter(User.email==form_data.email).first()
    if db_user:
   
        raise_not_found_exception(detail="user already exists!")
    else:
        hashed_password=get_pwd_hash(form_data.password)
        
        new_user=User(name=form_data.name,email=form_data.email,password=hashed_password, admin=form_data.admin,active=form_data.active)

        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user



@auth_routes.post("/token",response_model=tokenSchema)
def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_session)):
    """autheticate a user by checking its password and email"""

    
    db_user=db.query(User).filter(User.email==form_data.username).first()

    


    if not db_user or not verify_password(db_user.password,form_data.password):
       
        raise_not_found_exception(detail="Wrong credentials")
    
    if not db_user.active:
        
        raise_not_found_exception(detail="Inactive user")
        
   
    access_token=create_access_token(db_user.id,db_user.email)
    return {"access_token":access_token,"token_type":"bearer"}