import logging
from dotenv import load_dotenv
import os
load_dotenv()
import re
import json

from fastapi import HTTPException
from app.models import PropertyData
from app.prompt_loader import load_prompt, opik_enabled
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# Opik tracing is opt-in: it only turns on when an Opik URL or API key is set.
OPIK_ENABLED = opik_enabled()
if OPIK_ENABLED:
    from opik import track
    from opik.integrations.langchain import OpikTracer
else:
    def track(name=None):  # no-op decorator when Opik is off
        return lambda fn: fn


def trace_config(attempt):
    """LangChain config that sends each chain call to Opik (empty when Opik is off)."""
    if not OPIK_ENABLED:
        return {}
    return {"callbacks": [OpikTracer(tags=[f"attempt-{attempt}"])]}


# Ensure your OpenAI API key is set
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY not found in environment")

# Load prompt templates (Opik first, local files in app/prompts/ as fallback).
# Both use Mustache syntax: {{{variable}}} (triple braces so HTML is not escaped).
generator_template, _ = load_prompt("real-estate-generator")
evaluator_template, _ = load_prompt("real-estate-evaluator")

generator_prompt = PromptTemplate.from_template(generator_template, template_format="mustache")
evaluator_prompt = PromptTemplate.from_template(evaluator_template, template_format="mustache")

# Initialize ChatOpenAI with API key
# The stronger model generates, the light one evaluates. Override with env vars.
def build_llm(model, temperature):
    """ChatOpenAI client; only gpt-4*/gpt-3.5* are known to accept a custom temperature, newer models need the default."""
    kwargs = {"model": model, "api_key": openai_api_key}
    if re.match(r"^(gpt-4|gpt-3\.5)", model):
        kwargs["temperature"] = temperature
    return ChatOpenAI(**kwargs)


generator_llm = build_llm(os.getenv("GENERATOR_LLM", "gpt-6-luna"), 0.7)
evaluator_llm = build_llm(os.getenv("EVALUATOR_LLM", "gpt-5-nano"), 0)

# Setup chains using LCEL (LangChain Expression Language)
output_parser = StrOutputParser()
generator_chain = generator_prompt | generator_llm | output_parser
evaluator_chain = evaluator_prompt | evaluator_llm | output_parser

MAX_RETRIES = 3
MIN_SCORE = 3

@track(name="generate_listing")
def generate_and_evaluate(property_data: PropertyData):
    logger.info("Request: %s", property_data)
    retries = 0
    failed_criteria_log = []

    language_names = {"en": "English", "pt": "Portuguese", "es": "Spanish"}
    language_code = property_data.language if property_data.language in language_names else "en"
    language_name = language_names[language_code]
    logger.info("Language Code: %s", language_code)

    while retries < MAX_RETRIES:
        html_output = generator_chain.invoke({
            "property_json": property_data.model_dump_json(),
            "language_name": language_name,
            "language_code": language_code
        }, config=trace_config(retries + 1))
        logger.info("HTML Output: %s", html_output)
        
        evaluation_str = evaluator_chain.invoke({"html_output": html_output}, config=trace_config(retries + 1))
        evaluation_str = re.sub(r"^```.*\n|```$", "", evaluation_str.strip(), flags=re.MULTILINE)
        
        try:
            evaluation_json = json.loads(evaluation_str)
        except json.JSONDecodeError:
            logger.error("Invalid evaluator JSON: %s", evaluation_str)
            raise HTTPException(status_code=500, detail="Evaluator returned invalid JSON")
        
        logger.info("Evaluation JSON: %s", evaluation_json)

        total_score = evaluation_json.get("total_score", 0)

        if total_score >= MIN_SCORE:
            return {
                "html": html_output,
                "evaluation": evaluation_json,
                "retries": retries,
                "failed_criteria_log": failed_criteria_log
            }

        failing_criteria = {
            k: int(v) for k, v in evaluation_json.items()
            if k != "total_score" and int(v) < MIN_SCORE
        }
        failed_criteria_log.append({"retry": retries + 1, "failing_criteria": failing_criteria})
        retries += 1

    raise HTTPException(
        status_code=422,
        detail={
            "message": f"Generated content did not reach minimum score {MIN_SCORE} after {MAX_RETRIES} attempts",
            "failed_criteria_log": failed_criteria_log
        },
    )
