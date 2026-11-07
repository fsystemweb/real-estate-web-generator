"""Run the evaluation and log it to Opik as an experiment.

    python -m evaluation.run              # all languages
    python -m evaluation.run --language pt

Needs OPENAI_API_KEY and a running Opik (OPIK_URL_OVERRIDE). Makes paid API calls.
"""
import argparse
import os

import opik
from opik.evaluation import evaluate

from app.chains import generate_and_evaluate
from app.models import PropertyData
from evaluation.dataset import LANGUAGES, load_rows
from evaluation.metrics import FactPrecision, FactRecall


def task(item):
    """Generate one listing from a dataset item."""
    try:
        result = generate_and_evaluate(PropertyData(**item["property"]))
        return {"html": result["html"], "retries": result["retries"]}
    except Exception as e:  # e.g. the judge never reached the minimum score
        return {"html": "", "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--language", choices=LANGUAGES, help="default: all languages")
    args = parser.parse_args()

    if not (os.getenv("OPIK_URL_OVERRIDE") or os.getenv("OPIK_API_KEY")):
        raise SystemExit("Set OPIK_URL_OVERRIDE (see .env.example) and start Opik first.")

    client = opik.Opik()
    for language in [args.language] if args.language else LANGUAGES:
        dataset = client.get_or_create_dataset(name=f"real-estate-{language}")
        dataset.insert([{"property": prop, "expected_facts": facts}
                        for prop, facts in load_rows(language)])  # duplicates are skipped
        evaluate(
            dataset=dataset,
            task=task,
            scoring_metrics=[FactPrecision(), FactRecall()],
            experiment_name_prefix=f"listings-{language}",
            task_threads=4,
        )


if __name__ == "__main__":
    main()
