from pathlib import Path
from typing import List

from pypdf import PdfReader

from Backend.app.models.parsed_document import ParsedDocument
from Backend.app.models.parsed_page import ParsedPage
from Backend.app.models.parsed_line import ParsedLine


class PDFParser:
    """
    Production PDF parser.

    Extracts:
      - text
      - font size
      - font name
      - x/y coordinates
      - bold heuristic

    Output:
        ParsedDocument
            -> ParsedPage
                -> ParsedLine
    """

    def __init__(self):
        pass

    def parse(self, pdf_path: str) -> ParsedDocument:

        reader = PdfReader(pdf_path)

        parsed_pages: List[ParsedPage] = []

        for page_number, page in enumerate(reader.pages, start=1):

            extracted_lines: List[ParsedLine] = []

            line_buffer = {}

            def visitor(text, cm, tm, font_dict, font_size):

                if text is None:
                    return

                text = text.strip()

                if not text:
                    return

                font_name = ""

                if font_dict:
                    font_name = font_dict.get("/BaseFont", "")

                x = float(tm[4])
                y = float(tm[5])

                bold = False

                if "Bold" in font_name:
                    bold = True

                y_key = round(y, 1)

                if y_key not in line_buffer:

                    line_buffer[y_key] = []

                line_buffer[y_key].append(
                    ParsedLine(
                        text=text,
                        font_size=float(font_size),
                        font_name=font_name,
                        x=x,
                        y=y,
                        is_bold=bold,
                    )
                )

            page.extract_text(visitor_text=visitor)

            ordered_lines = []

            #
            # Sort from top -> bottom
            #
            for y in sorted(line_buffer.keys(), reverse=True):

                fragments = sorted(
                    line_buffer[y],
                    key=lambda item: item.x,
                )

                merged_text = " ".join(
                    fragment.text for fragment in fragments
                ).strip()

                if not merged_text:
                    continue

                first = fragments[0]

                ordered_lines.append(
                    ParsedLine(
                        text=merged_text,
                        font_size=first.font_size,
                        font_name=first.font_name,
                        x=first.x,
                        y=first.y,
                        is_bold=first.is_bold,
                    )
                )

            parsed_pages.append(
                ParsedPage(
                    page_number=page_number,
                    lines=ordered_lines,
                )
            )

        return ParsedDocument(
            filename=Path(pdf_path).name,
            pages=parsed_pages,
        )