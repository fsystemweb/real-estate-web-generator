# AGENTS.md

FastAPI service that turns structured property JSON into SEO-optimized, multilingual (en/pt/es) HTML listings with LangChain and OpenAI, then scores the output and retries.

## Commands
- Install: `python3.12 -m venv venv`, activate it, then `pip install -r requirements.txt`
- Run the API (port 8000): `python -m app.main`
- Run the demo web page: `python -m http.server 5500`, then open `http://localhost:5500/public/`
- Evaluation batch: `python -m evaluation.pipeline` (calls the OpenAI API, writes to `evaluation/results/`)
- Tests and lint: none configured yet

## Conventions
- Python 3.12, FastAPI, Pydantic 2, LangChain with `langchain-openai`. Dependencies are pinned in `requirements.txt`.
- `app/main.py`: FastAPI app and the `POST /generate-listing` route.
- `app/chains.py`: generator and evaluator chains plus the retry loop (up to 3 attempts while the score is below 3/5).
- `app/models.py`: Pydantic request and response models.
- `app/prompts/`: prompt templates as `.txt` files, loaded by `app/chains.py`. Edit prompts there, not inline.
- `evaluation/`: `data_input.json` sample inputs and `pipeline.py`, which writes results JSON, CSV and charts.
- `public/index.html`: static front end that calls the API.
- Config comes from env vars; the only documented one is `OPENAI_API_KEY` (see `.env.example`).
- If you rename a prompt file, update the file names read in `app/chains.py`.

## Boundaries
- Always: check that edits to `app/prompts/` still cover en, pt and es.
- Ask first: adding a dependency, changing the `/generate-listing` request or response shape, changing the model names or the retry threshold.
- Never: commit secrets or read `.env` files.
- Never: run `evaluation/pipeline.py` without being asked, since it makes paid API calls.
