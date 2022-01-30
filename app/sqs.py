from . import create_app

app = create_app()

def get_lambda_sqs_event_handler():
    from tasks.sqs import task_lambda_sqs_event_handler

    return task_lambda_sqs_event_handler


lambda_sqs_event_handler = get_lambda_sqs_event_handler()
