from todoist.api import TodoistAPI

from parsers.config import settings


def add_task(msg):
    api = TodoistAPI(settings.todoist_token)
    api.items.add(msg, project_id="2188189394", due={"string": "today"})
    api.commit()
