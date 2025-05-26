import requests

from dash import html
from style import color_map, get_badge_color

def fetch_sentiment_data(ticker: str):
    try:
        response = requests.post("http://api:5002/analyze", json={
                    "ticker": ticker
                })
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Dashboard exception for {ticker}: {e}")
        return None

def build_sentiment_figure(ticker: str, json_data):
    dist = json_data['distribution']

    return {
        "data": [{
            "type": "pie",
            "labels": list(dist.keys()),
            "values": list(dist.values()),
            "marker": {"colors": ["#dc3545", "#ffc107", "#28a745"]}
        }],
        "layout": {
            "title": {
                "text": f"Sentiment breakdown for {ticker.upper()}",
                "x": 0.5,
                "xanchor": "center",
                "font": { "size": 18 }
            },
            "margin": { "l": 20, "r": 20, "t": 40, "b": 20 }
        }
    }