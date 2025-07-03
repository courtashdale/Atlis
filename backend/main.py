# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend access during dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI backend running"}

@app.get("/api/hello")
def read_root():
    return {"message": "FastAPI says hi!"}

@app.get("/health")
def health():
    return {"status": "ok"}