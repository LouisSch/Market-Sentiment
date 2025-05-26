import os
import finnhub
import httpx
import re
import pytz

from datetime import datetime, timedelta
from fuzzywuzzy import fuzz

FINNHUB_KEY = os.getenv("FINNHUB_API_KEY", "")
client = finnhub.Client(api_key=FINNHUB_KEY)

async def fetch_news(symbol: str, from_date: str, to_date: str):
    url = "https://finnhub.io/api/v1/company-news"
    parameters = {
        "symbol": symbol,
        "from": from_date,
        "to": to_date,
        "token": FINNHUB_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=parameters)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[news] - API error for {symbol}: {e}")
            return None
        except Exception as e:
            print(f"[news] - Unexpected error for {symbol}: {e}")
            return None

async def fetch_profile(symbol: str):
    url = "https://finnhub.io/api/v1/stock/profile2"
    parameters = {
        "symbol": symbol,
        "token": FINNHUB_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=parameters)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"[news] - API error for {symbol}: {e}")
            return None
        except Exception as e:
            print(f"[news] - Unexpected error for {symbol}: {e}")
            return None

def fuzzy_match(text: str, keywords: list[str], threshold: int = 70) -> bool:
    text = re.sub(r"[^\w\s]", " ", text.lower())
    
    for kw in keywords:
        if fuzz.partial_ratio(kw.lower(), text) >= threshold:
            return True
        
    return False

async def get_articles_from_ticker(symbol: str):
    symbol = symbol.upper()
    today = datetime.today()
    from_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    to_date = today.strftime("%Y-%m-%d")
    tz = pytz.timezone("Europe/Paris")

    raw = await fetch_news(symbol, from_date, to_date)
    profile = await fetch_profile(symbol)

    if raw is None or profile is None:
        return None, None

    if not raw or "name" not in profile or not profile.get("name"):
        return None, None

    kw = [profile.get("ticker", ""), profile.get("name", "")]

    cleaned = []
    for item in raw:
        headline = item.get("headline")
        summary = item.get("summary")
        source = item.get("source", "")
        time = datetime.fromtimestamp(item.get("datetime", ""), tz).strftime("%Y-%m-%d %H:%M %Z")

        if not headline or len(headline) < 15:
            continue

        if fuzzy_match(headline, kw) or fuzzy_match(summary, kw):
            cleaned.append((f"News about {symbol}: {headline}. {summary}. How might investors react?", source, time)) if summary else cleaned.append((f"News about {symbol}: {headline}. How might investors react?", source, time))
    
    company_data = {
        "name": profile.get("name", ""),
        "exchange": profile.get("exchange", ""),
        "price_change": ""
    }

    return cleaned, company_data