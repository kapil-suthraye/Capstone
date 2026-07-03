from __future__ import annotations

import hashlib
import re
from typing import List

from Backend.app.models.document_chunk import DocumentChunk
from Backend.app.models.paragraph import Paragraph
from Backend.app.models.parsed_document import ParsedDocument
from Backend.app.models.parsed_line import ParsedLine

from Backend.app.utils.heading_detector import HeadingDetector
from Backend.app.utils.token_counter import count_tokens


class Chunker:
    """
    Production clinical chunker.

    Pipeline

    ParsedDocument
          ↓
    Section Detection
          ↓
    Paragraph Builder
          ↓
    Sentence Splitter
          ↓
    Token Chunking
          ↓
    DocumentChunk
    """

    MAX_TOKENS = 700

    MIN_TOKENS = 100

    TOKEN_OVERLAP = 75

    DEFAULT_CATEGORY = "Medical Record"

    def __init__(self):

        self.heading_detector = HeadingDetector()

    ####################################################################
    # PUBLIC
    ####################################################################

    def chunk_document(
        self,
        document: ParsedDocument
    ) -> List[DocumentChunk]:

        paragraphs = self.build_paragraphs(document)

        chunks = []

        for paragraph in paragraphs:

            chunks.extend(

                self.chunk_paragraph(

                    paragraph,

                    document.filename

                )

            )

        # Merge after all chunks are created
        chunks = self.merge_small_chunks(chunks)

        # Remove duplicates
        chunks = self.remove_duplicate_chunks(chunks)

        return chunks

    ####################################################################
    # PARAGRAPH BUILDER
    ####################################################################

    def build_paragraphs(
        self,
        document: ParsedDocument
    ) -> List[Paragraph]:

        paragraphs = []

        current_heading = "General"

        current_path = []

        buffer = []

        current_page = 1

        for page in document.pages:

            current_page = page.page_number

            for line in page.lines:

                text = self.clean(line.text)

                if not text:

                    continue

                #
                # Heading
                #

                if self.heading_detector.is_heading(line):

                    if buffer:

                        paragraphs.append(

                            Paragraph(

                                heading=current_heading,

                                page=current_page,

                                lines=buffer.copy(),

                                section_path=current_path.copy()

                            )

                        )

                        buffer.clear()

                    current_heading = text

                    current_path = self.update_section_path(

                        current_path,

                        current_heading

                    )

                    continue

                #
                # Blank line
                #

                if len(text) == 0:

                    if buffer:

                        paragraphs.append(

                            Paragraph(

                                heading=current_heading,

                                page=current_page,

                                lines=buffer.copy(),

                                section_path=current_path.copy()

                            )

                        )

                        buffer.clear()

                    continue

                buffer.append(text)

        if buffer:

            paragraphs.append(

                Paragraph(

                    heading=current_heading,

                    page=current_page,

                    lines=buffer,

                    section_path=current_path

                )

            )

        return paragraphs

    ####################################################################
    # SECTION PATH
    ####################################################################

    def update_section_path(

        self,

        current_path,

        heading

    ):

        """
        Simple hierarchy.

        Will be improved later.
        """

        if len(current_path) == 0:

            return [heading]

        numbered = re.match(

            r"^\d+(\.\d+)*",

            heading

        )

        if numbered:

            path = current_path.copy()

            path.append(heading)

            return path

        return [heading]

    ####################################################################
    # HELPERS
    ####################################################################

    @staticmethod
    def clean(text):

        text = text.replace("\t", " ")

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text.strip()

    ####################################################################
    # TABLE DETECTOR
    ####################################################################

    def looks_like_table(
        self,
        line: str,
    ):

        if "|" in line:
            return True

        if "\t" in line:
            return True

        if re.search(r"\s{3,}", line):
            return True

        if re.search(
            r"\b(HGB|WBC|RBC|BUN|Na|K|Cl|CO2)\b",
            line,
            re.IGNORECASE
        ):
            return True

        return False

    ####################################################################
    # SENTENCE SPLITTER
    ####################################################################

    def split_sentences(

        self,

        text

    ):

        """
        Conservative sentence splitting.
        """

        sentences = re.split(

            r'(?<=[.!?])\s+',

            text

        )

        return [

            s.strip()

            for s in sentences

            if s.strip()

        ]
    ####################################################################
    # PARAGRAPH CHUNKING
    ####################################################################

    def chunk_paragraph(
        self,
        paragraph: Paragraph,
        filename: str,
    ) -> List[DocumentChunk]:
        """
        Split a paragraph into token-aware chunks.
        """

        full_text = "\n".join(paragraph.lines).strip()

        if not full_text:
            return []

        #
        # Table paragraph
        #

        if any(self.looks_like_table(line) for line in paragraph.lines):

            return [
                self.build_chunk(
                    text=full_text,
                    paragraph=paragraph,
                    filename=filename,
                    chunk_type="table",
                )
            ]

        #
        # Split into sentences
        #

        sentences = self.split_sentences(full_text)

        if not sentences:
            return []

        chunks = []

        current_sentences = []

        current_tokens = 0

        for sentence in sentences:

            token_count = count_tokens(sentence)

            #
            # Single sentence larger than max
            #

            if token_count >= self.MAX_TOKENS:

                if current_sentences:

                    chunks.append(

                        self.build_chunk(

                            text=" ".join(current_sentences),

                            paragraph=paragraph,

                            filename=filename,

                            chunk_type="text",

                        )

                    )

                    current_sentences = []

                    current_tokens = 0

                chunks.extend(

                    self.chunk_large_sentence(

                        sentence,

                        paragraph,

                        filename

                    )

                )

                continue

            #
            # Window full
            #

            if current_tokens + token_count > self.MAX_TOKENS:

                chunks.append(

                    self.build_chunk(

                        text=" ".join(current_sentences),

                        paragraph=paragraph,

                        filename=filename,

                        chunk_type="text",

                    )

                )

                current_sentences = self.apply_overlap(
                    current_sentences
                )

                current_tokens = count_tokens(
                    " ".join(current_sentences)
                )

            current_sentences.append(sentence)

            current_tokens += token_count

        if current_sentences:

            chunks.append(

                self.build_chunk(

                    text=" ".join(current_sentences),

                    paragraph=paragraph,

                    filename=filename,

                    chunk_type="text",

                )

            )

        return chunks

    ####################################################################
    # LARGE SENTENCE
    ####################################################################

    def chunk_large_sentence(
        self,
        sentence: str,
        paragraph: Paragraph,
        filename: str,
    ) -> List[DocumentChunk]:

        words = sentence.split()

        chunks = []

        current = []

        tokens = 0

        for word in words:

            word_tokens = count_tokens(word)

            if tokens + word_tokens > self.MAX_TOKENS:

                chunks.append(

                    self.build_chunk(

                        text=" ".join(current),

                        paragraph=paragraph,

                        filename=filename,

                        chunk_type="text",

                    )

                )

                current = current[-25:]

                tokens = count_tokens(
                    " ".join(current)
                )

            current.append(word)

            tokens += word_tokens

        if current:

            chunks.append(

                self.build_chunk(

                    text=" ".join(current),

                    paragraph=paragraph,

                    filename=filename,

                    chunk_type="text",

                )

            )

        return chunks
    
    ####################################################################
    # OVERLAP
    ####################################################################

    def apply_overlap(
        self,
        sentences: List[str],
    ) -> List[str]:

        if not sentences:
            return []

        overlap = []

        tokens = 0

        for sentence in reversed(sentences):

            sentence_tokens = count_tokens(sentence)

            if tokens + sentence_tokens > self.TOKEN_OVERLAP:
                break

            overlap.insert(0, sentence)

            tokens += sentence_tokens

        return overlap
    
    ####################################################################
    # BUILD CHUNK
    ####################################################################

    def build_chunk(
        self,
        text: str,
        paragraph: Paragraph,
        filename: str,
        chunk_type: str,
    ) -> DocumentChunk:

        chunk_id = self.generate_chunk_id(
            filename,
            paragraph.page,
            paragraph.heading,
            text,
        )

        diagnosis = self.detect_diagnosis_tag(text)

        medications = self.detect_medications(text)

        labs = self.detect_lab_values(text)

        metadata = {

            "source_file": filename,

            "page_start": paragraph.page,

            "page_end": paragraph.page,

            "heading": paragraph.heading,

            "section_path": paragraph.section_path,

            "priority": self.section_priority(
                paragraph.heading
            ),

            "clinical_score": self.calculate_clinical_score(
                text,
                paragraph.heading
            ),

            "chunk_type": chunk_type,

            "diagnosis_tag": diagnosis,

            "medications": medications,

            "lab_values": labs,

            "token_count": count_tokens(text),

            "word_count": len(text.split()),

        }

        return DocumentChunk(

            id=chunk_id,

            text=text,

            page_start=paragraph.page,

            page_end=paragraph.page,

            source_file=filename,

            section_heading=paragraph.heading,

            section_path=paragraph.section_path,

            document_category=self.DEFAULT_CATEGORY,

            chunk_type=chunk_type,

            token_count=count_tokens(text),

            metadata=metadata,

        )
    ####################################################################
    # CHUNK ID
    ####################################################################

    @staticmethod
    def generate_chunk_id(
        filename,
        page,
        heading,
        text,
    ):

        key = f"{filename}|{page}|{heading}|{text}"

        return hashlib.sha256(
            key.encode("utf-8")
        ).hexdigest()

    ####################################################################
    # SECTION PRIORITY
    ####################################################################

    def section_priority(self, heading: str) -> int:
        """
        Assign retrieval priority to common clinical sections.
        Higher values indicate more clinically important content.
        """

        if not heading:
            return 1

        heading = heading.lower()

        priorities = {

            "assessment": 10,

            "impression": 10,

            "diagnosis": 10,

            "principal diagnosis": 10,

            "final diagnosis": 10,

            "plan": 9,

            "hospital course": 9,

            "history of present illness": 9,

            "history": 8,

            "physical examination": 8,

            "exam": 8,

            "laboratory": 8,

            "labs": 8,

            "radiology": 8,

            "imaging": 8,

            "medications": 7,

            "medication": 7,

            "allergies": 7,

            "vitals": 7,

            "consultation": 6,

            "discharge": 6

        }

        for key, value in priorities.items():

            if key in heading:
                return value

        return 5
    ####################################################################
    # DIAGNOSIS TAG
    ####################################################################

    def detect_diagnosis_tag(
        self,
        text: str,
    ):

        text = text.lower()

        # IMPORTANT: Keywords are checked in order from top to bottom.
        # Place LONGEST, MOST SPECIFIC phrases first to avoid false positives.
        # Avoid generic symptoms (e.g., "chest pain", "acute") that appear across many diagnoses.
        diagnosis_map = {

            # === Specific multi-word phrases first (highest priority) ===

            # Community-Acquired Pneumonia (specific)
            "community-acquired pneumonia": "PNEUMONIA",
            "community acquired pneumonia": "PNEUMONIA",

            # COPD Exacerbation (specific)
            "acute exacerbation of copd": "COPD",
            "copd exacerbation": "COPD",
            "aecopd": "COPD",
            "acute exacerbation copd": "COPD",

            # CHF specific phrases
            "congestive heart failure": "CHF",
            "acute decompensated heart failure": "CHF",
            "systolic heart failure": "CHF",
            "diastolic heart failure": "CHF",
            "left ventricular failure": "CHF",
            "right ventricular failure": "CHF",
            "biventricular failure": "CHF",
            "reduced ejection fraction": "CHF",
            "preserved ejection fraction": "CHF",
            "acute heart failure": "CHF",
            "chronic heart failure": "CHF",
            "decompensated heart": "CHF",

            # Stroke specific phrases
            "ischemic stroke": "STROKE",
            "transient ischemic attack": "STROKE",
            "cerebrovascular accident": "STROKE",
            "cerebral infarction": "STROKE",
            "brain infarction": "STROKE",
            "cerebral ischemia": "STROKE",
            "embolic stroke": "STROKE",
            "thrombotic stroke": "STROKE",

            # NSTEMI specific phrases
            "non-st elevation myocardial infarction": "NSTEMI",
            "non st elevation": "NSTEMI",
            "acute coronary syndrome": "NSTEMI",
            "myocardial infarction": "NSTEMI",
            "unstable angina": "NSTEMI",
            "troponin elevation": "NSTEMI",
            "elevated troponin": "NSTEMI",

            # Pulmonary Embolism specific phrases
            "pulmonary embolism": "PE",
            "pulmonary embolus": "PE",
            "deep vein thrombosis": "PE",
            "venous thromboembolism": "PE",
            "pulmonary thromboembolism": "PE",

            # Sepsis specific phrases
            "septic shock": "SEPSIS",
            "severe sepsis": "SEPSIS",
            "systemic inflammatory response": "SEPSIS",
            "systemic infection": "SEPSIS",

            # COVID specific phrases
            "covid-19": "COVID",
            "covid 19": "COVID",
            "sars-cov-2": "COVID",
            "novel coronavirus": "COVID",

            # COPD specific phrases
            "chronic obstructive pulmonary disease": "COPD",
            "chronic obstructive pulmonary": "COPD",
            "chronic obstructive": "COPD",
            "chronic bronchitis": "COPD",
            "obstructive lung disease": "COPD",
            "obstructive airway": "COPD",
            "chronic airway obstruction": "COPD",
            "hypercapnic respiratory": "COPD",

            # === Shorter / more generic terms (lower priority) ===

            "heart failure": "CHF",
            "cardiac failure": "CHF",
            "cardiomyopathy": "CHF",
            "adhf": "CHF",
            "hfref": "CHF",
            "hfpef": "CHF",
            "chf": "CHF",

            "pneumonia": "PNEUMONIA",
            "lower respiratory infection": "PNEUMONIA",
            "lung infection": "PNEUMONIA",
            "bacterial pneumonia": "PNEUMONIA",
            "viral pneumonia": "PNEUMONIA",
            "aspiration pneumonia": "PNEUMONIA",
            "lobar pneumonia": "PNEUMONIA",
            "pneumonitis": "PNEUMONIA",

            "sepsis": "SEPSIS",
            "septicemia": "SEPSIS",
            "bacteremia": "SEPSIS",
            "septic": "SEPSIS",

            "copd": "COPD",
            "emphysema": "COPD",

            "nstemi": "NSTEMI",
            "acute coronary": "NSTEMI",
            "heart attack": "NSTEMI",
            "ischemic heart": "NSTEMI",
            "acute mi": "NSTEMI",
            "angina": "NSTEMI",
            "acs": "NSTEMI",
            "ami": "NSTEMI",
            "ua": "NSTEMI",

            "stroke": "STROKE",
            "cerebrovascular": "STROKE",
            "brain attack": "STROKE",
            "cva": "STROKE",
            "tia": "STROKE",

            "covid": "COVID",
            "covid19": "COVID",
            "coronavirus": "COVID",
            "2019-ncov": "COVID",

            "dvt": "PE",
            "vte": "PE",
            "blood clot": "PE",
            "thromboembolism": "PE",

            # === Non-workbook diagnoses (generic fallback) ===
            "diabetes": "DIABETES",
            "diabetic": "DIABETES",
            "hyperglycemia": "DIABETES",
            "hypertension": "HTN",
            "high blood pressure": "HTN",
            "htn": "HTN",
            "acute kidney injury": "AKI",
            "kidney injury": "AKI",
            "renal failure": "AKI",
            "acute renal": "AKI",
            "aki": "AKI",

        }

        for keyword, tag in diagnosis_map.items():

            if keyword in text:

                return tag

        return None

    ####################################################################
    # MEDICATION DETECTION
    ####################################################################

    def detect_medications(
        self,
        text: str,
    ):

        meds = []

        medication_keywords = [

            "aspirin",

            "metformin",

            "lasix",

            "furosemide",

            "lisinopril",

            "insulin",

            "atorvastatin",

            "heparin",

            "warfarin",

            "eliquis",

            "jardiance",

            "amlodipine"

        ]

        lower = text.lower()

        for med in medication_keywords:

            if med in lower:

                meds.append(med)

        return meds

    ####################################################################
    # LAB DETECTION
    ####################################################################

    def detect_lab_values(
        self,
        text: str,
    ) -> list[str]:
        # Non-capturing groups (?:...) ensure re.findall returns the full
        # match string instead of just the captured sub-group.
        patterns = [
            r"hgb[: ]+\d+(?:\.\d+)?",
            r"wbc[: ]+\d+(?:\.\d+)?",
            r"platelets?[: ]+\d+",
            r"creatinine[: ]+\d+(?:\.\d+)?",
            r"bun[: ]+\d+",
            r"sodium[: ]+\d+",
            r"potassium[: ]+\d+(?:\.\d+)?",
            r"glucose[: ]+\d+",
        ]

        found: list[str] = []
        lower = text.lower()

        for pattern in patterns:
            matches = re.findall(pattern, lower)
            found.extend(matches)

        return found

    ####################################################################
    # MERGE SMALL CHUNKS
    ####################################################################

    def merge_small_chunks(
        self,
        chunks: List[DocumentChunk]
    ) -> List[DocumentChunk]:

        if not chunks:
            return []

        merged = []
        current = chunks[0]

        for next_chunk in chunks[1:]:

            if (
                current.token_count < self.MIN_TOKENS
                and current.section_heading == next_chunk.section_heading
            ):

                combined_text = current.text + "\n" + next_chunk.text

                current = self.build_chunk(
                    text=combined_text,
                    paragraph=Paragraph(
                        heading=current.section_heading,
                        page=current.page_start,
                        lines=combined_text.splitlines(),
                        section_path=current.section_path,
                    ),
                    filename=current.source_file,
                    chunk_type=current.chunk_type,
                )

            else:
                merged.append(current)
                current = next_chunk

        merged.append(current)

        return merged
    ####################################################################
    # REMOVE DUPLICATES
    ####################################################################

    def remove_duplicate_chunks(
        self,
        chunks: List[DocumentChunk]
    ) -> List[DocumentChunk]:

        seen = set()
        unique = []

        for chunk in chunks:

            if chunk.id in seen:
                continue

            seen.add(chunk.id)
            unique.append(chunk)

        return unique
    
    ####################################################################
    # CLINICAL SCORE
    ####################################################################

    def calculate_clinical_score(
        self,
        text: str,
        heading: str,
    ) -> int:

        score = 0

        score += self.section_priority(heading)

        keywords = [

            "diagnosis",
            "assessment",
            "plan",
            "acute",
            "chronic",
            "hospital",
            "discharge",
            "medication",
            "laboratory",
            "impression",

        ]

        lower = text.lower()

        for keyword in keywords:

            if keyword in lower:
                score += 1

        return score