from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, notes
from database import Base, engine

"""Initialization"""
app = FastAPI(title="AI Notes Generation",
             description="APIs for Gemini Notes",
            version="1.0.0")

"""Setting cors"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],  # Control over allowed hosts
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=['Notes Authentication'])
app.include_router(notes.router, prefix="/notes", tags=["Notes API"])

# Correct async startup event
@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to AI Notes API"}
    






