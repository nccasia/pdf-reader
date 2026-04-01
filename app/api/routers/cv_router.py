import io
import os

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from app.api.schemas import URLList
from app.config import ALLOWED_EXTENSIONS
from app.infrastructure.llm.factory import create_llm_client
from app.infrastructure.parsers.file_parser import FileParser
from app.infrastructure.parsers.url_fetcher import URLFetcher
from app.use_cases.extract_cv import ExtractCVUseCase

router = APIRouter()

_use_case = ExtractCVUseCase(
    file_parser=FileParser(),
    llm_client=create_llm_client(),
    url_fetcher=URLFetcher(),
)


def _validate_file(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Supported: .doc, .docx, .pdf",
        )


@router.post("/extract-cv")
async def extract_cv(file: UploadFile = File(...)):
    _validate_file(file)
    try:
        result = _use_case.extract_single(
            io.BytesIO(await file.read()), os.path.splitext(file.filename)[1]
        )
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-cv-vision")
async def extract_cv_vision(file: UploadFile = File(...)):
    _validate_file(file)
    try:
        result = _use_case.extract_single_ocr(
            io.BytesIO(await file.read()), os.path.splitext(file.filename)[1]
        )
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-multifile")
async def extract_multifile(urls: URLList):
    if len(urls.urls) > 10:
        raise HTTPException(status_code=400, detail="Too many URLs. Maximum is 10.")
    try:
        result = _use_case.extract_multi_from_urls(urls.urls)
        return JSONResponse(content=result, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-multifile-vision")
async def extract_multifile_vision(urls: URLList):
    if len(urls.urls) > 10:
        raise HTTPException(status_code=400, detail="Too many URLs. Maximum is 10.")
    try:
        result = _use_case.extract_multi_from_urls_ocr(urls.urls)
        return JSONResponse(content=result, status_code=200)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
