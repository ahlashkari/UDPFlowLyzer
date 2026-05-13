"""Statistical moment features over packet and payload sizes."""
from .base import Feature
import numpy as np

def skewness(data):
    """Calculate skewness using numpy - γ = E[(X-μ)³]/σ³."""
    data = np.asarray(data)
    if len(data) < 3:
        return 0.0
    mean = np.mean(data)
    std = np.std(data, ddof=0)
    if std == 0:
        return 0.0
    return np.mean(((data - mean) / std) ** 3)

def kurtosis(data):
    """Calculate kurtosis using numpy - κ = E[(X-μ)⁴]/σ⁴ - 3."""
    data = np.asarray(data)
    if len(data) < 4:
        return 0.0
    mean = np.mean(data)
    std = np.std(data, ddof=0)
    if std == 0:
        return 0.0
    return np.mean(((data - mean) / std) ** 4) - 3

class PacketSizeSkewFeature(Feature):
    """Packet size skewness - third moment about the mean - γ = E[(X-μ)³]/σ³."""
    name = "pkt_size_skew"
    category = "stat"
    min_samples = 3
    min_moment_samples = 5  # Reduced from 50 to work with typical UDP flows
    paper_reference = "Pearson (1895) - Skewness and Asymmetry"
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < max(self.min_samples, 3):  # Need at least 3 for skewness
            return 0.0
        return float(skewness(sizes))

class PacketSizeKurtFeature(Feature):
    """Packet size kurtosis - fourth moment about the mean - κ = E[(X-μ)⁴]/σ⁴ - 3."""
    name = "pkt_size_kurt"
    category = "stat"
    min_samples = 4
    min_moment_samples = 6  # Reduced from 50 to work with typical UDP flows
    paper_reference = "Pearson (1905) - Das Fehlergesetz und seine Verallgemeinerungen"
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < max(self.min_samples, 4):  # Need at least 4 for kurtosis
            return 0.0
        return float(kurtosis(sizes))

class MedianPacketSizeFeature(Feature):
    """Median packet size in bytes."""
    name = "median_pkt_size"
    category = "stat"
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        return float(np.median(sizes)) if len(sizes) > 0 else 0.0

class PacketSizeCOVFeature(Feature):
    """Packet size coefficient of variation - σ/μ."""
    name = "pkt_size_cov"
    category = "stat"
    min_samples = 2
    paper_reference = "Pearson (1896) - Mathematical Contributions to Evolution"
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_samples:
            return 0.0
        mean_size = np.mean(sizes)
        if mean_size == 0:
            return 0.0
        return float(np.std(sizes) / mean_size)

class PayloadSizeSkewFeature(Feature):
    """Skewness of payload sizes (third standardized moment) - L2-L4 analysis."""
    name = "payload_size_skew"
    category = "stat"
    min_samples = 5
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        # Extract payload sizes (packet content, not deep inspection)
        payload_sizes = np.array([pkt.get_payloadbytes() for pkt in packets])
        
        if len(payload_sizes) < self.min_samples:
            return 0.0
        
        # Calculate skewness
        mean = np.mean(payload_sizes)
        std = np.std(payload_sizes)
        
        if std == 0:
            return 0.0
        
        # Third standardized moment
        skewness = np.mean(((payload_sizes - mean) / std) ** 3)
        return float(skewness)

class PayloadSizeKurtFeature(Feature):
    """Kurtosis of payload sizes (fourth standardized moment) - L2-L4 analysis."""
    name = "payload_size_kurt"
    category = "stat"
    min_samples = 5
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        # Extract payload sizes (packet content, not deep inspection)
        payload_sizes = np.array([pkt.get_payloadbytes() for pkt in packets])
        
        if len(payload_sizes) < self.min_samples:
            return 0.0
        
        # Calculate kurtosis (excess kurtosis)
        mean = np.mean(payload_sizes)
        std = np.std(payload_sizes)
        
        if std == 0:
            return 0.0
        
        # Fourth standardized moment minus 3 (excess kurtosis)
        kurtosis = np.mean(((payload_sizes - mean) / std) ** 4) - 3
        return float(kurtosis)

class HeaderSizeSkewFeature(Feature):
    """Skewness of header sizes (third standardized moment)."""
    name = "header_size_skew"
    category = "stat"
    
    def __init__(self, *, min_moment_samples: int = 5, **kwargs):  # Reduced from 50
        super().__init__(**kwargs)
        self.min_moment_samples = min_moment_samples
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < max(3, self.min_moment_samples):
            return 0.0
        
        # Calculate header sizes for each packet
        header_sizes = []
        for pkt in packets:
            eth_size = 14  # Ethernet header
            ip_size = getattr(pkt, 'ip_header_len', 20)  # IP header
            udp_size = 8   # UDP header
            total_header = eth_size + ip_size + udp_size
            header_sizes.append(total_header)
        
        header_array = np.array(header_sizes)
        
        # Calculate skewness
        mean = np.mean(header_array)
        std = np.std(header_array)
        
        if std == 0:
            return 0.0
        
        # Third standardized moment
        skewness = np.mean(((header_array - mean) / std) ** 3)
        return float(skewness)

class HeaderSizeKurtFeature(Feature):
    """Kurtosis of header sizes (fourth standardized moment)."""
    name = "header_size_kurt"
    category = "stat"
    
    def __init__(self, *, min_moment_samples: int = 6, **kwargs):  # Reduced from 50
        super().__init__(**kwargs)
        self.min_moment_samples = min_moment_samples
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < max(4, self.min_moment_samples):
            return 0.0
        
        # Calculate header sizes for each packet
        header_sizes = []
        for pkt in packets:
            eth_size = 14  # Ethernet header
            ip_size = getattr(pkt, 'ip_header_len', 20)  # IP header
            udp_size = 8   # UDP header
            total_header = eth_size + ip_size + udp_size
            header_sizes.append(total_header)
        
        header_array = np.array(header_sizes)
        
        # Calculate kurtosis
        mean = np.mean(header_array)
        std = np.std(header_array)
        
        if std == 0:
            return 0.0
        
        # Fourth standardized moment
        kurtosis = np.mean(((header_array - mean) / std) ** 4)
        return float(kurtosis)

class SizeTimeCorrelationFeature(Feature):
    """Correlation between packet size and arrival time."""
    name = "size_time_correlation"
    category = "stat"
    min_samples = 5
    requires_timestamps = True
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        # Extract sizes and timestamps
        sizes = np.array([pkt.get_length() for pkt in packets])
        timestamps = np.array([pkt.get_timestamp() for pkt in packets])
        
        if len(sizes) != len(timestamps) or len(sizes) < self.min_samples:
            return 0.0
        
        # Calculate correlation coefficient
        try:
            correlation = np.corrcoef(sizes, timestamps)[0, 1]
            return float(correlation) if not np.isnan(correlation) else 0.0
        except Exception:
            return 0.0

class PacketSizeVarianceFeature(Feature):
    """Packet size variance - σ² = E[(X-μ)²]."""
    name = "pkt_size_var"
    category = "stat"
    min_samples = 2
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_samples:
            return 0.0
        return float(np.var(sizes))

class PacketSizeRangeFeature(Feature):
    """Packet size range (max - min)."""
    name = "pkt_size_range"
    category = "stat"
    
    def extract(self, flow) -> int:
        sizes = [pkt.get_length() for pkt in flow.get_packets()]
        if not sizes:
            return 0
        return max(sizes) - min(sizes) 