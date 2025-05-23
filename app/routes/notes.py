from fastapi import APIRouter, Depends
import schemas
from models import User, Notes
from sqlalchemy import or_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi import HTTPException
from security import hash_password, verify_password, create_access_token, get_user_info
from fastapi.security import OAuth2PasswordRequestForm
import crud

router= APIRouter()

'''Get all notes'''
@router.get("")
async def get_all_notes(user_info: dict= Depends(get_user_info),db: AsyncSession = Depends(get_db)):
    return await crud.get_notes(user_info, db)

'''Save/Create Notes'''
@router.post("", response_model=schemas.NotesResponse)
async def save_note(note: schemas.NotesCreate, user_info: dict= Depends(get_user_info), db: AsyncSession= Depends(get_db)):
    return await crud.post_notes(user_info, db, note)

'''Delete Notes'''
@router.delete('/{note_id}',response_model=schemas.NotesResponse)
async def delete_note(note_id: int, user_info: dict= Depends(get_user_info), db: AsyncSession= Depends(get_db)):
    return await crud.delete_note(db,note_id, user_info)

'''Summarize Notes'''
@router.post("/summarize",response_model=schemas.NoteSummaryResponse)
async def summarize_notes(data: schemas.NoteSummaryRequest, user_info: dict= Depends(get_user_info)):
    return await crud.summarize_note(data, user_info)





