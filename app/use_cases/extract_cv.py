import json
from typing import Any, BinaryIO, List

from app.domain.interfaces import IFileParser, ILLMClient
from app.infrastructure.llm.anthropic_client import CV_LIST_SCHEMA, CV_SCHEMA
from app.infrastructure.llm.prompts import (
    MULTI_SYSTEM_PROMPT,
    MULTI_USER_PROMPT,
    SYSTEM_PROMPT,
    USER_PROMPT,
)
from app.infrastructure.parsers.url_fetcher import URLFetcher


class ExtractCVUseCase:
    def __init__(
        self,
        file_parser: IFileParser,
        llm_client: ILLMClient,
        url_fetcher: URLFetcher,
    ) -> None:
        self._parser = file_parser
        self._llm = llm_client
        self._fetcher = url_fetcher

    def extract_single(self, file: BinaryIO, extension: str) -> Any:
        text = self._parser.parse_text(file, extension)
        return self._complete_single(text)

    def extract_single_ocr(self, file: BinaryIO, extension: str) -> Any:
        text = self._parser.parse_ocr(file, extension)
        return self._complete_single(text)

    def extract_multi_from_urls(self, urls: List[str]) -> Any:
        parts = []
        for i, url in enumerate(urls, 1):
            parts.append(f"\n---------- This is CV {i} ----------\n")
            parts.append(self._fetcher.fetch_text(url))
            parts.append("\n")
        return self._complete_multi("".join(parts))

    def extract_multi_from_urls_ocr(self, urls: List[str]) -> Any:
        parts = []
        for i, url in enumerate(urls, 1):
            parts.append(f"\n---------- This is CV {i} ----------\n")
            parts.append(self._fetcher.fetch_text_ocr(url))
            parts.append("\n")
        return self._complete_multi("".join(parts))

    def _complete_single(self, text: str) -> Any:
        content = self._llm.complete(SYSTEM_PROMPT, USER_PROMPT.format(attachment_data=text), CV_SCHEMA)
        try:
            return json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return self._parse_json(content, mode="single")

    def _complete_multi(self, text: str) -> Any:
        content = self._llm.complete(MULTI_SYSTEM_PROMPT, MULTI_USER_PROMPT.format(attachment_data=text), CV_LIST_SCHEMA)
        try:
            return json.loads(content)
        except (json.JSONDecodeError, TypeError):
            return self._parse_json(content, mode="multi")

    def _parse_json(self, response: str, mode: str) -> Any:
        if mode == "single":
            start = response.find("{")
            end = response.rfind("}") + 1
        else:
            start = response.find("[")
            end = response.rfind("]") + 1
        return json.loads(response[start:end])
