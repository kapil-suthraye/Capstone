from backend.models.review_response import ReviewResponse


class EvidenceService:
    """
    Returns supporting evidence.
    """

    def get_evidence(
        self,
        review: ReviewResponse
    ):

        return review.evidence