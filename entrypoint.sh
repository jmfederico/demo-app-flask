#!/usr/bin/env bash
set -Eeuo pipefail

# Run migrations automatically the first time.
# After the first time, migrations should be run manually.
if ! [[ $(PYTHONUNBUFFERED=0 python -m flask db current) ]]
then
    python -m flask db upgrade
fi

exec "$@"
