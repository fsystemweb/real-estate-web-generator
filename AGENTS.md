# AGENTS.md

FastAPI service that turns structured property JSON into SEO-optimized, multilingual (en/pt/es) HTML listings with LangChain and OpenAI, then scores the output and retries.

## Commands
- Install: `python3.12 -m venv venv`, activate it, then `pip install -r requirements.txt`
- Run the API (port 8000): `python -m app.main`
- Start local Opik (Docker): `scripts/opik.sh [up|down|status|logs|reset]`
- Run the demo web page: `python -m http.server 5500`, then open `http://localhost:5500/public/`
- Evaluation batch: `python -m evaluation.run [--language en|pt|es]` (calls the OpenAI API, logs an experiment to Opik; needs Opik running). Offline metric checks: `python -m evaluation.test_metrics`
- Tests and lint: none configured yet

## Conventions
- Python 3.12, FastAPI, Pydantic 2, LangChain with `langchain-openai`. Dependencies are pinned in `requirements.txt`.
- `app/main.py`: FastAPI app and the `POST /generate-listing` route.
- `app/chains.py`: generator and evaluator chains plus the retry loop (up to 3 attempts while the score is below 3/5).
- `app/models.py`: Pydantic request and response models.
- `app/prompts/`: prompt templates as `.txt` files (Mustache syntax, `{{{variable}}}`), examples and fallback. `app/prompt_loader.py` loads each prompt from Opik first when configured, else from these files; `app/chains.py` uses it. Edit prompts there, not inline.
- `evaluation/`: `datasets/` (per-language CSVs, see `datasets/README.md`), `dataset.py` (CSV loader), `metrics.py` (fact precision and recall as Opik metrics), `test_metrics.py` (offline checks) and `run.py` (the evaluation entry point).
- `public/index.html`: static front end that calls the API.
- Config comes from env vars: `OPENAI_API_KEY`, optional `GENERATOR_LLM` / `EVALUATOR_LLM` (model names; the stronger model generates, the light one evaluates), plus optional `OPIK_URL_OVERRIDE` / `OPIK_PROJECT_NAME` to enable Opik tracing (see `.env.example`). Tracing is off when they are unset.
- If you rename a prompt file, update the file names in `PROMPTS` in `app/prompt_loader.py`.

## Boundaries
- Always: check that edits to `app/prompts/` still cover en, pt and es.
- Ask first: adding a dependency, changing the `/generate-listing` request or response shape, changing the model names or the retry threshold.
- Never: commit secrets or read `.env` files.
- Never: run `evaluation/run.py` without being asked, since it makes paid API calls.
