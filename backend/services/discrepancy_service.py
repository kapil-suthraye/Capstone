from backend.models.review_response import ReviewResponse


class DiscrepancyService:

    def get_missing_documents(
        self,
        review: ReviewResponse
    ):

        return review.missing_documentation