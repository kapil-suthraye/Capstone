from __future__ import annotations

import hashlib
import re
from typing import List

from Backend.app.domain.models.document_chunk import DocumentChunk
from Backend.app.domain.models.paragraph import Paragraph
from Backend.app.domain.models.parsed_document import ParsedDocument
from Backend.app.domain.models.parsed_line import ParsedLine

from Backend.app.services.ingestion.tokenizer import Tokenizer
from Backend.app.services.ingestion.heading_detector import HeadingDetector


class Chunker:
    """
    Production chunker.

    Workflow

    ParsedDocument
            ↓
    Sections
            ↓
    Paragraphs
            ↓
    Token Splitter
            ↓
    DocumentChunks
    """

    DEFAULT_CATEGORY = "Medical Record"

    MAX_TOKENS = 700

    MIN_TOKENS = 100

    OVERLAP = 75

    def __init__(self):

        self.tokenizer = Tokenizer()

        self.heading_detector = HeadingDetector()

    ###########################################################
    # Public API
    ###########################################################

    def chunk_document(
        self,
        document: ParsedDocument,
    ) -> List[DocumentChunk]:

        paragraphs = self.build_paragraphs(document)

        chunks = []

        for paragraph in paragraphs:

            paragraph_chunks = self.chunk_paragraph(
                paragraph,
                document.filename,
            )

            chunks.extend(paragraph_chunks)

        return chunks

    ###########################################################
    # Paragraph Builder
    ###########################################################

    def build_paragraphs(
        self,
        document: ParsedDocument,
    ) -> List[Paragraph]:

        paragraphs = []

        current_heading = "General"

        section_path = []

        paragraph_lines = []

        paragraph_page = 1

        for page in document.pages:

            paragraph_page = page.page_number

            for line in page.lines:

                text = self.clean_text(line.text)

                if not text:
                    continue

                #
                # Heading
                #
                if self.heading_detector.is_heading(line):

                    #
                    # Flush current paragraph
                    #
                    if paragraph_lines:

                        paragraphs.append(

                            Paragraph(

                                heading=current_heading,

                                page=paragraph_page,

                                lines=paragraph_lines.copy(),

                                section_path=section_path.copy()

                            )

                        )

                        paragraph_lines.clear()

                    current_heading = text

                    section_path = self.update_section_path(
                        section_path,
                        text,
                    )

                    continue

                #
                # Blank line
                #
                if text == "":

                    if paragraph_lines:

                        paragraphs.append(

                            Paragraph(

                                heading=current_heading,

                                page=paragraph_page,

                                lines=paragraph_lines.copy(),

                                section_path=section_path.copy()

                            )

                        )

                        paragraph_lines.clear()

                    continue

                paragraph_lines.append(text)

        if paragraph_lines:

            paragraphs.append(

                Paragraph(

                    heading=current_heading,

                    page=paragraph_page,

                    lines=paragraph_lines,

                    section_path=section_path,

                )

            )

        return paragraphs

    ###########################################################
    # Section Hierarchy
    ###########################################################

    def update_section_path(

        self,

        current_path,

        heading,

    ):

        """
        Very simple hierarchy.

        Later we improve using font size.
        """

        if len(current_path) == 0:

            return [heading]

        #
        # Numbered heading
        #

        if re.match(r"^\d+", heading):

            return current_path + [heading]

        #
        # Otherwise replace current section
        #

        return [heading]

    ###########################################################
    # Helpers
    ###########################################################

    @staticmethod
    def clean_text(text):

        text = text.replace("\t", " ")

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    ###########################################################
    # Chunk Paragraph
    ###########################################################

    def chunk_paragraph(

        self,

        paragraph: Paragraph,

        filename: str,

    ):

        """
        Placeholder.

        Part B implements production token chunking.
        """

        return self.simple_chunk(

            paragraph,

            filename,

        )