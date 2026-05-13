# NTLFlowLyzer/feature_extractor.py
from __future__ import annotations

from .tcp_feature_extractor import TCPFeatureExtractor
from .udp_feature_extractor import UDPFeatureExtractor

_VALID = {"tcp", "udp"}

def _resolve_protocol(cfg) -> str:
    p = (cfg.get("protocol") or "").strip().lower()
    if p not in _VALID:
        raise ValueError(f'config["protocol"] must be one of {sorted(_VALID)}')
    return p

class FeatureExtractor:
    """
    Public extractor façade. Internally uses TCP/UDP-specific feature registries.
    """
    def __init__(self, config):
        proto = _resolve_protocol(config)
        if proto == "tcp":
            self._impl = TCPFeatureExtractor(config)
        else:
            self._impl = UDPFeatureExtractor(config)

    def extract(self, flows_batch):
        return self._impl.extract(flows_batch)

    def get_header(self):
        return self._impl.get_header()
