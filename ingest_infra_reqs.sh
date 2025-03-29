#!/bin/bash

for f in requirements/infrastructure/*.json; do
    python -m src.infrastructure.cli create-infra-requirement --input-file "$f"
done