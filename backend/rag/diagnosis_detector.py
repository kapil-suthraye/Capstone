import re


class DiagnosisDetector:

    """
    Extract primary diagnosis from
    retrieved medical evidence.
    """

    KEYWORDS = {

        "COVID-19": [

            "covid",

            "coronavirus"

        ],

        "Sepsis": [

            "sepsis",

            "septic shock"

        ],

        "CAP": [

            "pneumonia",

            "community acquired"

        ],

        "CHF": [

            "heart failure",

            "congestive heart failure",

            "adhf"

        ],

        "NSTEMI": [

            "nstemi",

            "acute coronary"

        ],

        "AECOPD": [

            "copd",

            "aecopd"

        ],

        "Pulmonary Embolism": [

            "pulmonary embolism",

            "pe"

        ],

        "Ischemic Stroke": [

            "stroke",

            "cva"

        ]

    }

    def detect(

        self,

        documents

    ):

        combined = ""

        for doc in documents:

            combined += doc.page_content.lower()

        for diagnosis, words in self.KEYWORDS.items():

            for word in words:

                if re.search(

                    word,

                    combined

                ):

                    return diagnosis

        return "General Medical Review"