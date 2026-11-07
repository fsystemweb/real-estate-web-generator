"""Push the local prompts and datasets to Comet Opik when the API starts.

Only what is missing in Opik is created, so edits made in Opik are never overwritten.
Does nothing when Opik is not configured, and never raises (the API starts anyway).
"""
import logging

from app.prompt_loader import PROMPTS, opik_enabled

logger = logging.getLogger(__name__)


def sync_to_opik():
    if not opik_enabled():
        return
    try:
        import opik
        from evaluation.dataset import LANGUAGES, load_rows

        client = opik.Opik()
        for name, local_file in PROMPTS.items():
            if client.get_prompt(name=name) is None:
                client.create_prompt(name=name, prompt=local_file.read_text())
                logger.info("Prompt '%s' created in Opik", name)
        for language in LANGUAGES:
            dataset = client.get_or_create_dataset(name=f"real-estate-{language}")
            if dataset.dataset_items_count:
                continue
            dataset.insert([{"property": prop, "expected_facts": facts}
                            for prop, facts in load_rows(language)])
            logger.info("Dataset 'real-estate-%s' created in Opik", language)
    except Exception as e:
        logger.warning("Opik sync skipped: %s", e)
