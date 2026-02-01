"""
Setup script for the package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-document-parser",
    version="1.0.0",
    author="Anas Mohammad",
    author_email="anas.mohammad6673332@gmail.com",
    description="AI-powered document parser with RAG integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pyxon-ai/pyxon-ai-entry-task",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "docparser=cli:cli",
        ],
    },
)
