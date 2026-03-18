from abc import ABC, abstractmethod
from typing import BinaryIO


class IFileParser(ABC):
    @abstractmethod
    def parse_text(self, file: BinaryIO, extension: str) -> str: ...

    @abstractmethod
    def parse_ocr(self, file: BinaryIO, extension: str) -> str: ...


class ILLMClient(ABC):
    @abstractmethod
    def complete(self, system_prompt: str, user_content: str) -> str: ...
