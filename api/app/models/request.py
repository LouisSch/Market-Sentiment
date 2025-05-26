from pydantic import BaseModel, Field

class AnalyzeRequest(BaseModel):
    ticker: str = Field(
        ...,
        description="Stock ticker (e.g. AAPL, TSLA, ...)",
        min_length=1,
        max_length=10,
        pattern="^[A-Z0-9]+$"
    )