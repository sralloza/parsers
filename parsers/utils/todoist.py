from todoist.api import TodoistAPI

from ..config import settings


def add_task(msg):
    if not settings.todoist_enabled:
        return

    api = TodoistAPI(settings.todoist_token)
    api.items.add(
        msg,
        project_id=settings.todoist_project_id,
        due={"string": settings.todoist_due_str},
    )
    api.commit()
