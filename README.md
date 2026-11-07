# real-state-web-generator
This project provides a REST API that transforms structured property data (JSON) into SEO-optimized, multilingual HTML listings for real estate websites.
It uses FastAPI, LangChain, and OpenAI for generation and evaluation.

## Features
- ✅ Generates structured HTML (title, meta description, description, features, neighborhood, CTA)
- 🌍 Multilingual support: English 🇬🇧, Portuguese 🇵🇹 and Spanish 🇪🇸
- 🔍 SEO keyword enrichment
- 🧪 Automatic evaluation of output:
    - Structure compliance
    - Language fluency & SEO
    - Multilingual adaptability

- 🔁 Retry mechanism: Up to 3 attempts if evaluation score < 3/5
- 📦 Modular design: Prompts stored separately for easier editing

## Solution

![Solution Diagram](solution.png)

## Installation
 - ``` git clone https://github.com/fsystemweb/real-state-web-generator.git ```
 - ``` cd real-state-web-generator ```

### Create virtual environment
 1. Create a virtual environment called "venv"
  - ``` python3.12 -m venv venv ```
 2. Activate it
  * On Linux / macOS:
    - ``` source venv/bin/activate ```
  * On Windows (PowerShell):
    - ``` .\venv\Scripts\Activate.ps1 ```
 3. Install dependecies:
    - ``` pip install -r requirements.txt ```

* Set environement variable
  - OPENAI_API_KEY=your_openai_api_key_here

## Running the API
 - ``` python -m app.main ```

## Usage
Example Request:
- POST /generate-listing
```json
{
  "title": "T3 apartment in Lisbon",
  "location": {
    "city": "Lisbon",
    "neighborhood": "Campo de Ourique"
  },
  "features": {
    "bedrooms": 3,
    "bathrooms": 2,
    "area_sqm": 120,
    "balcony": true,
    "parking": false,
    "elevator": true,
    "floor": 2,
    "year_built": 2005
  },
  "price": 650000,
  "listing_type": "sale",
  "language": "en"
}
```

Example response: 
```json
{
  "html": "<title>...</title>\n<meta ... > ...",
  "evaluation": {
    "structure_compliance": 5,
    "language_fluency_seo": 4,
    "multilingual_adaptability": 4,
    "total_score": 4
  },
  "retries": 0,
  "failed_criteria_log": []
}
```

## Run app
 1. Start API
  - ``` python -m app.main ```
 2. Start Webapp
  - ``` python -m http.server 5500```
 3. Open browser on this url:
    - ``` http://localhost:5500/public/ ```


## Observability (optional)
Traces (prompts, outputs, evaluator scores and each retry) can be sent to a local [Comet Opik](https://github.com/comet-ml/opik) server. It is off by default.

 1. Start Opik (needs Docker), following the [official docs](https://www.comet.com/docs/opik/self-host/local_deployment):
  - ``` git clone https://github.com/comet-ml/opik.git ```
  - ``` cd opik && ./opik.sh ```
 2. In this project's `.env`, uncomment `OPIK_URL_OVERRIDE` (see `.env.example`) and restart the API.
 3. Call `POST /generate-listing` and open `http://localhost:5173`. Each call is one trace; every attempt is tagged `attempt-1`, `attempt-2`, ...

Without these variables the app runs exactly as before.

## Evaluation Criteria by Request
Each generated listing is automatically evaluated against:

- ✅ Structure compliance (HTML tags + hierarchy)
- 📣 Language fluency & SEO effectiveness
- 🌍 Multilingual adaptability

Each criterion is scored 0–5. The total score must be ≥ 3 to be accepted.

## Evaluation Pipeline
Runs the datasets in `evaluation/datasets/` through the generator and logs an experiment to Opik with two metrics that do not depend on the LLM judge:

- **fact precision**: share of numbers in the listing that come from the input (low = invented details)
- **fact recall**: share of the input numbers that appear in the listing (low = omitted details)

With Opik running and `OPIK_URL_OVERRIDE` set (see Observability), run (makes paid OpenAI calls):
 - ``` python -m evaluation.run ```
 - ``` python -m evaluation.run --language pt ```

Then open `http://localhost:5173` and compare experiments. Offline checks for the metrics (no API calls): ``` python -m evaluation.test_metrics ```

## License
MIT License – free to use and modify.