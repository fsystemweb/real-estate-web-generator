"""Load the per-language CSV datasets into API request bodies."""
import csv
from pathlib import Path

DATASET_DIR = Path(__file__).resolve().parent / "datasets"
LANGUAGES = ["en", "pt", "es"]


def _value(text, cast):
    """Empty cell -> None, otherwise cast it."""
    if text == "":
        return None
    if cast is bool:
        return text == "True"
    return cast(text)


def load_rows(language):
    """Return a list of (property_dict, expected_facts) for one language."""
    rows = []
    with open(DATASET_DIR / f"{language}.csv", newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            prop = {
                "title": r["title"],
                "location": {"city": r["city"], "neighborhood": _value(r["neighborhood"], str)},
                "features": {
                    "bedrooms": _value(r["bedrooms"], int),
                    "bathrooms": _value(r["bathrooms"], int),
                    "area_sqm": _value(r["area_sqm"], float),
                    "balcony": _value(r["balcony"], bool),
                    "parking": _value(r["parking"], bool),
                    "elevator": _value(r["elevator"], bool),
                    "floor": _value(r["floor"], int),
                    "year_built": _value(r["year_built"], int),
                },
                "price": _value(r["price"], float),
                "listing_type": r["listing_type"],
                "language": r["language"],
            }
            expected_facts = [f for f in r["expected_facts"].split("|") if f]
            rows.append((prop, expected_facts))
    return rows
