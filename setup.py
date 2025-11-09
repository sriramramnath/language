"""Setup script for levlang package."""

from setuptools import setup, find_packages

setup(
    name="levlang",
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
            "levlang=levlang.cli.main:main",
        ],
    },
    python_requires=">=3.8",
)
