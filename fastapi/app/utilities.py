from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError,InvalidHashError
from dotenv import load_dotenv
from datetime import timedelta,datetime,timezone
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError,PyJWKError
import os
from fastapi import HTTPException,status,Depends
from sqlalchemy.orm import Session 
from app.db.dependencies import get_session
from app.db.models import User 
from app.schemas import tokenResponseSchema
from fastapi.security import OAuth2PasswordBearer
from app.exceptions import raise_unauthorized_exception,raise_not_found_exception
import uuid


# carregar os variable de ambiente na nossa sistema
load_dotenv()


ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# The tokenUrl is the path where the client should send the username/password
# to receive a token (e.g., POST /api/v1/auth/token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

# AUTHENTICATION
password_hasher=PasswordHasher()

SALT =os.getenv("SALT") 
#  # Hash the user's password before storing it
def get_pwd_hash(plain_password:str)->str:
    password_with_salt=SALT+plain_password
    return password_hasher.hash(password_with_salt)


# verify decreapt the user password
def verify_password(hashed_pwd:str ,plain_pwd:str)->bool:
    # backend message
    # print(f"DEBUG: Hashed Password Retrieved: '{hashed_pwd}'") # <-- ADD THIS LINE
    # print(f"DEBUG: plain Password : '{plain_pwd}'") # <-- ADD THIS LINE
    password_with_salt=SALT+plain_pwd
    try:
        return password_hasher.verify(hashed_pwd,password_with_salt) # This line raises the error
    except VerifyMismatchError:
         # backend message
        print("Incorrect username or password")
        return False
    except InvalidHashError:
        # backend message
        print("CRITICAL: Invalid hash format detected. Check your DB storage size.")
        return False
    
    except Exception:
            # Catch other potential errors (like InvalidHashError, as seen previously)
            # and treat them as an authentication failure to avoid leaking details.
            # raise HTTPException(
            #     status_code=status.HTTP_401_UNAUTHORIZED,
            #     detail="Authentication failed due to system error.",
            #     headers={"WWW-Authenticate": "Bearer"},
            # )
        print("CRITICAL: Authentication failed due to system error..")
        return False

# create a user token
def create_access_token(user_id:uuid.UUID, user_email: str)->str:
    """Creates a JWT token with expiration and user claims."""

    # 2. Define the payload (claims)
    payload = {
        # Standard Claims
        "sub": str(user_id), # Subject (user identifier)#the sub can be anything (user_email etc..)
        "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), # Token expiration time (30 min)
        "iat": datetime.now(timezone.utc), # Issued at time
        # Custom Claims
        "email": user_email
    }

    # get the "SECRET_KEY" environment variable from the env file
    SECRET_KEY=os.getenv("SECRET_KEY")
    ALGORITHM =os.getenv("ALGORITHM")
    encoded_jwt= jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt





# verify the token if valid
def verify_access_token(token: str)-> dict | None:
    """
    Decodes and validates the JWT token.
    Returns the payload dictionary if valid, otherwise returns None.
    """
    ALGORITHM = os.getenv("ALGORITHM")

    try:
        # jwt.decode() performs signature verification and expiration check automatically.
        payload = jwt.decode(
            token,
            key=os.getenv("SECRET_KEY"),        # The key used for signing/verification
            algorithms=[ALGORITHM] # List of allowed algorithms
        )
        # get the user_id from the token
        user_id=payload.get("sub")
        if user_id is None: #if there is no user_id in the payload
            raise_unauthorized_exception(detail="Could not verify credentials")

        # If decoding succeeds, the token is valid and not expired
        print("Token verified successfully.")
        return payload
    
 
    except ExpiredSignatureError:
        # Handles the case where the 'exp' claim is in the past
        # raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
        #                          detail="Verification Failed: Token has expired.",
        #                           headers={"www-Authenticate":"Bearer"})
        print("Verification Failed: Token has expired.")
        return None
        
    except InvalidTokenError:
        # Handles invalid signatures, invalid algorithms, or malformed tokens
        # raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
        #                          detail="Verification Failed: Invalid signature, algorithm, or token format.",
        #                           headers={"www-Authenticate":"Bearer"})
        print("Verification Failed: Invalid signature, algorithm, or token format.")
        return None
        
    except Exception as e:

        # raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,
        #                          detail="Verification Failed due to an unexpected error: {e}",
        #                           headers={"www-Authenticate":"Bearer"})
        print(f"Verification Failed due to an unexpected error: {e}")
        return None






async def get_current_user(token:str=Depends(oauth2_scheme),db:Session=Depends(get_session)):
    """dependency to encode and validate the JWT from the authorition header 
    this function run on every protected route
    """
    # get data from token
    if token is None:
        raise_unauthorized_exception(detail="token expired")
        
    
    user_payload=verify_access_token(token)
    
    current_user=db.query(User).filter(User.email==user_payload.get("email")).first()
    current_user_id=user_payload.get("sub")

    if current_user is None or current_user_id is None:
        raise_unauthorized_exception(detail="Could not validate user")       

    return current_user


async def get_current_active_user(current_user:User=Depends(get_current_user)):
    
    if not current_user.active: 
        raise_not_found_exception(detail="Inactive user")

    return current_user


