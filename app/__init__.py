import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .helpers import get_environ_or_aws_secret
from flask_wtf.csrf import CSRFProtect


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=get_environ_or_aws_secret("DATABASE_URL_SECRET"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQS_URL=os.environ.get("PD_SQS_URL"),
    )
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from . import tasks

    app.register_blueprint(tasks.bp)

    return app


db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
