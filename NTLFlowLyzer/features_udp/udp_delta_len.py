"""Features derived from differences in packet, header, and payload lengths."""
from .base import Feature
import numpy as np
import logging

logger = logging.getLogger(__name__)

def _warn_negative(deltas, flow):
    if len(deltas) > 0 and np.all(deltas < 0):
        logger.debug("All size deltas negative for flow %s: %s", flow, deltas)

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

class DeltaPktSizeMinFeature(Feature):
    """Minimum of successive packet size differences - min(|Δs_i|)."""
    name = "delta_pkt_size_min"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10 to work with typical UDP flows
    paper_reference = "Successive difference analysis for traffic characterization"
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(np.min(deltas))

class DeltaPktSizeMaxFeature(Feature):
    """Maximum of successive packet size differences - max(|Δs_i|)."""
    name = "delta_pkt_size_max"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(np.max(deltas))

class DeltaPktSizeMeanFeature(Feature):
    """Mean of successive packet size differences - μ(|Δs_i|)."""
    name = "delta_pkt_size_mean"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(np.mean(deltas))

class DeltaPktSizeStdFeature(Feature):
    """Standard deviation of successive packet size differences - σ(|Δs_i|)."""
    name = "delta_pkt_size_std"
    category = "delta"
    min_samples = 3
    min_delta_samples = 3  # Reduced from 10, but need 3 for std
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(np.std(deltas))

class DeltaPktSizeMedianFeature(Feature):
    """Median of successive packet size differences."""
    name = "delta_pkt_size_median"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(np.median(deltas))

class DeltaPktSizeVarFeature(Feature):
    """Variance of successive packet size differences - σ²(|Δs_i|)."""
    name = "delta_pkt_size_var"
    category = "delta"
    min_samples = 3
    min_delta_samples = 3  # Reduced from 10, need 3 for variance
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(np.var(deltas))

class DeltaPktSizeSkewFeature(Feature):
    """Skewness of successive packet size differences - γ(|Δs_i|)."""
    name = "delta_pkt_size_skew"
    category = "delta"
    min_samples = 4
    min_delta_samples = 4  # Reduced from 10, need 4 for skewness
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        return float(skewness(deltas))

class DeltaPktSizeCovFeature(Feature):
    """Coefficient of variation of successive packet size differences - σ/μ."""
    name = "delta_pkt_size_cov"
    category = "delta"
    min_samples = 3
    min_delta_samples = 3  # Reduced from 10
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(sizes))  # Use absolute differences
        mean_delta = np.mean(deltas)
        if mean_delta == 0:
            return 0.0
        return float(np.std(deltas) / mean_delta)

# Header size delta features
class DeltaHdrSizeMeanFeature(Feature):
    """Mean of successive header size differences."""
    name = "delta_hdr_size_mean"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        header_sizes = np.array([pkt.get_length() - pkt.get_payloadbytes() 
                               for pkt in flow.get_packets()])
        if len(header_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(header_sizes))  # Use absolute differences
        return float(np.mean(deltas))

class DeltaHdrSizeStdFeature(Feature):
    """Standard deviation of successive header size differences."""
    name = "delta_hdr_size_std"
    category = "delta"
    min_samples = 3
    min_delta_samples = 3  # Reduced from 10
    
    def extract(self, flow) -> float:
        header_sizes = np.array([pkt.get_length() - pkt.get_payloadbytes() 
                               for pkt in flow.get_packets()])
        if len(header_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(header_sizes))  # Use absolute differences
        return float(np.std(deltas))

class DeltaHdrSizeMaxFeature(Feature):
    """Maximum of successive header size differences."""
    name = "delta_hdr_size_max"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        header_sizes = np.array([pkt.get_length() - pkt.get_payloadbytes() 
                               for pkt in flow.get_packets()])
        if len(header_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(header_sizes))  # Use absolute differences
        return float(np.max(deltas))

