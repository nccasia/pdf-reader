import os
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from app.api.extract_cv import router as extract_cv_router
from dotenv import load_dotenv
load_dotenv()

CORS_ORIGINs = os.getenv("CORS_ORIGIN", "*").strip().strip('"').split('", "')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINs,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(extract_cv_router)


@app.get("/check-connection")
def check_connection():
    return Response(status_code=200)
