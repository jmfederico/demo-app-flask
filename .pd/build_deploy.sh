#!/usr/bin/env bash

# Build and deploy!
exec docker \
    run --rm \
    -v "${PWD}:/pd_app" -w /pd_app \
    --env-file .pd/.env \
    lambci/lambda:build-python3.8 ./.pd/_build_deploy.sh
