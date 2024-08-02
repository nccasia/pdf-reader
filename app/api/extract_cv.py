import os
import io
from app.utils.file_utils import process_multi_file, extract_text_from_url
from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.extract_cv import GeminiProcessor
from app.utils.file_utils import allowed_file
from fastapi.responses import JSONResponse
from app.schemas.CV import URLList

router = APIRouter()

processor = GeminiProcessor()


@router.post("/extract-cv")
async def extract_cv(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Supported file extensions are .doc, .docx, .pdf",
        )
    try:
        attachment_data = processor.process_text(
            io.BytesIO(await file.read()), os.path.splitext(file.filename)[1]
        )
        response = processor.get_response(attachment_data)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-cv-vision")
async def extract_cv_vision(file: UploadFile = File(...)):
    if file.filename == "":
        raise HTTPException(status_code=400, detail="No selected file")
    if not allowed_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail="Invalid file extension. Supported file extensions are .doc, .docx, .pdf",
        )
    try:
        attachment_data = processor.process(
            io.BytesIO(await file.read()), os.path.splitext(file.filename)[1]
        )
        response = processor.get_response(attachment_data)
        return JSONResponse(content=response, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/extract-multifile")
async def extract_multifile(urls: URLList):
    if len(urls.urls) > 10:
        raise HTTPException(
            status_code=400, detail="Too many URLs provided. Maximum limit is 10."
        )
    data_cv = []
    i = 1
    for url in urls.urls:
        data_cv.append(f"\n---------- This is CV {i} ----------\n")
        i += 1
        data_cv.append(extract_text_from_url(url))
        data_cv.append("\n")
    text = "".join(data_cv)
    response = processor.get_response_multi(text)
    return JSONResponse(content=response, status_code=200)


@router.post("/extract-multifile-vision")
async def extract_multifile_vision(urls: URLList):
    if len(urls.urls) > 10:
        raise HTTPException(
            status_code=400, detail="Too many URLs provided. Maximum limit is 10."
        )

    attachment_data = process_multi_file(urls=urls)
    result = processor.get_response_multi(attachment_data)
    return JSONResponse(content=result, status_code=200)
