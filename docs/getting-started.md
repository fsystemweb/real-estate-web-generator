# Getting started

## Requirements

- **Python 3.12**
- An **OpenAI API key**. Using it costs money (see the note below).
- Optional, only for Opik: **Docker** with Compose v2, and **git**.
- Free ports: 8000, 5500 and 5173.

?> **Cost note:** each request calls OpenAI at least twice (one generator call and one judge call), and up to 3 times each if the score is low. Running the evaluation (`python -m evaluation.run`) sends 50 requests per language, so it costs real money.

## 1. Get the code and install

```bash
git clone https://github.com/fsystemweb/real-state-web-generator.git
cd real-state-web-generator
python3.12 -m venv venv
source venv/bin/activate        # Windows: .\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Set your settings

```bash
cp .env.example .env
```

Open `.env` and set `OPENAI_API_KEY`. Never share this file or commit it to git.

| Variable | Required | What it does |
|---|---|---|
| `OPENAI_API_KEY` | yes | Your OpenAI key |
| `GENERATOR_LLM` | no | Model that writes (default `gpt-6-luna`) |
| `EVALUATOR_LLM` | no | Model that judges (default `gpt-5-nano`) |
| `OPIK_URL_OVERRIDE` | no | Opik address, for example `http://localhost:5173/api`. Turns on tracing |
| `OPIK_PROJECT_NAME` | no | Opik project name, for example `real-estate-listings` |

## 3. Start the API

```bash
python -m app.main
```

The API runs at `http://localhost:8000`. Try it:

```bash
curl -X POST http://localhost:8000/generate-listing \
  -H "Content-Type: application/json" \
  -d '{"title":"T2 in Porto","location":{"city":"Porto"},"features":{"bedrooms":2},"listing_type":"rent","language":"en"}'
```

## 4. Open the demo page (optional)

In a second terminal:

```bash
python -m http.server 5500
```

Open `http://localhost:5500/public/`.

## 5. Start Opik (optional)

Opik shows traces, prompts, datasets and experiments. It runs in Docker.

```bash
scripts/opik.sh          # start it (first time downloads several images)
```

Open `http://localhost:5173`. Then set these in `.env` and restart the API:

```
OPIK_URL_OVERRIDE=http://localhost:5173/api
OPIK_PROJECT_NAME=real-estate-listings
```

Other commands:

| Command | What it does |
|---|---|
| `scripts/opik.sh down` | Stop Opik, keep your data |
| `scripts/opik.sh status` | Show running containers |
| `scripts/opik.sh logs` | Follow the logs |
| `scripts/opik.sh reset` | Stop Opik and **delete** all its data |

?> Opik here is set up for learning only. For real use, follow the [official guide](https://www.comet.com/docs/opik/self-host/local_deployment).

## 6. Run the evaluation (optional, paid)

Needs Opik running and `OPIK_URL_OVERRIDE` set.

```bash
python -m evaluation.run                 # all languages
python -m evaluation.run --language pt   # one language
python -m evaluation.test_metrics        # offline check of the metrics, no API calls
```

## 7. Run these docs locally

```bash
npm i -g docsify-cli
docsify serve docs
```

Or without Node: `python -m http.server 3000 --directory docs`, then open `http://localhost:3000`.

## Troubleshooting

| Problem | Fix |
|---|---|
| `OPENAI_API_KEY not found in environment` | Create `.env` from `.env.example` and set the key |
| Nothing shows up in Opik | Check Opik is running (`scripts/opik.sh status`), that `OPIK_URL_OVERRIDE` is set, and restart the API |
| `Address already in use` | Another program uses the port. Stop it or change the port |
| Demo page cannot reach the API | The API only accepts requests from `http://localhost:5500`. Use that exact address |
| `{"error": ...}` response | Read the message. Often it is a wrong API key or a model name you cannot use |
| HTTP 422 after 3 tries | The judge kept scoring below 3/5. The response lists which criteria failed |
