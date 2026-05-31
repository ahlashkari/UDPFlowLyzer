#!/usr/bin/env python3

import setuptools

with open(file="README.md", mode="r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UDPFlowLyzer",
    version="0.1.0",
    author="Moein Shafi",
    author_email="moeinsh@yorku.ca",
    description="The UDP Flow Analyzer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahlashkari/UDPFlowLyzer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: York University",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts": ["udpflowlyzer = UDPFlowLyzer.__main__:main"]
    },
)
