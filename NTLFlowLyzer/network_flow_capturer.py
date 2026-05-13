# NTLFlowLyzer/network_flow_capturer.py
from __future__ import annotations

from .network_flow_capturer.tcp_network_flow_capturer import TCPNetworkFlowCapturer
from .network_flow_capturer.udp_network_flow_capturer import UDPNetworkFlowCapturer

_VALID = {"tcp", "udp"}

def _resolve_protocol(cfg) -> str:
    p = (cfg.get("protocol") or "").strip().lower()
    if p not in _VALID:
        raise ValueError(f'config["protocol"] must be one of {sorted(_VALID)}')
    return p

class NetworkFlowCapturer:
    """
    Public capturer façade. Downstream code can type against this single class.
    """
    def __init__(self, config, *args, **kwargs):
        proto = _resolve_protocol(config)
        if proto == "tcp":
            self._impl = TCPNetworkFlowCapturer(config, *args, **kwargs)
        else:
            self._impl = UDPNetworkFlowCapturer(config, *args, **kwargs)

    # pass-through of the methods your capturers expose
    def capture(self):
        return self._impl.capture()

    def close(self):
        return self._impl.close()
