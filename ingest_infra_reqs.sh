#!/bin/bash

for f in requirements/infrastructure/*.json; do
    python -m src.interface.cli.main infrastructure-requirement create --text "$(jq -r .requirementText $f)"
done