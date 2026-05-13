# NTLFlowLyzer/network_flow_analyzer.py
from __future__ import annotations

from .tcp_network_flow_analyzer import TCPNetworkFlowAnalyzer
from .udp_network_flow_analyzer import UDPNetworkFlowAnalyzer

_VALID = {"tcp", "udp"}

def _resolve_protocol(cfg) -> str:
    p = (cfg.get("protocol") or "").strip().lower()
    if p not in _VALID:
        raise ValueError(f'config["protocol"] must be one of {sorted(_VALID)}')
    return p

class NetworkFlowAnalyzer:
    """
    Public analyzer façade. Delegates to protocol-specific analyzers without
    changing their code or behavior.
    """
    def __init__(self, config):
        self.config = config
        proto = _resolve_protocol(config)
        if proto == "tcp":
            self._impl = TCPNetworkFlowAnalyzer(config)
        else:
            self._impl = UDPNetworkFlowAnalyzer(config)

    # keep the surface identical to TCP/UDP analyzers
    def run(self):
        return self._impl.run()
