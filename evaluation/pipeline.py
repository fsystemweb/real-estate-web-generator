import os
import re
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
from fastapi.testclient import TestClient

from app.main import app
from evaluation.dataset import LANGUAGES, load_rows

client = TestClient(app)

# --- File paths ---
BASE_DIR = "evaluation"
RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

RESULTS_JSON = os.path.join(RESULTS_DIR, "evaluation_results.json")
SUMMARY_CSV = os.path.join(RESULTS_DIR, "evaluation_summary.csv")


def facts_found(html, facts):
    """Share of expected facts (numbers) that appear in the HTML."""
    if not facts:
        return None
    text = re.sub(r"(?<=\d)[,. ](?=\d{3})", "", html)  # 420,000 -> 420000
    text = re.sub(r"(\d+)\.0\b", r"\1", text)
    found = [f for f in facts if re.search(rf"(?<!\d){re.escape(f.removesuffix('.0'))}(?!\d)", text)]
    return len(found) / len(facts)


# --- Load input: optional language argument, e.g. `python -m evaluation.pipeline pt` ---
languages = sys.argv[1:] or LANGUAGES

results = []

for language in languages:
    for prop, expected in load_rows(language):
        response = client.post("/generate-listing", json=prop)
        response_data = response.json()
        results.append({
            "input": prop,
            "expected_facts": expected,
            "output": response_data
        })

# Save raw results
with open(RESULTS_JSON, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# --- Convert to DataFrame ---
rows = []
for item in results:
    lang = item["input"].get("language", "unknown")
    output = item.get("output", {})
    eval_data = output.get("evaluation", {})
    rows.append({
        "title": item["input"].get("title", ""),
        "language": lang,
        "structure_compliance": eval_data.get("structure_compliance"),
        "language_fluency_seo": eval_data.get("language_fluency_seo"),
        "multilingual_adaptability": eval_data.get("multilingual_adaptability"),
        "total_score": eval_data.get("total_score"),
        "missing_or_invalid_tags": ", ".join(eval_data.get("missing_or_invalid_tags", [])),
        "facts_found": facts_found(output.get("html", ""), item["expected_facts"]),
        "retries": output.get("retries", 0),
        "failed_criteria_log": "; ".join(str(x) for x in output.get("failed_criteria_log", []))
    })

df = pd.DataFrame(rows)
df.to_csv(SUMMARY_CSV, index=False)

# --- Graphs ---

# 1. Average scores by language
avg_scores = df.groupby("language")[["structure_compliance", "language_fluency_seo",
                                     "multilingual_adaptability", "total_score", "facts_found"]].mean()

avg_scores.plot(kind="bar")
plt.title("Average Evaluation Scores by Language")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "avg_scores_by_language.png"))
plt.close()

# 2. Distribution of total scores
df["total_score"].value_counts().sort_index().plot(kind="bar")
plt.title("Distribution of Total Scores")
plt.xlabel("Total Score")
plt.ylabel("Number of Listings")
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "total_score_distribution.png"))
plt.close()

# 3. Missing tags count per language
missing_tags_counts = df.groupby("language")["missing_or_invalid_tags"].apply(
    lambda col: col.apply(lambda x: 0 if x == "" else len(x.split(","))).sum()
)

missing_tags_counts.plot(kind="bar")
plt.title("Missing/Invalid Tags by Language")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(RESULTS_DIR, "missing_tags_by_language.png"))
plt.close()
