from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="learning-checkin",
    version="3.0.0",
    description="Simple daily learning check-in tracker - Privacy-first, natural language interface",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Learning Check-in Team",
    author_email="support@learning-checkin.dev",
    license="MIT",
    url="https://github.com/daizongyu/learning-checkin",
    project_urls={
        "Source": "https://github.com/daizongyu/learning-checkin",
        "Tracker": "https://github.com/daizongyu/learning-checkin/issues",
        "Documentation": "https://github.com/daizongyu/learning-checkin/blob/main/SKILL.md",
    },
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
    keywords=["learning", "check-in", "streak", "productivity", "offline", "local", "privacy"],
    py_modules=["checkin_cli"],
    packages=find_packages(where=".", include=["src*"]),
    python_requires=">=3.8",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "learning-checkin=checkin_cli:main",
        ],
    },
    include_package_data=True,
)
