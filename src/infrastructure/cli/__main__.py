import logging
from src.infrastructure.cli.cli import main

logging.basicConfig(filename='application.log', level=logging.INFO)

if __name__ == "__main__":
    main()
