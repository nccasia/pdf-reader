from typing import List, Optional

from pydantic import BaseModel


class URLList(BaseModel):
    urls: List[str]


class CVData(BaseModel):
    fullname: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    dob: Optional[str] = None
    address: Optional[str] = None
    gender: Optional[str] = None
    position: Optional[str] = None
    note: Optional[str] = None
