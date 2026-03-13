#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script for learning-checkin package
Alternative to pyproject.toml for older pip versions
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="learning-checkin",
    version="1.0.0",
    description="Global learning check-in system with streak tracking and leaderboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Learning Check-in Team",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Education",
    ],
    keywords=["learning", "check-in", "streak", "leaderboard", "productivity"],
    py_modules=["checkin_cli"],
    packages=find_packages(where=".", include=["src*"]),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "learning-checkin=checkin_cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json"],
    },
)
