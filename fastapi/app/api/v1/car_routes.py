from fastapi import APIRouter,Depends,File,UploadFile,Form
from app.schemas import carSchema ,carRespseSchema
from app.db.dependencies import get_session
from sqlalchemy.orm import Session
from app.db.models import User,Car
from app.utilities import get_current_active_user, get_pwd_hash,verify_access_token
from app.exceptions import raise_not_found_exception, raise_bad_request_exception
import uuid
from sqlalchemy import func
from app.images import imageKit 
import os 
from dotenv import load_dotenv 
import shutil 
import tempfile
from app.exceptions import raise_server_error_exception


load_dotenv()

car_routes=APIRouter(prefix="/api/v1/cars",tags=["Cars"])

@car_routes.get("/cars",response_model=list[carRespseSchema])
def get_all_cars(db:Session=Depends(get_session)):
    """
     Get all post.
    """
    return db.query(Car).order_by(Car.created_at)

@car_routes.post("/add-car",response_model=carRespseSchema)
async def add_car(
                  file:UploadFile=File(...),
                  brand:str=Form(""),
                  category:str=Form(""),
                  description:str=Form(""),
                  fuel_type:str=Form(""),
                  isAvaliable:bool=Form(True),
                  location:str=Form(""),
                  model:str=Form(""),
                  transmission:str=Form(""),
                  pricePerDay:int=Form(0),
                  seating_capacity:int=Form(0),
                  year:int=Form(0000),
                  current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    """
     adding car.
    """
    temp_file_path=None 
    # here we create a tempory file with same format from the file uploaded
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file,temp_file)
        
        # 3. Appeler la méthode d'upload
        upload_response=imageKit.files.upload(
            file=open(temp_file_path,"rb"),
            file_name=file.filename,
            folder="/cars",
            tags=["car", "voiture"],
            use_unique_file_name=True,
        )

        
        
        if upload_response.url: 
            new_car=Car(
                          brand=brand,
                          category=category,
                          description=description,
                          fuel_type=fuel_type,
                          isAvaliable=isAvaliable,
                          location=location,
                          model=model,
                          pricePerDay=pricePerDay,
                          seating_capacity=seating_capacity,
                          transmission=transmission,
                          year=year,
                          user_id=current_user.id,
                          file_type="video" if file.content_type.startswith("video/") else "image", 
                          url=upload_response.url,
                          file_name=upload_response.name)

            # to save this user to the database
            db.add(new_car)
            db.commit()
            db.refresh(new_car)
            return new_car 
        

    except Exception as e:
        raise_server_error_exception(detail=str(e)) 
    finally:
        # clean the temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

@car_routes.put("/avaliable/{cart_id}",response_model=carRespseSchema)
def toggle_Car_Avaliable(cart_id:uuid.UUID, current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    
    db_car=db.query(Car).filter(Car.id==cart_id).first()
    if not db_car:
        raise_not_found_exception(detail="car not found")

    
    db_car.isAvaliable= not db_car.isAvaliable 
    db.commit()
    db.refresh(db_car)

    return db_car


@car_routes.put("/{car_id}",response_model=carRespseSchema)
async def update_car_by_id(
                  car_id:uuid.UUID,
                  file:UploadFile=File(...),
                  brand:str=Form(""),
                  category:str=Form(""),
                  description:str=Form(""),
                  fuel_type:str=Form(""),
                  isAvaliable:bool=Form(True),
                  location:str=Form(""),
                  model:str=Form(""),
                  transmission:str=Form(""),
                  pricePerDay:int=Form(0),
                  seating_capacity:int=Form(0),
                  year:int=Form(0000),
                  current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    """
     adding car.
    """

    db_car=db.query(Car).filter(Car.id==car_id).first()

    if not db_car:
        raise_not_found_exception(detail="user does not found")

    temp_file_path=None 
    # here we create a tempory file with same format from the file uploaded
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file,temp_file)
        
        # 3. Appeler la méthode d'upload
        upload_response=imageKit.files.upload(
            file=open(temp_file_path,"rb"),
            file_name=file.filename,
            folder="/cars",
            tags=["car", "voiture"],
            use_unique_file_name=True,
        )
        
        if upload_response.url: 
            db_car.url=upload_response.url,
            db_car.file_name=upload_response.name


        db_car.pricePerDay=pricePerDay,
        db_car.seating_capacity=seating_capacity,
        db_car.transmission=transmission,
        db_car.year=year,
        db_car.brand=brand,
        db_car.category=category,
        db_car.description=description,
        db_car.fuel_type=fuel_type,
        db_car.isAvaliable=isAvaliable,
        db_car.location=location,
        db_car.model=model,                
        # to save this user to the database
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car 
        

    except Exception as e:
        raise_server_error_exception(detail=str(e)) 
    finally:
        # clean the temp file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()



@car_routes.delete("/{car_id}")
def delete_car(car_id:uuid.UUID,current_user:User=Depends(get_current_active_user),db:Session=Depends(get_session)):
    """
     delete a car by id.
    """
    db_car=db.query(Car).filter(Car.id==car_id).first()

    if not db_car:
        raise_not_found_exception(detail="car does not found")
    
    db.delete(db_car)
    db.commit()
    
    return {"message":"car deleted successfully"}