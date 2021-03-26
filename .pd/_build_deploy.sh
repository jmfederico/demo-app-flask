#!/usr/bin/env bash

# Generate the necessary requirements.txt file.
poetry export -f requirements.txt -o requirements.txt --without-hashes

# Build and deploy the application.
pipx run --spec "pd_aws_lambda[deploy]~=1.0" pd_build_and_deploy --wait

# Run Flask migrations.
pipx run --spec "pd_aws_lambda[deploy]~=1.0" pd_run -- python3 -m flask db upgrade
