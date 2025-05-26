from dash import html, dcc

layout = html.Div(
    className="container mx-auto px-4 py-8",
    children=[
        # Error Banner
        html.Div(
            id="error-banner",
            className="hidden bg-yellow-100 border-1-4 border-yellow-500 text-yellow-700 p-4 mb-4",
            role="alert",
            children=[
                html.P("News temporarily unavailable. Please try again later.")
            ]
        ),

        # Header
        html.Div(
            className="flex items-center justify-between mb-8",
            children=[
                html.Div(
                    className="flex items-center space-x-4",
                    children=[
                        html.Div(
                            className="bg-blue-100 p-4 rounded-full",
                            children=html.I(className="fas fa-chart-line text-blue-600 text-2xl")
                        ),
                        html.Div([
                            html.H1("Stock Sentiment Analysis", className="text-3xl font-bold text-gray-800"),
                            html.P("Real-time market sentiment dashboard", className="text-gray-600")
                        ])
                    ]
                ),
                html.Div(
                    className="flex items-center bg-white rounded-lg shadow px-4 py-2 transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                    children=[
                        html.I(className="fas fa-search text-gray-400 mr-2"),
                        dcc.Input(
                            id="ticker-name",
                            type="text",
                            placeholder="Search stock symbol...",
                            className="outline-none"
                        ),
                        html.Button(
                            "Search",
                            id="analyze-button",
                            className="ml-2 bg-blue-600 text-white px-3 py-1 rounded-md hover:bg-blue-700 transition"
                        )
                    ]
                )
            ]
        ),
        dcc.Loading(
            id="loading",
            type="circle",
            color="#007BFF",
            children=[
                html.Div(
                    id="dashboard-container",
                    style={"display": "none"},
                    children=[
                        # Current Stock Info
                        html.Div(
                            className="bg-white rounded-xl shadow-md p-6 mb-8 transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                            children=html.Div(
                                className="flex items-center justify-between",
                                children=[
                                    html.Div(
                                        className="flex items-center space-x-4",
                                        children=[
                                            html.Div(
                                                className="bg-blue-600 text-white p-3 rounded-lg",
                                                children=html.Span(id="stockSymbol", className="text-xl font-bold")
                                            ),
                                            html.Div([
                                                html.H2(id="companyName", className="text-2xl font-bold text-gray-800"),
                                                html.Div(className="flex items-center space-x-2 text-gray-600", children=[
                                                    html.Span(id="marketName"),
                                                    html.Span(id="marketChange", className="text-green-600 font-medium"),
                                                    html.Span("Today", className="text-gray-400")
                                                ])
                                            ])
                                        ]
                                    ),
                                    html.Div(
                                        className="flex space-x-2",
                                        children=[
                                            html.Button(
                                                [html.I(className="fas fa-chart-bar mr-2"), "Charts"],
                                                className="px-4 py-2 bg-gray-100 rounded-lg hover:bg-gray-200 transition"
                                            ),
                                            html.Button(
                                                [html.I(className="fas fa-sync-alt mr-2"), "Refresh"],
                                                id="refresh-btn",
                                                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
                                            )
                                        ]
                                    )
                                ]
                            )
                        ),

                        # Dashboard Grid
                        html.Div(
                            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8",
                            children=[

                                # Sentiment Distribution
                                html.Div(
                                    className="highlight-card bg-white rounded-xl shadow-md p-6 transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                                    children=[
                                        html.Div(
                                            className="flex items-center justify-between mb-4",
                                            children=[
                                                html.H3("Sentiment Distribution", className="text-lg font-semibold text-gray-700"),
                                                html.I(className="fas fa-project-diagram text-purple-500")
                                            ]
                                        ),
                                        html.Div(id="distributionBadge", className="px-6 py-3 rounded-full text-lg font-bold mb-4 sentiment-balanced border-2 text-center"),
                                        html.Div(
                                            className="grid grid-cols-3 gap-2 text-center",
                                            children=[
                                                html.Div(className="p-2 rounded-lg sentiment-positive", children=[
                                                    html.P("Positive", className="font-semibold text-green-600"),
                                                    html.P(id="distPositive", className="text-xl font-bold")
                                                ]),
                                                html.Div(className="p-2 rounded-lg sentiment-neutral", children=[
                                                    html.P("Neutral", className="font-semibold text-gray-600"),
                                                    html.P(id="distNeutral", className="text-xl font-bold")
                                                ]),
                                                html.Div(className="p-2 rounded-lg sentiment-negative", children=[
                                                    html.P("Negative", className="font-semibold text-red-600"),
                                                    html.P(id="distNegative", className="text-xl font-bold")
                                                ])
                                            ]
                                        )
                                    ]
                                ),

                                # Most Confident Prediction
                                html.Div(
                                    className="highlight-card bg-white rounded-xl shadow-md p-6 transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                                    children=[
                                        html.Div(
                                            className="flex items-center justify-between mb-4",
                                            children=[
                                                html.H3("Most Confident Prediction", className="text-lg font-semibold text-gray-700"),
                                                html.I(className="fas fa-bullseye text-blue-500")
                                            ]
                                        ),
                                        html.Div(
                                            className="flex flex-col items-center justify-center py-4",
                                            children=[
                                                html.Div(
                                                    id="confidenceBadge",
                                                    className="px-6 py-3 rounded-full text-lg font-bold mb-3 sentiment-positive border-2",
                                                    children=[]
                                                ),
                                                html.Div(
                                                    className="w-full bg-gray-200 rounded-full h-2.5",
                                                    children=html.Div(id="confidenceBar", className="h-2.5 rounded-full")
                                                ),
                                                html.P(id="confidenceText", className="text-gray-600 mt-2")
                                            ]
                                        )
                                    ]
                                ),

                                # Pie Chart
                                html.Div(
                                    className="highlight-card bg-white rounded-xl shadow-md p-6 transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                                    children=[
                                        html.Div(
                                            className="flex items-center justify-between mb-4",
                                            children=[
                                                html.H3("Sentiment Classification", className="text-lg font-semibold text-gray-700"),
                                                html.I(className="fas fa-chart-pie text-yellow-500")
                                            ]
                                        ),
                                        dcc.Graph(
                                            id="sentiment-distribution",
                                            config={"displayModeBar": False},
                                            style={"height": "250px"}
                                        )
                                    ]
                                ),

                            ]
                        ),

                        # News
                        html.Div(
                            className="grid grid-cols-1 lg:grid-cols-2 gap-6",
                            children=[

                                # Most Positive News
                                html.Div(
                                    className="highlight-card bg-white rounded-xl shadow-md overflow-hidden transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                                    children=[
                                        html.Div(className="bg-green-100 px-6 py-3 flex items-center", children=[
                                            html.I(className="fas fa-smile text-green-600 text-xl mr-3"),
                                            html.H3("Most Positive News", className="text-lg font-semibold text-green-800"),
                                            html.Span(id="posScore", className="ml-auto bg-green-600 text-white text-xs px-2 py-1 rounded-full")
                                        ]),
                                        html.Div(className="news-card p-6", children=[
                                            html.P(id="mostPositive", className="text-gray-800 mb-4"),
                                            html.Div(className="flex items-center text-sm text-gray-500", children=[
                                                html.I(className="fas fa-newspaper mr-2"),
                                                html.Span(id="posSource")
                                            ])
                                        ])
                                    ]
                                ),

                                # Most Negative News
                                html.Div(
                                    className="highlight-card bg-white rounded-xl shadow-md overflow-hidden transition-all duration-200 hover:shadow-xl hover:-translate-y-1",
                                    children=[
                                        html.Div(className="bg-red-100 px-6 py-3 flex items-center", children=[
                                            html.I(className="fas fa-frown text-red-600 text-xl mr-3"),
                                            html.H3("Most Negative News", className="text-lg font-semibold text-red-800"),
                                            html.Span(id="negScore", className="ml-auto bg-red-600 text-white text-xs px-2 py-1 rounded-full")
                                        ]),
                                        html.Div(className="news-card p-6", children=[
                                            html.P(id="mostNegative", className="text-gray-800 mb-4"),
                                            html.Div(className="flex items-center text-sm text-gray-500", children=[
                                                html.I(className="fas fa-newspaper mr-2"),
                                                html.Span(id="negSource")
                                            ])  
                                        ])
                                    ]
                                )
                            ]
                        ),

                        # Last Updated
                        html.Div(
                            className="mt-6 text-right text-sm text-gray-500",
                            children=[
                                html.I(className="fas fa-clock mr-1"),
                                html.Span("Last updated: "),
                                html.Span(id="lastUpdated")
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)