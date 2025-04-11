from models import Notes, User
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from utils.helpers import call_gemini
from sqlalchemy import select
import schemas

'''Get all notes'''
async def get_notes(user_info:User, db:AsyncSession):
    stmt= select(Notes).where(Notes.owner_id==user_info.id)
    result= await db.execute(stmt)
    return result.scalars().all()

'''Post all notes'''
async def post_notes(user_info:User, db:AsyncSession, notes_data: schemas.NotesCreate):
    new_note= Notes(**notes_data.dict(), owner_id= user_info.id)
    db.add(new_note)
    await db.commit()
    await db.refresh(new_note)
    return new_note

'''Delete note'''
async def delete_note(db:AsyncSession, note_id:int, user_info: User):
    note= await db.get(Notes, note_id)
    if not note or note.owner_id != user_info.id:
        raise HTTPException(status_code=404, detail="Note not found or Anauthorized")
    await db.delete(note)
    await db.commit()
    return note


'''Summarize note via Gemini'''
async def summarize_note(data:dict):
    print(f"Data: {data}")
    content = data.content
    print(f"Content: {content}")

    # If previous_summary exists, modify prompt accordingly
    if data.previous_summary:
        prompt = (
            "The user was not satisfied with the previous summary."
            "Do not mention anything about content or previous summary, just summarize content more accurately.\n"
            "Please generate a better summary of the following note content.\n\n"
            f"Content:\n{content}\n\n"
            f"Previous Summary:\n{data.previous_summary}"
        )
    else:
        prompt = f"Summarize the following note content:\n\n{content}"

    summary = await call_gemini(prompt=prompt)
    print(f"Summary: {summary}")
    return {"summary": summary}


    
    
