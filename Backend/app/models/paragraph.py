from typing import List

from pydantic import BaseModel


class Paragraph(BaseModel):
    """
    Intermediate representation used by the chunker.
    """

    heading: str

    page: int

    lines: List[str]

    section_path: List[str] = []