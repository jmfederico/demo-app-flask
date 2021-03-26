from datetime import datetime
from uuid import uuid4

import boto3
from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from sqlalchemy.dialects import postgresql

from . import db

bp = Blueprint("tasks", __name__)

client = boto3.client("sqs")


class Task(db.Model):
    uuid = db.Column(postgresql.UUID, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)


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

    return render_template("tasks.html", tasks=Task.query.all(), form=FlaskForm())


def complete_task(task_uuid):
    task = Task.query.filter_by(uuid=task_uuid, completed_at=None).first()
    if task:
        task.completed_at = datetime.now()
        db.session.commit()
