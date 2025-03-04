from typing import BinaryIO
import docx2txt
from app.utils.file_utils import ocr_pdf, convert_pdf_to_text
import requests
import json
import os
from .prompt import SYSTEM_PROMPT, USER_PROMPT, MULTI_SYSTEM_PROMPT, MULTI_USER_PROMPT
from dotenv import load_dotenv
load_dotenv()

class BaseProcessor:
    def __init__(self): ...

    def process_text(
        self,
        file: BinaryIO,
        file_extension: str,
    ):
        file_extension = file_extension.lower()
        if file_extension == ".pdf":
            attachment_data = convert_pdf_to_text(file)
        elif file_extension in [".doc", ".docx"]:
            attachment_data = docx2txt.process(file)
        else:
            raise ValueError(
                "Invalid file extension. Supported file extensions are .txt, .doc, .docx, .pdf."
            )
        return attachment_data

    def process(
        self,
        file: BinaryIO,
        file_extensiion: str,
    ):
        file_extensiion = file_extensiion.lower()
        if file_extensiion == ".pdf":
            attachment_data = ocr_pdf(file)
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


class GeminiProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.headers = {"Content-Type": "application/json"}
        self.api_key = os.getenv("GEMINI_API_KEY")
        GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL_NAME}:generateContent?key={self.api_key}"

    def check_number_of_tokens(self, text):
        pass

    def _get_payload(self, attachment_data, system_prompt, user_prompt):
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{system_prompt}\n{user_prompt.format(attachment_data=attachment_data)}",
                        }
                    ]
                }
            ],
        }

        return payload

    def _get_response(self, payload, response_type):
        response = requests.post(
            self.url,
            headers=self.headers,
            json=payload,
        )

        response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        try:
            if response_type == "single":
                start_pos = response.find("{")
                end_pos = response.rfind("}") + 1
            else:  # assuming response_type == "multi"
                start_pos = response.find("[")
                end_pos = response.rfind("]") + 1

            json_string = response[start_pos:end_pos]
            data = json.loads(json_string)
            return data
        except KeyError:
            print("KeyError: Some key is missing in the JSON response")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_response(self, attachment_data):
        payload = self._get_payload(attachment_data, SYSTEM_PROMPT, USER_PROMPT)
        return self._get_response(payload, "single")

    def get_response_multi(self, attachment_data):
        payload = self._get_payload(
            attachment_data, MULTI_SYSTEM_PROMPT, MULTI_USER_PROMPT
        )
        return self._get_response(payload, "multi")