# Payload size delta features
class DeltaPaySizeMeanFeature(Feature):
    """Mean of successive payload size differences."""
    name = "delta_pay_size_mean"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        payload_sizes = np.array([pkt.get_payloadbytes() for pkt in flow.get_packets()])
        if len(payload_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(payload_sizes))  # Use absolute differences
        return float(np.mean(deltas))

class DeltaPaySizeStdFeature(Feature):
    """Standard deviation of successive payload size differences."""
    name = "delta_pay_size_std"
    category = "delta"
    min_samples = 3
    min_delta_samples = 3  # Reduced from 10
    
    def extract(self, flow) -> float:
        payload_sizes = np.array([pkt.get_payloadbytes() for pkt in flow.get_packets()])
        if len(payload_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(payload_sizes))  # Use absolute differences
        return float(np.std(deltas))

class DeltaPaySizeMaxFeature(Feature):
    """Maximum of successive payload size differences."""
    name = "delta_pay_size_max"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        payload_sizes = np.array([pkt.get_payloadbytes() for pkt in flow.get_packets()])
        if len(payload_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(payload_sizes))  # Use absolute differences
        return float(np.max(deltas))

class DeltaPaySizeMinFeature(Feature):
    """Minimum of successive payload size differences."""
    name = "delta_pay_size_min"
    category = "delta"
    min_samples = 2
    min_delta_samples = 2  # Reduced from 10
    
    def extract(self, flow) -> float:
        payload_sizes = np.array([pkt.get_payloadbytes() for pkt in flow.get_packets()])
        if len(payload_sizes) < self.min_delta_samples:
            return 0.0
        deltas = np.abs(np.diff(payload_sizes))  # Use absolute differences
        return float(np.min(deltas))

class DeltaPktSizeKurtFeature(Feature):
    """Kurtosis of successive packet size differences - distribution tail measure."""
    name = "delta_pkt_size_kurt"
    category = "delta"
    min_samples = 5
    min_delta_samples = 4
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        
        deltas = np.diff(sizes)  # Don't use absolute - preserve direction
        if len(deltas) < self.min_samples:
            return 0.0
        
        # Calculate excess kurtosis
        mean = np.mean(deltas)
        std = np.std(deltas)
        
        if std == 0:
            return 0.0
        
        kurtosis = np.mean(((deltas - mean) / std) ** 4) - 3
        return float(kurtosis)

class DeltaPktSize90thPercentileFeature(Feature):
    """90th percentile of successive packet size differences."""
    name = "delta_pkt_size_90th_percentile"
    category = "delta"
    min_samples = 10
    min_delta_samples = 9
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_length() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        
        deltas = np.abs(np.diff(sizes))
        if len(deltas) < 9:
            return 0.0
        
        return float(np.percentile(deltas, 90))

class DeltaPayloadSkewFeature(Feature):
    """Skewness of successive payload size differences."""
    name = "delta_payload_skew"
    category = "delta"
    min_samples = 5
    min_delta_samples = 4
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_payloadbytes() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        
        deltas = np.diff(sizes)  # Don't use absolute - preserve direction
        if len(deltas) < self.min_samples:
            return 0.0
        
        # Calculate skewness
        mean = np.mean(deltas)
        std = np.std(deltas)
        
        if std == 0:
            return 0.0
        
        skewness = np.mean(((deltas - mean) / std) ** 3)
        return float(skewness)

class DeltaPayloadKurtFeature(Feature):
    """Kurtosis of successive payload size differences."""
    name = "delta_payload_kurt"
    category = "delta"
    min_samples = 5
    min_delta_samples = 4
    
    def extract(self, flow) -> float:
        sizes = np.array([pkt.get_payloadbytes() for pkt in flow.get_packets()])
        if len(sizes) < self.min_delta_samples:
            return 0.0
        
        deltas = np.diff(sizes)  # Don't use absolute - preserve direction
        if len(deltas) < self.min_samples:
            return 0.0
        
        # Calculate excess kurtosis
        mean = np.mean(deltas)
        std = np.std(deltas)
        
        if std == 0:
            return 0.0
        
        kurtosis = np.mean(((deltas - mean) / std) ** 4) - 3
        return float(kurtosis)
