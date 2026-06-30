from backend.models.review_response import ReviewResponse


class SummaryService:
    """
    Returns the clinical summary from the AI review.
    """

    def get_summary(
        self,
        review: ReviewResponse
    ) -> str:

        return review.summary