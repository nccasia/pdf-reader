import io

import fitz
import requests
from fastapi import HTTPException

from app.infrastructure.parsers.file_parser import FileParser


class URLFetcher:
    def __init__(self) -> None:
        self._parser = FileParser()

    def fetch_text(self, url: str) -> str:
        """Extract text from a URL via fitz (no OCR)."""
        response = self._download(url)
        doc = fitz.open(stream=io.BytesIO(response.content))
        return "".join(page.get_text() for page in doc)

    def fetch_text_ocr(self, url: str) -> str:
        """Extract text from a URL via OCR, choosing strategy based on content type."""
        response = self._download(url)
        content_type = response.headers.get("content-type", "")
        if "pdf" in content_type:
            return self._parser._ocr_pdf(response.content)
        if "doc" in content_type:
            doc = fitz.open(stream=io.BytesIO(response.content))
            return "".join(page.get_text() for page in doc)
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported content type from URL: {url}",
        )

    def _download(self, url: str) -> requests.Response:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch data from URL: {url}. Status code: {response.status_code}",
            )
        return response
