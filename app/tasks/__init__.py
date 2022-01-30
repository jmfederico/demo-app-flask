import os
import sys
from datetime import datetime
from time import sleep
from uuid import uuid4

import boto3
import click
from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from sqlalchemy.dialects import postgresql

from .. import db
from .models import Task
from .sqs import task_sqs_handler

bp = Blueprint("tasks", __name__, template_folder="templates")

client = boto3.client("sqs", endpoint_url=os.environ.get("BOTO_ENDPOINT_URL"))


@bp.route("/", methods=("GET", "POST"))
def tasks():
    if request.method == "POST":
        if "clear" in request.form:
            Task.query.delete()
            db.session.commit()
            return redirect(url_for("tasks.tasks"))

        task_uuid = str(uuid4())
        db.session.add(Task(uuid=task_uuid, created_at=datetime.now()))
        db.session.commit()

        if current_app.config["SQS_URL"]:
            client.send_message(
                QueueUrl=current_app.config["SQS_URL"],
                DelaySeconds=10,
                MessageBody=task_uuid,
            )

        return redirect(url_for("tasks.tasks"))

    return render_template(
        "tasks.html",
        tasks=Task.query.order_by(Task.created_at.desc()).all(),
        form=FlaskForm(),
    )


@bp.cli.command("consume-sqs")
def consume_sqs():
    click.echo("Consuming SQS messages from %s" % current_app.config["SQS_URL"])
    try:
        while True:
            if not _consume_sqs():
                sleep(5)
    except KeyboardInterrupt:
        sys.exit(0)


def _consume_sqs():
    click.echo("Receiving messages")
    response = client.receive_message(
        QueueUrl=current_app.config["SQS_URL"],
        MaxNumberOfMessages=10,
        WaitTimeSeconds=0,
    )

    messages = response.get("Messages", None)
    if not messages:
        click.echo("No messages")
        return messages

    for message in response["Messages"]:
        click.echo("Processing message [%s]" % message["MessageId"])
        task_sqs_handler(message)
        receipt_handle = message["ReceiptHandle"]
        client.delete_message(
            QueueUrl=current_app.config["SQS_URL"], ReceiptHandle=receipt_handle
        )
        click.echo("Message consumed [%s]" % message["MessageId"])

    return messages
