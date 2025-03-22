#!/bin/bash

for f in $(ls requirements/model); do
    python -m src.infrastructure.cli create-model-requirement --input-file requirements/model/$f
done