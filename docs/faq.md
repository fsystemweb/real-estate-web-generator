# FAQ

**Why does a second model score the first one?**
A model is often better at checking text than at writing it perfectly. The judge catches missing tags, long titles and weak writing, and the app retries.

**Why is the judge a smaller model?**
Reading and scoring is easier than writing. A small model is cheaper and faster.

**Is the judge always right?**
No. That is why we also have the [evaluation](evaluation.md), which checks the facts with plain code, without an LLM.

**How do I change a prompt?**
Edit the `.txt` file in `app/prompts/`, or edit it in Opik (Prompt library -> Edit). Restart the API. If the prompt exists in Opik, the Opik version wins. Always keep en, pt and es working.

**How do I add a language?**
Add it in the language names in `app/chains.py`, update both prompts, add a dataset CSV in `evaluation/datasets/`, and add the language to `LANGUAGES` in `evaluation/dataset.py`. This changes how the app behaves, so discuss it first.

**Do I need Opik?**
No. Without `OPIK_URL_OVERRIDE` everything works, just without traces.

**Why does a request take 20 seconds?**
There are at least two model calls, one after the other, and more if a retry is needed.

**Why did I get a 422 error?**
The judge scored below 3 on three tries in a row. The response lists the failed criteria for each try.

**Where do I see the cost?**
In Opik, on each trace and span.
