from pydantic import BaseModel
from typing import List


class URLList(BaseModel):
    urls: List[str]
