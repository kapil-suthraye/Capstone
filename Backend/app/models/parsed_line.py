from pydantic import BaseModel, Field


class ParsedLine(BaseModel):
    """
    Represents one logical line extracted from a PDF.
    """

    text: str = Field(..., description="Line text")

    font_size: float = Field(
        default=12.0,
        description="Detected font size"
    )

    font_name: str = Field(
        default="",
        description="PDF font name"
    )

    x: float = Field(
        default=0.0,
        description="X coordinate"
    )

    y: float = Field(
        default=0.0,
        description="Y coordinate"
    )

    is_bold: bool = Field(
        default=False,
        description="Bold font heuristic"
    )

    is_heading: bool = Field(
        default=False,
        description="Heading detected"
    )

    is_table_row: bool = Field(
        default=False,
        description="Detected table row"
    )