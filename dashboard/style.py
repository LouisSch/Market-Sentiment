color_map = {
    "positive": "#28a745",
    "neutral": "#ffc107",
    "negative": "#dc3545"
}

def get_badge_color(polarization: str):
    text = polarization.lower()

    for key in color_map:
        if key in text:
            return color_map[key]
    
    return "#6c757d"