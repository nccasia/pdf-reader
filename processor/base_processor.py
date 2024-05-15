from typing import BinaryIO
from pypdf import PdfReader
import docx2txt


def convert_pdf_to_text(file_contents):
    reader = PdfReader(file_contents)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
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
        elif file_extensiion in [".doc", ".docx"]:
            attachment_data = docx2txt.process(file)
        else:
            raise ValueError(
                "Invalid file extension. Supported file extensions are .txt, .doc, .docx, .pdf."
            )
        return attachment_data

    def check_number_of_tokens(self, text):
        raise NotImplementedError

    def get_response(self, attachment_data, year):
        raise NotImplementedError
