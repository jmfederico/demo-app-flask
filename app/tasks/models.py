from datetime import datetime

from sqlalchemy.dialects import postgresql

from .. import db


class Task(db.Model):
    uuid = db.Column(postgresql.UUID, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)


def complete_task(task_uuid):
    task = Task.query.filter_by(uuid=task_uuid, completed_at=None).first()
    if task:
        task.completed_at = datetime.now()
        db.session.commit()
