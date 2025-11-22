"""Setup script for levlang package."""

from setuptools import setup, find_packages

setup(
    name="levlang",
    version="0.1.0",
    author="Sriram Ramnath",
    author_email="sriramramnath2011@gmail.com",
    description="A simplified game development language that transpiles to Python/pygame",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sriramramnath/language",
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
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Code Generators",
    ],
    license="MIT",
)
