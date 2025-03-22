#!/bin/bash
for f in $(ls requirements/application); do
    python -m src.infrastructure.cli create-command --input-file requirements/application/$f;
done