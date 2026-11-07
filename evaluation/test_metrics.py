"""Offline checks for the metrics (no API calls). Run: python -m evaluation.test_metrics"""
from evaluation.metrics import fact_precision, fact_recall, numbers_in

PROP = {
    "title": "T2 em Alfama",
    "features": {"bedrooms": 2, "bathrooms": 1, "area_sqm": 85.0, "balcony": True, "floor": 3, "year_built": 1950},
    "price": 420000.0,
}
GOOD = ('<title>T2 em Alfama</title><meta name="description" content="Apartamento de 85 m² por €420,000.">'
        "<p>Dois quartos, 1 casa de banho, terceiro andar, construído em 1950.</p>")
INVENTED = GOOD + "<p>A 5 minutos do metro, com 2 lugares de garagem e 12 anos de garantia.</p>"
MISSING = "<p>Apartamento com 85 m² em Alfama, por €420.000.</p>"


def test_number_formats():
    assert {420000.0, 85.0} <= numbers_in("€420,000 and 420.000 and 85 m²")
    assert {2.0, 3.0} <= numbers_in("dois quartos, terceiro andar")


def test_good_listing():
    assert fact_precision(GOOD, PROP)[0] == 1.0
    assert fact_recall(GOOD, ["2", "1", "85", "3", "1950", "420000"])[0] == 1.0


def test_invented_number_lowers_precision():
    score, invented = fact_precision(INVENTED, PROP)
    assert score < 1.0 and 5.0 in invented and 12.0 in invented


def test_missing_fact_lowers_recall():
    score, missing = fact_recall(MISSING, ["2", "1", "85", "3", "1950", "420000"])
    assert score == 2 / 6 and missing == ["2", "1", "3", "1950"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
