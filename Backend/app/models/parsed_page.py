from typing import List

from pydantic import BaseModel

from Backend.app.models.parsed_line import ParsedLine


class ParsedPage(BaseModel):
    """
    One PDF page.
    """

    page_number: int

    lines: List[ParsedLine] = []