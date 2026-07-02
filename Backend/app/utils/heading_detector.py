import re

from Backend.app.models.parsed_line import ParsedLine


class HeadingDetector:

    @staticmethod
    def score(line: ParsedLine) -> int:

        score = 0

        text = line.text.strip()

        if not text:
            return 0

        if line.font_size >= 16:
            score += 3

        elif line.font_size >= 14:
            score += 2

        if line.is_bold:
            score += 2

        if text.isupper():
            score += 2

        if text.endswith(":"):
            score += 1

        if re.match(r"^\d+(\.\d+)*", text):
            score += 2

        if len(text.split()) <= 8:
            score += 1

        return score

    @staticmethod
    def is_heading(line: ParsedLine) -> bool:

        return HeadingDetector.score(line) >= 4