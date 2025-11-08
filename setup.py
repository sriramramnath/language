"""Setup script for gamelang package."""

from setuptools import setup, find_packages

setup(
    name="gamelang",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gamelang=gamelang.cli.main:main",
        ],
    },
    python_requires=">=3.8",
)
