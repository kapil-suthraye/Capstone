import requests
from config import BACKEND_URL

TIMEOUT = 300


def _request(method, endpoint, payload=None):
    """
    Centralized HTTP helper.

    Every UI page should use this helper instead of calling
    requests directly.
    """

    url = f"{BACKEND_URL}{endpoint}"

    try:

        if method == "GET":

            response = requests.get(
                url,
                timeout=TIMEOUT
            )

        elif method == "POST":

            response = requests.post(
                url,
                json=payload,
                timeout=TIMEOUT
            )

        else:

            raise ValueError(f"Unsupported HTTP method: {method}")

        response.raise_for_status()

        return response.json()

    except requests.exceptions.ConnectionError:

        raise Exception(
            "Unable to connect to Medical AI Reviewer Backend."
        )

    except requests.exceptions.Timeout:

        raise Exception(
            "Backend request timed out."
        )

    except requests.exceptions.HTTPError as ex:

        raise Exception(
            f"Backend Error : {ex.response.text}"
        )


def review_claim(payload):

    return _request(

        "POST",

        "/review",

        payload

    )


def health():

    return _request(

        "GET",

        "/health"

    )