#!/bin/bash
for f in requirements/application/*.json; do
    python -m src.interface.cli.main command create --name "$(jq -r .name $f)" --description "$(jq -r .description $f)"
done