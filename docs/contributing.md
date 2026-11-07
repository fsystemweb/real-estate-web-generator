# Contributing

## Rules of the project

- **Ask first** before you: add a dependency, change the request or response shape of `/generate-listing`, change the model names, or change the retry threshold.
- When you edit anything in `app/prompts/`, check that it still works for **en, pt and es**.
- Prompts live in `app/prompts/`, not inside Python code. If you rename a prompt file, update `PROMPTS` in `app/prompt_loader.py`.
- **Never commit secrets** or `.env` files.
- Do not run `python -m evaluation.run` by accident. It makes paid API calls.
- There are no automated tests or lint yet. `python -m evaluation.test_metrics` checks the metrics offline.

## Publishing these docs

The docs are a Docsify site in the `docs/` folder. GitHub Pages serves that folder from the `main` branch.

1. Edit or add a Markdown file in `docs/`.
2. If it is a new page, add it to `docs/_sidebar.md`.
3. Preview it: `docsify serve docs`.
4. Open a pull request. When it is merged to `main`, the site updates in a minute or two.

Live site: <https://fsystemweb.github.io/real-state-web-generator/>

Write in short sentences and explain any hard word, or add it to the [Glossary](glossary.md).
