from sqlalchemy import create_engine,\
    Column,String,Integer, Boolean,\
        Float,ForeignKey,Date,Text,DateTime,\
        Table

# from sqlalchemy_utils.types import ChoiceType
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID,ENUM
from datetime import datetime, timezone
from app.db.dependencies import Base
# import enum


# class RolesEnum(enum.Enum):
#     ADMIN = "ADMIN"
#     USER = "USER"
#     GUEST = "GUEST"


class User(Base):
    __tablename__="users"

    id= Column("id",UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    name=Column("name",String(50),nullable=False )
    email=Column("email",String,unique=True, nullable=False, index=True)
    password=Column("password",String)
    active=Column("active",Boolean)
    admin=Column("admin",Boolean,default=False)
    # role=Column("role",ENUM(RolesEnum), default=RolesEnum.USER, nullable=False)
    created_at=Column("created_at",DateTime, default=datetime.now(timezone.utc))
    car = relationship("Car", back_populates="user")
    def __init__(self, name,email, password,active=True,admin=False):
        self.name=name 
        self.email=email 
        self.password=password
        self.active=active 
        self.admin=admin




  
  
class Car(Base):
    __tablename__="cars"

    id= Column("id",UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    brand=Column("brand",String, nullable=False)
    model=Column("model",String, nullable=False)
    year=Column("year",Integer, nullable=False)
    category=Column("category",String, nullable=False)
    seating_capacity=Column("seating_capacity",Integer, nullable=False)
    fuel_type=Column("fuel_type",String, nullable=False)
    transmission=Column("transmission",String, nullable=False)
    pricePerDay=Column("pricePerDay",Integer, nullable=False)
    location=Column("location",String, nullable=False)
    description=Column("description",String, nullable=False)
    isAvaliable=Column("isAvaliable",Boolean,default=True)
    # image car
    url=Column("url",String, nullable=False)
    file_type=Column("file_type",String, nullable=False)
    file_name=Column("file_name",String, nullable=False)

    timestamp=Column("timestamp",DateTime,default=datetime.now(timezone.utc)) 
    created_at=Column("created_at",DateTime, default=datetime.now(timezone.utc))

    user_id=Column("user_id",ForeignKey("users.id"))#cheve primary da tabela User
    user= relationship("User", back_populates="car")

    def __init__(self,brand, model,year,category,
                 seating_capacity,fuel_type,file_type,file_name,user_id,transmission,pricePerDay,location,description,url,isAvaliable=True):
        self.brand=brand 
        self.model=model
        self.year=year 
        self.category=category
        self.seating_capacity=seating_capacity
        self.fuel_type=fuel_type
        self.user_id=user_id
        self.transmission=transmission
        self.pricePerDay=pricePerDay
        self.location=location
        self.description=description
        self.url=url
        self.file_type=file_type
        self.file_name=file_name
        self.isAvaliable=isAvaliable 

