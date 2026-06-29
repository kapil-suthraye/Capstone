import json
from pathlib import Path


class KnowledgeRegistry:

    def __init__(self):

        registry_file = (
            Path(__file__).parent /
            "knowledge_registry.json"
        )

        with open(
            registry_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.registry = json.load(file)

    def get_sheet(self, diagnosis: str):

        diagnosis = diagnosis.lower()

        for disease, info in self.registry.items():

            aliases = [

                disease.lower()

            ] + [

                alias.lower()

                for alias in info["aliases"]

            ]

            if diagnosis in aliases:

                return info["sheet"]

        return None