"""Load prompts from Comet Opik, falling back to the local files in app/prompts/.

Opik is the source of truth when it is configured and the prompt exists there.
Run `python -m app.prompt_loader` once to push the local files to Opik as a starting point.
"""
import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

PROMPT_DIR = Path(__file__).resolve().parent / "prompts"
PROMPTS = {  # Opik prompt name -> local file
    "real-estate-generator": PROMPT_DIR / "generator_prompt.txt",
    "real-estate-evaluator": PROMPT_DIR / "evaluator_prompt.txt",
}


def opik_enabled():
    return bool(os.getenv("OPIK_URL_OVERRIDE") or os.getenv("OPIK_API_KEY"))


def load_prompt(name, local_file):
    """Return (template_text, source). The source is "opik" or "local". Never raises."""
    if opik_enabled():
        try:
            import opik
            prompt = opik.Opik().get_prompt(name=name)  # latest version
            if prompt:
                logger.info("Prompt '%s' loaded from opik", name)
                return prompt.prompt, "opik"
            logger.info("Prompt '%s' not found in Opik", name)
        except Exception as e:
            logger.warning("Opik unavailable for prompt '%s': %s", name, e)
    logger.info("Prompt '%s' loaded from local file", name)
    return local_file.read_text(), "local"


if __name__ == "__main__":
    import opik

    client = opik.Opik()
    for name, local_file in PROMPTS.items():
        client.create_prompt(name=name, prompt=local_file.read_text())
        print(f"Pushed {name}")
