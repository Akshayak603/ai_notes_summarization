import jwt
import os
from datetime import timedelta, datetime
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User

'''loading environment variables'''
load_dotenv()

pass_context= CryptContext(schemes=['brypt'], deprecated='auto')

async def hash_password(password:str):
    """Hash a password for storing."""
    return pass_context.hash(password)

async def verify_password(stored_pswd:str, given_passwd:str):
    """Verify a password against a stored hash."""
    return pass_context.verify(given_passwd, stored_pswd)

'''JWT Implementation'''
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

'''creating access token'''
async def create_access_token(data:dict, expires_delta:int=ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY , ALGORITHM)
    return encoded_jwt

'''decoding access token'''
async def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        return payload
    except:
        return "Invalid Token or Token has expired"
    

'''get user info'''
oauth= OAuth2PasswordBearer(tokenUrl=('auth/login'))
async def get_user_info(token: str= Depends(oauth), db: AsyncSession= Depends(get_db)):
    '''get user info from token'''
    try:
        payload= await decode_access_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid Token or Token has expired")
        
        username= payload.get('username')
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid Token or Token has expired")
        
        stmt= select(User).where(User.username==username)
        result= await db.execute(stmt)
        user_obj= result.scalars().first()

        if not user_obj:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user_obj
    except:
        raise HTTPException(status_code=401, detail="Invalid Token or Token has expired")
        

