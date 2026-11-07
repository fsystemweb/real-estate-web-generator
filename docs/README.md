# Real Estate Listing Generator

You give it facts about a property (city, bedrooms, price...). It gives you a ready-to-publish web page text for that property, in **English, Portuguese or Spanish**.

It is a small project made to **learn** how to build with AI models in a careful way:

- **Generate** text with an LLM (a large language model, like ChatGPT).
- **Check** the text with a second LLM that acts as a judge, and try again if the score is low.
- **See** everything that happens with traces (Opik).
- **Manage** prompts and **measure** quality with datasets and experiments.

## What goes in and what comes out

Send this to `POST /generate-listing`:

```json
{
  "title": "T3 apartment in Lisbon",
  "location": { "city": "Lisbon", "neighborhood": "Campo de Ourique" },
  "features": {
    "bedrooms": 3, "bathrooms": 2, "area_sqm": 120, "balcony": true,
    "parking": false, "elevator": true, "floor": 2, "year_built": 2005
  },
  "price": 650000,
  "listing_type": "sale",
  "language": "en"
}
```

You get back:

```json
{
  "html": "<title>...</title> <meta ...> <h1>...</h1> ...",
  "evaluation": {
    "structure_compliance": 5,
    "language_fluency_seo": 4,
    "multilingual_adaptability": 4,
    "total_score": 4,
    "missing_or_invalid_tags": []
  },
  "retries": 0,
  "failed_criteria_log": []
}
```

Only `title`, `location.city`, `listing_type` and `language` are required. If something fails, the API returns `{"error": "..."}`.

## The HTML it writes

Every listing has the same parts, so search engines and people can read it easily:

| Part | What it is |
|---|---|
| `<title>` | Page title, up to 60 characters |
| `<meta name="description">` | Short summary for search results, up to 155 characters |
| `<h1>` | Main heading |
| `<section id="description">` | The main description |
| `<ul id="key-features">` | Bullet list of key features |
| `<section id="neighborhood">` | About the area |
| `<p class="call-to-action">` | A closing sentence that invites contact |

## Where to go next

- New here? Start with [Getting started](getting-started.md).
- Want to know how it works? Read [Architecture](architecture.md).
- Want to see traces, prompts and experiments? Open [Observability with Opik](observability.md).
- Stuck on a word? See the [Glossary](glossary.md).

Source code: [github.com/fsystemweb/real-state-web-generator](https://github.com/fsystemweb/real-state-web-generator). License: MIT.
