from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Post API")
# avoid cors origin for this domian "http://localhost:3000/"
app.add_middleware(
    CORSMiddleware, 
    allow_origins=["http://localhost:3000/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )



from app.api.v1.auth_routes import auth_routes
from app.api.v1.car_routes import car_routes
from app.api.v1.user_routes import user_routes
# include the routes
app.include_router(auth_routes)
app.include_router(user_routes)
app.include_router(car_routes)