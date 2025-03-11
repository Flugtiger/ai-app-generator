from setuptools import setup, find_packages

setup(
    name="ddd-model-generator",
    version="0.1.0",
    description="Domain-Driven Design Model Generator",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pydantic>=1.9.0,<2.0.0",
        "typer>=0.4.0",
        "rich>=10.0.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "ddd-model-generator=src.infrastructure.cli.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
