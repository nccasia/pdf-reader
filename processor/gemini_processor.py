import requests
import json
from .base_processor import BaseProcessor
import os
from .prompt import SYSTEM_PROMPT, USER_PROMPT

GEMINI_MAX_TOKENS = 1048576
GEMINI_MODEL_NAME = "gemini-1.5-pro-latest"


class GeminiProcessor(BaseProcessor):
    def __init__(self):
        super().__init__()
        self.headers = {"Content-Type": "application/json"}
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key={self.api_key}"

    def check_number_of_tokens(self, text):
        pass

    def get_gemini_payload(self, attachment_data):
        with open("fields.txt", "r") as f:
            target_fields = f.read()
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"{SYSTEM_PROMPT}\n{USER_PROMPT.format(attachment_data=attachment_data, target_fields=target_fields)}",
                        }
                    ]
                }
            ],
        }
        return payload

    def get_response(self, attachment_data):
        response = requests.post(
            self.url,
            headers=self.headers,
            json=self.get_gemini_payload(attachment_data),
        )
        response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        try:
            start_pos = response.find("{")
            end_pos = response.rfind("}") + 1

            json_string = response[start_pos:end_pos]
            data = json.loads(json_string)
            return data
        except KeyError:
            print("KeyError: Some key is missing in the JSON response")
        except Exception as e:
            print(f"An error occurred: {e}")
