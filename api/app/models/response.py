from pydantic import BaseModel, Field

class SentimentResponse(BaseModel):
    name: str = Field(..., description="Company name (e.g. Apple Inc.)")
    exchange: str = Field(..., description="Market exchange (e.g. NASDAQ)")
    price_change: str = Field(..., description="Recent price change (e.g. +2.13%)")
    sentiment: str = Field(..., description="Most confident predicted sentiment label")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence of the prediction")
    polarization: str = Field(..., description="Text summary of sentiment distribution")
    articles_analyzed: int = Field(..., ge=0, description="Number of articles processed")
    avg_scores: dict[str, float] = Field(..., description="Average sentiment confidence scores")
    distribution: dict[str, int] = Field(..., description="Sentiment counts per class")
    most_positive: str
    most_negative: str
    most_positive_score: float
    most_negative_score: float
    most_positive_source: str
    most_negative_source: str
    most_positive_time: str
    most_negative_time: str


    class Config:
        json_schema_extra = {
            "example": {
                "name": "ABC",
                "exchange": "NASDAQ",
                "price_change": "+2.13%",
                "sentiment": "positive",
                "confidence": 0.89,
                "polarization": "Consensus: Strongly positive",
                "articles_analyzed": 6,
                "avg_scores": {
                    "positive": 0.72,
                    "neutral": 0.24,
                    "negative": 0.04
                },
                "distribution": {
                    "positive": 4,
                    "neutral": 1,
                    "negative": 1
                },
                "most_positive": "ABC stock jumps after record deliveries.",
                "most_negative": "ABC faces pressure on profit margins.",
                "most_positive_score": 0.802,
                "most_negative_score": 0.431,
                "most_positive_source": "XYZ",
                "most_negative_source": "XYZ",
                "most_positive_time": "2025-01-01 12:05:50 CEST",
                "most_negative_time": "2025-01-01 12:05:50 CEST",
            }
        }