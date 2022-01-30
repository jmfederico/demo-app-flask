FROM python:3.8-slim as base

ENV PYTHONUNBUFFERED=1

ADD https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py /poetry/
RUN python /poetry/get-poetry.py

ENV PATH="/root/.poetry/bin:${PATH}"
RUN poetry config virtualenvs.create false

# Define function directory
ARG FUNCTION_DIR="/function"

# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY entrypoint.sh /usr/local/bin/pd_entrypoint
RUN chmod +x /usr/local/bin/pd_entrypoint

ENTRYPOINT [ "pd_entrypoint" ]

# Copy function code
COPY . .

CMD [ "flask", "run", "--port", "80", "--host", "0.0.0.0" ]


# Fargate compatible image.
# Use gunicorn to handle requests.
FROM base as fargate

CMD [ "gunicorn", "--capture-output", "--access-logfile", "-", "app.wsgi:app", "-b", "0.0.0.0:80" ]


# Fargate compatible image.
# Use awslambdaric to handle lambda requests.
FROM base as lambda

# Important!
# This CMD is required for your image to be compatible with
# AWS Lambda and Python Deploy.
CMD [ "python", "-m", "awslambdaric", "pd_aws_lambda.dispatcher.dispatcher" ]
