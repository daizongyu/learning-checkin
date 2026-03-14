from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="learning-checkin",
    version="2.0.0",
    description="Local learning check-in system with streak tracking and leaderboard (no network required)",
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
        "Topic :: Productivity",
    ],
    keywords=["learning", "check-in", "streak", "leaderboard", "productivity", "offline", "local"],
    py_modules=["checkin_cli"],
    packages=find_packages(where=".", include=["src*"]),
    python_requires=">=3.8",
    install_requires=[],  # No dependencies!
    entry_points={
        "console_scripts": [
            "learning-checkin=checkin_cli:main",
        ],
    },
    include_package_data=True,
)
