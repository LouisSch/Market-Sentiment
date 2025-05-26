from dash import Dash, Output, Input, State, html
from dash.exceptions import PreventUpdate

from logic import fetch_sentiment_data, build_sentiment_figure

def register_callbacks(app: Dash):
    @app.callback(
        [
            Output("stockSymbol", "children"),
            Output("companyName", "children"),
            Output("marketName", "children"),
            Output("marketChange", "children"),

            Output("confidenceBadge", "children"),
            Output("confidenceBadge", "className"),
            Output("confidenceBar", "className"),
            Output("confidenceBar", "style"),
            Output("confidenceText", "children"),

            Output("distributionBadge", "children"),
            Output("distributionBadge", "className"),
            Output("distPositive", "children"),
            Output("distNeutral", "children"),
            Output("distNegative", "children"),

            Output("sentiment-distribution", "figure"),

            Output("posScore", "children"),
            Output("mostPositive", "children"),
            Output("posSource", "children"),

            Output("negScore", "children"),
            Output("mostNegative", "children"),
            Output("negSource", "children"),

            Output("lastUpdated", "children"),
            Output("dashboard-container", "style"),
            Output("error-banner", "className")
        ],
        Input("analyze-button", "n_clicks"),
        State("ticker-name", "value")
    )
    def analyze(n_clicks, ticker):
        if not n_clicks or not ticker:
            raise PreventUpdate()

        data = fetch_sentiment_data(ticker)

        if not data:
            return (
                "", "", "", "",              
                "", "", "", {}, "",
                "", "", "", "", "",
                {},                                
                "", "", "",
                "", "", "",
                "",       
                { "display": "none" },
                "block bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4"
            )

        figure = build_sentiment_figure(ticker, data)

        # Stock header
        symbol = ticker.upper()
        name = data.get("company", "")
        market = data.get("exchange", "")
        change = data.get("price_change", "")

        # Confidence badge
        conf_label = data["sentiment"].capitalize()
        conf_val = int(data["confidence"] * 100)
        badge_cls = f"px-6 py-3 rounded-full text-lg font-bold mb-3 border-2 sentiment-{data['sentiment']}"
        badge_icon = {
            "Positive": html.I(className="fas fa-smile-beam mr-2"),
            "Negative": html.I(className="fas fa-frown mr-2"),
        }.get(conf_label, html.I(className="fas fa-meh mr-2"))
        bar_cls = f"h-2.5 rounded-full bg-{ 'green' if data['sentiment']=='positive' else 'red' if data['sentiment']=='negative' else 'gray' }-500"
        bar_style = {"width": f"{conf_val}%"}

        # Distribution badge
        dist_label = data["polarization"]
        dist_cls = f"px-6 py-3 rounded-full text-lg font-bold mb-4 border-2 sentiment-{dist_label.split()[-1].lower()}"
        dist_children = [
            html.I(className="fas fa-balance-scale mr-2") if "balanced" in dist_label.lower() else
            html.I(className="fas fa-thumbs-up mr-2")   if "positive" in dist_label.lower() else
            html.I(className="fas fa-thumbs-down mr-2") if "negative" in dist_label.lower() else
            html.I(className="fas fa-equals mr-2"),
            dist_label
        ]

        # News
        pos_text = data["most_positive"]
        pos_src = f"{data['most_positive_source']} – {data['most_positive_time']}"
        neg_text = data["most_negative"]
        neg_src = f"{data['most_negative_source']} – {data['most_negative_time']}"

        from datetime import datetime
        updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return (
            symbol, name, market, change,
            [badge_icon, conf_label], badge_cls, bar_cls, bar_style, f"{conf_val}% confidence",
            dist_children, dist_cls,
            f"{data['distribution']['positive']/data['articles_analyzed']:.0%}", f"{data['distribution']['neutral']/data['articles_analyzed']:.0%}", f"{data['distribution']['negative']/data['articles_analyzed']:.0%}",
            figure,
            f"Conf: {data['most_positive_score']:.0%}", pos_text, pos_src,
            f"Conf: {data['most_negative_score']:.0%}", neg_text, neg_src,
            updated,
            { "display": "block" },
            "hidden block bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4"
        )