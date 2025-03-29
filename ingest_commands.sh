#!/bin/bash
for f in requirements/application/*.json; do
    python -m src.infrastructure.cli create-command --input-file "$f"
done