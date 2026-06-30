import requests

from config import BACKEND_URL

TIMEOUT = 300


def review_claim(payload):

    url = f"{BACKEND_URL}/review"

    response = requests.post(
        url,
        json=payload,
        timeout=TIMEOUT
    )

    response.raise_for_status()

    return response.json()


def health():

    url = f"{BACKEND_URL}/health"

    response = requests.get(url)

    return response.json()