from datetime import timedelta
from typing import Any

from backend.danswer.configs.app_configs import LLM_MODEL_UPDATE_API_URL

from danswer.configs.constants import DanswerCeleryPriority


tasks_to_schedule = [
    {
        "name": "check-for-vespa-sync",
        "task": "check_for_vespa_sync_task",
        "schedule": timedelta(seconds=20),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
    {
        "name": "check-for-connector-deletion",
        "task": "check_for_connector_deletion_task",
        "schedule": timedelta(seconds=20),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
    {
        "name": "check-for-indexing",
        "task": "check_for_indexing",
        "schedule": timedelta(seconds=15),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
    {
        "name": "check-for-prune",
        "task": "check_for_pruning",
        "schedule": timedelta(seconds=15),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
    {
        "name": "kombu-message-cleanup",
        "task": "kombu_message_cleanup_task",
        "schedule": timedelta(seconds=3600),
        "options": {"priority": DanswerCeleryPriority.LOWEST},
    },
    {
        "name": "monitor-vespa-sync",
        "task": "monitor_vespa_sync",
        "schedule": timedelta(seconds=5),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
    {
        "name": "check-for-doc-permissions-sync",
        "task": "check_for_doc_permissions_sync",
        "schedule": timedelta(seconds=30),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
    {
        "name": "check-for-external-group-sync",
        "task": "check_for_external_group_sync",
        "schedule": timedelta(seconds=20),
        "options": {"priority": DanswerCeleryPriority.HIGH},
    },
]

# Only add the LLM model update task if the API URL is configured
if LLM_MODEL_UPDATE_API_URL:
    tasks_to_schedule.append(
        {
            "name": "check-for-llm-model-update",
            "task": "check_for_llm_model_update",
            "schedule": timedelta(hours=1),  # Check every hour
            "options": {
                "priority": DanswerCeleryPriority.LOW,
            },
        }
    )


def get_tasks_to_schedule() -> list[dict[str, Any]]:
    return tasks_to_schedule
