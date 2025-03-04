import io
from PIL import Image
import fitz
from google.cloud import vision
from app.constants import ALLOWED_EXTENSIONS
import PyPDF2
from fastapi import HTTPException
import requests


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def convert_pdf_to_images(file_contents):
    images = []
    pdf_file = fitz.open("pdf", file_contents)
    for page_index in range(len(pdf_file)):
        page = pdf_file[page_index]
        image = page.get_pixmap(dpi=300)
        image_data = image.tobytes()
        pil_image = Image.open(io.BytesIO(image_data))
        width, height = pil_image.size
        resized_image = pil_image.resize((int(width * 0.8), int(height * 0.8)))

        images.append(resized_image)

    return images


def ocr_image(pil_image):
    client = vision.ImageAnnotatorClient()
    with io.BytesIO() as output:
        pil_image.save(output, format="JPEG")
        content = output.getvalue()
    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(f"{response.error.message}")
    return texts[0].description if texts else ""


def ocr_pdf(file_contents):
    images = convert_pdf_to_images(file_contents)

    full_text = ""
    for pil_image in images:
        text = ocr_image(pil_image)
        full_text += text + "\n"

    return full_text


def process_multi_file(urls):
    data_cv = []
    i = 1
    for url in urls.urls:
        response = requests.get(url)
        if response.status_code == 200:
            content_type = response.headers["content-type"]
            if "pdf" in content_type:
                text = ocr_pdf(response.content)
                data_cv.append(f"\n---------- This is CV {i} ----------\n")
                data_cv.append(text)
                i += 1
            elif "doc" or "docx" in content_type:
                pdf_document = fitz.open(stream=io.BytesIO(response.content))
                text = ""
                for page_number, page in enumerate(pdf_document):
                    text += page.get_text()
                data_cv.append(f"\n---------- This is CV {i} ----------\n")
                data_cv.append(text)
                i += 1
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"From URL: {url}: invalid file extension. Supported file extensions are .doc, .docx, .pdf",
                )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to fetch data from URL: {url}. Status code: {response.status_code}",
            )
    attachment_data = "".join(data_cv)
    return attachment_data


def convert_pdf_to_text(file_contents):
    reader = PyPDF2.PdfReader(file_contents)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    return text


def extract_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        pdf_document = fitz.open(stream=io.BytesIO(response.content))
        text = ""
        for page_number, page in enumerate(pdf_document):
            text += page.get_text()

        return text
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to fetch data from URL: {url}. Status code: {response.status_code}",
        )
