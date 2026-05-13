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
