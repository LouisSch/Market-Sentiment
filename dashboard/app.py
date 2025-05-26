from dash import Dash

from callbacks import register_callbacks
from layout import layout

external_css = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
]

external_scripts = [
    "https://cdn.tailwindcss.com",
    "https://cdn.jsdelivr.net/npm/chart.js"
]

# external_css = ["https://fonts.googleapis.com/css2?family=Roboto&display=swap"]

app = Dash(__name__,
           title="Market Sentiment Analysis",
           external_stylesheets=external_css,
           external_scripts=external_scripts,
           suppress_callback_exceptions=True
        )

app.index_string = """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"/>
        </head>
        <body class="bg-gray-50">
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""
app.layout = layout
register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)