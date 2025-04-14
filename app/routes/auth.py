from fastapi import APIRouter, Depends
import schemas
from models import User
from sqlalchemy import or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import HTTPException
from security import hash_password, verify_password, create_access_token, get_user_info
from fastapi.security import OAuth2PasswordRequestForm

router= APIRouter()

'''Registration'''
@router.post('/register', response_model=schemas.UserRegisterResponse)
async def register_user(user: schemas.UserRegister, db: AsyncSession= Depends(get_db)):
    stmt= select(User).where(
        or_(
            func.lower(User.username)==user.username.lower(),
            func.lower(User.email)==user.email.lower()
    )
    )
    result= await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail='Username or Email already exists')
    
    hashPassword= await hash_password(user.password)
    """Insert data now"""
    user_data= User(username=user.username, email=user.email, hashed_password=hashPassword)
    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    return user_data
    

'''login'''
@router.post('/login')
async def login_user(user: OAuth2PasswordRequestForm= Depends(), db: AsyncSession= Depends(get_db)):
    stmt= select(User).where(or_(
            func.lower(User.username) == user.username.lower(),
            func.lower(User.email) == user.username.lower()
        ))
    result= await db.execute(stmt)
    existing_user = result.scalar_one_or_none()
    if not existing_user or not await verify_password(existing_user.hashed_password, user.password):
        raise HTTPException(status_code=401, detail='Invalid username or password')
    token= await create_access_token({"username": existing_user.username})
    return {"access_token": token, "token_type": "bearer"}


'''Getting user info'''
@router.get('/me', response_model=schemas.UserResponse)
async def get_user(user: dict=Depends(get_user_info)):
    return user




