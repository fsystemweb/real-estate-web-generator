# Glossary

| Word | Simple meaning |
|---|---|
| **LLM** | Large language model. An AI that reads and writes text, like ChatGPT |
| **Prompt** | The instructions and data you send to an LLM |
| **Template** | A prompt with blanks, like `{{{property_json}}}`, filled at run time |
| **Chain** | A few steps joined together: prompt -> model -> result |
| **Generator** | The LLM that writes the listing |
| **LLM as judge** | A second LLM that reads the first one's work and scores it |
| **Retry** | Trying again when the score is too low |
| **Trace** | The full record of one request |
| **Span** | One step inside a trace, such as one model call |
| **Token** | A small piece of text. Models charge by tokens |
| **Dataset** | A list of test inputs, with the facts we expect |
| **Experiment** | One run of a dataset through the app, with scores |
| **Metric** | A number that measures quality |
| **Fact precision** | Of the numbers in the listing, how many were in the input. Low means the model made things up |
| **Fact recall** | Of the numbers in the input, how many appear in the listing. Low means something was left out |
| **SEO** | Search engine optimization. Writing so that search engines can find and rank the page |
| **Meta description** | The short text under a link in search results |
| **Opik** | The open source tool we use to trace, store prompts and run experiments |
| **Docker** | A tool that runs programs in isolated boxes. We use it for Opik |
