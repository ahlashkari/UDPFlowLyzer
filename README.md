![](https://github.com/ahlashkari/UDPFlowLyzer/blob/main/bccc.jpg)

# UDPFlowLyzer

UDPFlowLyzer is a UDP network traffic flow analyzer for extracting UDP flow-level features from PCAP/PCAPNG traffic.

## Features

- Extracts UDP packet and flow-level statistics
- Supports configurable flow analysis
- Includes UDP header, timing, volume, burst, entropy, percentile, and statistical feature modules
- Exports extracted flow features for downstream intrusion detection and traffic analysis

## Installation

Create a virtual environment and install the package:

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

## Usage

Run the analyzer with the package entry point or module interface.

Example:

python3 -m NTLFlowLyzer --help

If using a config file:

python3 -m NTLFlowLyzer --config NTLFlowLyzer/config.json

## Repository Structure

- NTLFlowLyzer/: core UDP flow analysis package
- NTLFlowLyzer/features_udp/: UDP feature extraction modules
- NTLFlowLyzer/network_flow_capturer/: packet and flow capture logic
- NTLFlowLyzer/writers/: output writer logic
- docs/: documentation files

## Notes

Large PCAP files, generated CSV outputs, virtual environments, and private datasets are intentionally excluded from this repository.

# Citation & Copyright (c) 2023

For citation in your works and also understanding NTLFlowLyzer completely, you can find below published papers:

- Jafari, S.; Shafi, M. and Lashkari, A. H., Unveiling Hierarchical Machine Learning UDP–QUIC Intrusion Detection: Protocol-Aware Flow Analysis and a New Generated DDoS Dataset, International Conference on Security and Cryptography (SECRYPT) 2026, Portugal

# Contributing

Any contribution is welcome in form of pull requests.


# Project Team members 

* [**Arash Habibi Lashkari:**](http://ahlashkari.com/index.asp) Founder and supervisor

* [**Sepehr Jafari:**](https://github.com/Aeripsen) Research Assistant - York University ( 2025 - 2026)


# Acknowledgment

This project has been made possible through funding from the Natural Sciences and Engineering Research Council of Canada — NSERC (#RGPIN-2020-04701) and Canada Research Chair (Tier II) - (#CRC-2021-00340) to Arash Habibi Lashkari.
