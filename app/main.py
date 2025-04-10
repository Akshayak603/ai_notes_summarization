from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, notes
from database import init_db, Base, engine

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
app.include_router()

@app.on_event('starup')
async def startup_event():
    init_db()
    Base.metadata.create_all(engine)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to AI Notes API"}
    






