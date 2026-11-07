"""Two deterministic metrics that do not depend on the LLM judge.

- fact precision: of the numbers stated in the listing, how many come from the input?
- fact recall:    of the numbers in the input, how many appear in the listing?

"Numbers" are digits (420,000 / 420.000 / 85) and number words in en/pt/es ("dois", "third").
"""
import re

from opik.evaluation.metrics import BaseMetric
from opik.evaluation.metrics.score_result import ScoreResult

# word -> number. Ambiguous words are left out ("quarto" and "cuarto" mean "room").
WORDS = {}
for number, words in {
    1: "one first um uma primeiro primeira un una primero primera primer",
    2: "two second dois duas segundo segunda dos",
    3: "three third três tres terceiro terceira tercero tercera tercer",
    4: "four fourth quatro cuatro",
    5: "five fifth cinco quinto quinta",
    6: "six sixth seis sexto sexta",
    7: "seven seventh sete siete",
    8: "eight eighth oito ocho",
    9: "nine ninth nove nueve",
    10: "ten tenth dez diez",
    11: "eleven eleventh onze once",
    12: "twelve twelfth doze doce",
}.items():
    for word in words.split():
        WORDS[word] = number


def strip_tags(html):
    """Keep the text of the listing, including the meta description content."""
    html = re.sub(r'<meta[^>]*content="([^"]*)"[^>]*>', r" \1 ", html)
    return re.sub(r"<[^>]+>", " ", html)


def numbers_in(text, include_one=True):
    """All numbers (digits and words) in a text, as a set of floats.

    The word "one" and its translations are skipped when include_one is False,
    because they are often just articles ("um apartamento", "una terraza").
    """
    text = re.sub(r"(?<=\d)[,. ](?=\d{3}\b)", "", text)  # 420,000 -> 420000
    found = {float(n.replace(",", ".")) for n in re.findall(r"\d+(?:[.,]\d+)?", text)}
    for word in re.findall(r"[^\W\d_]+", text.lower()):
        value = WORDS.get(word)
        if value and (include_one or value != 1):
            found.add(float(value))
    return found


def input_numbers(prop):
    """Numbers given in the input property (features, price and the title)."""
    numbers = {float(v) for v in [*prop["features"].values(), prop["price"]]
               if isinstance(v, (int, float)) and not isinstance(v, bool)}
    return numbers | numbers_in(prop["title"])


def fact_precision(html, prop):
    """Share of numbers in the listing that are supported by the input. Returns (score, invented)."""
    stated = numbers_in(strip_tags(html), include_one=False)
    invented = sorted(stated - input_numbers(prop))
    if not stated:
        return 1.0, []
    return (len(stated) - len(invented)) / len(stated), invented


def fact_recall(html, expected_facts):
    """Share of expected facts that appear in the listing. Returns (score, missing)."""
    stated = numbers_in(strip_tags(html))
    missing = [f for f in expected_facts if float(f) not in stated]
    if not expected_facts:
        return 1.0, []
    return (len(expected_facts) - len(missing)) / len(expected_facts), missing


class FactPrecision(BaseMetric):
    def __init__(self):
        super().__init__(name="fact_precision")

    def score(self, html, property, **kwargs):
        if not html:  # generation failed
            return ScoreResult(name=self.name, value=0.0, reason="no listing", scoring_failed=True)
        value, invented = fact_precision(html, property)
        return ScoreResult(name=self.name, value=value, reason=f"unsupported numbers: {invented}")


class FactRecall(BaseMetric):
    def __init__(self):
        super().__init__(name="fact_recall")

    def score(self, html, expected_facts, **kwargs):
        if not html:
            return ScoreResult(name=self.name, value=0.0, reason="no listing", scoring_failed=True)
        value, missing = fact_recall(html, expected_facts)
        return ScoreResult(name=self.name, value=value, reason=f"missing facts: {missing}")
