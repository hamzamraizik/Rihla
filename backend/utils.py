
def map_to_qloo_type(category):
    return {
        "musique": "music",
        "livres": "books",
        "nourriture": "food",
        "lieux": "travel",
        "ambiances": "people",
        "styles": "fashion"
    }.get(category, "people")
