from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.request import AnalyzeRequest
from models.response import SentimentResponse

from core.sentiment import RobertaSentiment
from core.news import get_articles_from_ticker

from middleware.rate_limit import RateLimiterMiddleware

app = FastAPI(title="News Sentiment API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app.add_middleware(RateLimiterMiddleware)

predictor = RobertaSentiment()

def get_polarization_label(distribution: dict[str, int]) -> str:
    total = sum(distribution.values())
    if total == 0:
        return "No sentiment detected."
    
    ratios = {k: v / total for k, v in distribution.items()}
    major = max(ratios, key=ratios.get)
    share = ratios[major]

    if share > 0.5:
        return f"Consensus: Strongly {major.capitalize()}"
    elif share > 0.45:
        return f"Market: {major.capitalize()}"
    else:
        return "Sentiment distribution: Balanced"

@app.post(
        "/analyze",
        tags=["SentimentAnalysis"],
        response_model=SentimentResponse,
        summary="Analyze news sentiment for a given stock ticker.",
        description="Fetches recent news from Finnhub and applie a transformer model to predict market sentiment on a givent stock symbol."
    )
async def analyze_sentiment(request: AnalyzeRequest):
    articles, company_data = await get_articles_from_ticker(request.ticker)

    if not articles:
        raise HTTPException(status_code=404, detail=f"No news found for symbol {request.ticker}.")

    result = predictor.predict(request.ticker, articles)
    result['polarization'] = get_polarization_label(result['distribution'])

    for k, v in company_data.items():
        result[k] = v

    return result