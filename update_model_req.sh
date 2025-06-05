#!/bin/bash

req_id=$1

python -m src.interface.cli.main model-requirement get -i $req_id | jq -r .requirementText > requirementText.tmp
vim requirementText.tmp
python -m src.interface.cli.main model-requirement update -i $req_id -t "$(cat requirementText.tmp)"
rm requirementText.tmp

# Ask if the requirement should be implemented
read -p "Do you want to implement this requirement now? (Y/n): " implement
implement=${implement:-Y}  # Default to Y if empty

if [[ $implement == "Y" || $implement == "y" ]]; then
    echo "Implementing requirement..."
    python -m src.interface.cli.main model-requirement implement -i $req_id
else
    echo "Skipping implementation."
fi
