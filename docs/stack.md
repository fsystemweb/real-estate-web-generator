# Stack

| Area | Tool | Why we use it |
|---|---|---|
| Language | Python 3.12 | Simple and popular for AI work |
| API | FastAPI + Uvicorn | Fast to write, checks input automatically |
| Data checks | Pydantic 2 | Makes sure the request has the right shape |
| LLM framework | LangChain (`langchain-openai`) | Connects prompt -> model -> result in small steps ("chains") |
| Models | OpenAI | A stronger model **generates**, a light model **judges** |
| Tracing, prompts, datasets, experiments | [Comet Opik](https://github.com/comet-ml/opik) | See what the models did and measure quality. Runs locally with Docker |
| Front end | One static page (`public/index.html`) | A demo that calls the API |
| Docs | Docsify | Turns Markdown files into a website, no build step |

## Models

| Role | Default | Setting |
|---|---|---|
| Generator (writes the listing) | `gpt-6-luna` | `GENERATOR_LLM` |
| Evaluator / judge (scores it) | `gpt-5-nano` | `EVALUATOR_LLM` |

The stronger model writes. The cheaper one only has to read and score, so it is a good place to save money.

## Python packages

Pinned in `requirements.txt`: `langchain`, `langchain-openai`, `fastapi`, `uvicorn`, `pydantic`, `python-dotenv` and `opik`.

## Ports

| Port | What |
|---|---|
| 8000 | The API |
| 5500 | The demo page (optional) |
| 5173 | The Opik web page (optional) |
