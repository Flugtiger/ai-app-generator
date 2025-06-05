#!/bin/bash

req_id=$1

python -m src.interface.cli.main model-requirement get -i $req_id | jq -r .requirementText > requirementText.tmp
vim requirementText.tmp
python -m src.interface.cli.main model-requirement update -i $req_id -t "$(cat requirementText.tmp)"
rm requirementText.tmp