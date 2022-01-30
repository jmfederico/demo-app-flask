from uuid import UUID

from .models import complete_task


def task_lambda_sqs_event_handler(event, context):

    for record in event["Records"]:
        task_uuid = record["body"]
        try:
            UUID(task_uuid)
        except ValueError:
            return

        complete_task(task_uuid)


def task_sqs_handler(message):

    task_uuid = message["Body"]
    try:
        UUID(task_uuid)
    except ValueError:
        return

    complete_task(task_uuid)
