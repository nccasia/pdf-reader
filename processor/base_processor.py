from typing import BinaryIO
import fitz


def convert_pdf_to_text(file_contents):
    text = ""
    pdf_document = fitz.open(stream=file_contents, filetype="pdf")
    if pdf_document:
        for page_number in range(len(pdf_document)):
            page = pdf_document.load_page(page_number)
            text += page.get_text()
        pdf_document.close()
    else:
        print("Error: Cannot open or process the PDF document.")
    return text


class BaseProcessor:
    def __init__(self): ...

    def process(
        self,
        file: BinaryIO,
        file_extensiion: str,
    ):
        file_extensiion = file_extensiion.lower()

        if file_extensiion == ".pdf":
            attachment_data = convert_pdf_to_text(file)
        elif file_extensiion in [".txt", ".doc", ".docx"]:
            attachment_data = file.read()
        else:
            raise ValueError(
                "Invalid file extension. Supported file extensions are .txt, .doc, .docx, .pdf."
            )
        return attachment_data

    def check_number_of_tokens(self, text):
        raise NotImplementedError

    def get_response(self, attachment_data, year):
        raise NotImplementedError
