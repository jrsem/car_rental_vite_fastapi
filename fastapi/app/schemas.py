import uuid
from pydantic import BaseModel, Field 
from fastapi import File,UploadFile
from typing import Optional
from datetime import date, datetime, time
from uuid import UUID, uuid4 # Import uuid4 to generate new UUIDs
from sqlalchemy.dialects.postgresql import UUID
# from enum import Enum

# class UserRole(str, Enum):
#     ADMIN = "ADMIN"
#     USER = "USER"
#     GUEST="GUEST"

class registerSchema(BaseModel):
    name:str
    email:str 
    password:str
    active:Optional[bool]=True
    admin:Optional[bool]=False
    # role:UserRole=UserRole.USER
    class config: 
        from_attributes=True 
  
class carSchema(BaseModel):
    brand:str
    model:str 
    year:int 
    category:str
    seating_capacity:int 
    fuel_type:str 
    transmission:str 
    pricePerDay:int 
    location:str 
    description:str
    isAvaliable:Optional[bool]=True
    class config: 
        from_attributes=True 

class carRespseSchema(carSchema):
    id:uuid.UUID
    user_id:uuid.UUID 
    url:str 
    file_name:str 
    file_type:str
    created_at:datetime
    timestamp:datetime
    class config: 
        from_attributes=True 
        



class loginSchema(BaseModel):
    email:str 
    password:str
    class config: 
        from_attributes=True 


class tokenSchema(BaseModel):
    """ the shape of the response when a token is successfully issued"""
    access_token:str 
    token_type:str="bearer"


class tokenResponseSchema(BaseModel):
    """ the data we expect to find inside the JWT payload"""
    id:uuid.UUID = Field(primary_key=True)
    email:Optional[str]=None 


class userResponse(registerSchema):
    id:uuid.UUID = Field(primary_key=True)
    class config: 
        from_attributes=True 

    
    







  