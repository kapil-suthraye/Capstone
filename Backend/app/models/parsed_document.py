from typing import List

from pydantic import BaseModel

from Backend.app.models.parsed_page import ParsedPage


class ParsedDocument(BaseModel):
    """
    Parsed PDF.
    """

    filename: str

    pages: List[ParsedPage] = []

    metadata: dict = {}