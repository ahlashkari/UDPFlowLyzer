![](https://github.com/ahlashkari/UDPFlowLyzer/blob/main/bccc.jpg)

# UDPFlowLyzer

**UDP Network Flow Analyzer**

UDPFlowLyzer is a UDP network traffic flow analyzer for extracting UDP flow-level features from PCAP/PCAPNG traffic.

## Features

- Extracts UDP packet and flow-level statistics
- Supports configurable flow analysis
- Includes UDP header, timing, volume, burst, entropy, percentile, and statistical feature modules
- Exports extracted flow features for downstream intrusion detection and traffic analysis

## Feature Visualization

The figure below shows the UDPFlowLyzer feature taxonomy, organized by feature category and subgroup.

![UDPFlowLyzer Feature Taxonomy](UDPFlowLyzer.jpg)

## Installation

Create a virtual environment and install the package:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Usage

Run the analyzer with the package entry point or module interface.
```
python3 -m UDPFlowLyzer --help
```
If using a config file:
```
python3 -m UDPFlowLyzer --config UDPFlowLyzer/config.json
```

## Repository Structure

- `UDPFlowLyzer/`: core UDP flow analysis package
- `UDPFlowLyzer/features_udp/`: UDP feature extraction modules
- `UDPFlowLyzer/network_flow_capturer/`: packet and flow capture logic
- `UDPFlowLyzer/writers/`: output writer logic

## Notes

Large PCAP files, generated CSV outputs, virtual environments, and private datasets are intentionally excluded from this repository.

Contributions are welcome in the form of pull requests. 

## Copyright (c) 2023 & Citation

To cite UDPFlowLyzer in your work and understand it completely, find the following published papers:
```
@inproceedings{jafari_2026,
    author={Jafari, Sepehr and Shafi, MohammadMoein and Lashkari, Arash Habibi},
    title={Unveiling Hierarchical Machine Learning UDP–QUIC Intrusion Detection: Protocol-Aware Flow Analysis and a New Cloud-Generated DDoS Dataset}, 
    booktitle={Proceedings of the 23rd International Conference on Security and Cryptography - Volume 1: SECRYPT}, 
    year={2026},
    pages={46-68},
    isbn = {978-989-758-858-7},
    doi={10.5220/0015033600004103}
}
```


## Team Members 

* [**Arash Habibi Lashkari:**](http://ahlashkari.com/index.asp) Founder and supervisor

* [**Sepehr Jafari:**](https://github.com/Aeripsen) Research Assistant, York University (2025–2026)


## Acknowledgment

This project has been made possible through funding from the Natural Sciences and Engineering Research Council of Canada — NSERC (#RGPIN-2020-04701) and Canada Research Chair (Tier II) - (#CRC-2021-00340) to Arash Habibi Lashkari.
