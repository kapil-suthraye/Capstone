from typing import Literal
from uuid import uuid4

from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    """
    Final chunk stored in Pinecone.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    text: str

    page_start: int

    page_end: int

    source_file: str

    document_category: str = "Medical Record"

    section_heading: str = "General"

    section_path: list[str] = []

    chunk_type: Literal[
        "text",
        "table"
    ] = "text"

    token_count: int = 0

    metadata: dict = {}