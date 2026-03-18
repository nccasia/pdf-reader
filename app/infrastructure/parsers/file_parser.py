import io
from typing import BinaryIO

import docx2txt
import fitz
import PyPDF2
from PIL import Image
from google.cloud import vision

from app.domain.interfaces import IFileParser


class FileParser(IFileParser):
    def parse_text(self, file: BinaryIO, extension: str) -> str:
        ext = extension.lower()
        if ext == ".pdf":
            return self._pdf_to_text(file)
        if ext in (".doc", ".docx"):
            return docx2txt.process(file)
        raise ValueError(f"Unsupported file extension: {extension}")

    def parse_ocr(self, file: BinaryIO, extension: str) -> str:
        ext = extension.lower()
        if ext == ".pdf":
            return self._ocr_pdf(file)
        if ext in (".doc", ".docx"):
            return docx2txt.process(file)
        raise ValueError(f"Unsupported file extension: {extension}")

    def _pdf_to_text(self, file: BinaryIO) -> str:
        reader = PyPDF2.PdfReader(file)
        return "".join(page.extract_text() or "" for page in reader.pages)

    def _ocr_pdf(self, source) -> str:
        data = source.read() if hasattr(source, "read") else source
        images = self._pdf_to_images(data)
        return "\n".join(self._ocr_image(img) for img in images)

    def _pdf_to_images(self, file_contents: bytes) -> list:
        images = []
        pdf = fitz.open("pdf", file_contents)
        for page in pdf:
            pixmap = page.get_pixmap(dpi=300)
            pil_image = Image.open(io.BytesIO(pixmap.tobytes()))
            w, h = pil_image.size
            images.append(pil_image.resize((int(w * 0.8), int(h * 0.8))))
        return images

    def _ocr_image(self, pil_image: Image.Image) -> str:
        client = vision.ImageAnnotatorClient()
        with io.BytesIO() as buf:
            pil_image.save(buf, format="JPEG")
            content = buf.getvalue()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise RuntimeError(response.error.message)
        texts = response.text_annotations
        return texts[0].description if texts else ""
