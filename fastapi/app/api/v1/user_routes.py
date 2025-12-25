from fastapi import APIRouter,Depends
from app.schemas import userResponse,registerSchema 
from app.db.dependencies import get_session
from sqlalchemy.orm import Session
from app.db.models import User
from app.utilities import get_current_active_user, get_pwd_hash,verify_access_token
from app.exceptions import raise_not_found_exception, raise_bad_request_exception
import uuid


user_routes=APIRouter(prefix="/api/v1/users",tags=["Users"])



@user_routes.get("/profile",response_model=userResponse)
def get_user_profile(current_user:User=Depends(get_current_active_user)):
    """
     Get current user profile.
    """
    # Exclude the sensitive hashed_password before returning

    return current_user


@user_routes.get("/verify-token")
def verify_token_endpoint(current_user:User=Depends(get_current_active_user)):
    """
     Get current user profile.
    """
    return {
        "valide":True,
        "user":{
            "id":current_user.id,
            "name":current_user.name ,
            "email":current_user.email,
            "active":current_user.active ,
            "admin":current_user.admin
        }
    }


@user_routes.get("/",response_model=list[userResponse])
def get_all_users(current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    return db.query(User).all()


@user_routes.get("/{user_id}",response_model=userResponse)
def get_user_by_id(user_id:uuid.UUID,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    """
     Get a user by id.
    """
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise_not_found_exception(detail="user not found")
    return user


@user_routes.post("/create-user", response_model=userResponse)
async def create_user(user_data:registerSchema,current_user:User=Depends(get_current_active_user), db:Session=Depends(get_session)):   
    """
     This endpoint create a user.
    """
    user=db.query(User).filter(User.email==user_data.email).first()
    if user:
        raise_not_found_exception(detail="user already exists!")
    else:
        hashed_password=get_pwd_hash(user_data.password)
        new_user=User(user_data.name,user_data.email,hashed_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

# only an active user can update a user
@user_routes.put("/{user_id}",response_model=userResponse)
def update_user(user_id:uuid.UUID,update_user:registerSchema,current_user:User=Depends(get_current_active_user), db:Session=Depends(get_session)):
    """
     Update a user by id.
    """
    db_user=db.query(User).filter(User.id==user_id).first()
    if not db_user:
        raise_not_found_exception(detail="user does not found")
    
    db_user.name=update_user.name
    db_user.email=update_user.email 
    db_user.active=update_user.active 
    db_user.admin=update_user.admin 

    db.commit()
    db.refresh(db_user)
    return db_user

# # only an active user can delete a users
@user_routes.delete("/{user_id}")
def delete_user(user_id:uuid.UUID,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    """
     delete a user by id.
    """
    db_user=db.query(User).filter(User.id==user_id).first()

    if not db_user:
        raise_not_found_exception(detail="user does not found")
    
    # to avoid the current user delete him self
    if db_user.id==current_user.id:
        raise_not_found_exception(detail="you can not delete yourself")

    db.delete(db_user)
    db.commit()
    
    return {"message":"user deleted successfully"}