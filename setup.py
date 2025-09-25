from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vidiq-api",
    version="1.0.0",
    author="vidIQ Python API",
    author_email="your.email@example.com",
    description="Python wrapper for vidIQ YouTube keyword analysis API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/vidiq-python-api",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/vidiq-python-api/issues",
        "Documentation": "https://github.com/yourusername/vidiq-python-api#readme",
        "Source Code": "https://github.com/yourusername/vidiq-python-api",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Multimedia :: Video",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    entry_points={
        "console_scripts": [
            "vidiq-api=vidiq_api.vidiq_api:main",
        ],
    },
    keywords="vidiq youtube seo keyword analysis api wrapper",
    include_package_data=True,
    zip_safe=False,
)