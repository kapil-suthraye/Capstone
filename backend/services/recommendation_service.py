from backend.models.review_response import ReviewResponse


class RecommendationService:

    def get_recommendation(
        self,
        review: ReviewResponse
    ):

        return {

            "recommendation": review.recommendation,

            "confidence": review.confidence

        }