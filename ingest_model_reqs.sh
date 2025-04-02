#!/bin/bash

for f in requirements/model/*.json; do
    python -m src.interface.cli.main model-requirement create --text "$(jq -r .requirementText $f)"
done