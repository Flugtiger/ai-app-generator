#!/bin/bash

for f in requirements/model/*.json; do
    python -m src.infrastructure.cli create-model-requirement --input-file "$f"
done