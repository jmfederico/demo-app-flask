from uuid import UUID

from . import create_app
from .tasks import complete_task

app = create_app()


def sqs_event_handler(event, context):
    with app.app_context():
        for record in event["Records"]:
            task_uuid = record["body"]
            try:
                UUID(task_uuid)
            except ValueError:
                return

            complete_task(task_uuid)
