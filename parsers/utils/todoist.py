from todoist.api import TodoistAPI

from parsers.config import settings


def add_task(msg):
    api = TodoistAPI(settings.todoist_token)
    api.items.add(msg, project_id="2272212085", due={"string": "today"})
    api.commit()
