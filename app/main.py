import os

from dotenv import load_dotenv
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.cv_router import router as cv_router

load_dotenv()

CORS_ORIGINS = os.getenv("CORS_ORIGIN", "*").strip().strip('"').split('", "')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv_router)


@app.get("/check-connection")
def check_connection():
    return Response(status_code=200)
