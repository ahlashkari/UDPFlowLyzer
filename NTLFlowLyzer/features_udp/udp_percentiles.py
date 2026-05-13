"""Percentile-based statistical features for packet sizes and timing."""
from .base import Feature
import numpy as np

class PacketSize25thPercentileFeature(Feature):
    """25th percentile of packet sizes."""
    name = "pkt_size_25th_percentile"
    category = "stat"
    min_samples = 4
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_length() for pkt in packets])
        return float(np.percentile(sizes, 25))

class PacketSize75thPercentileFeature(Feature):
    """75th percentile of packet sizes."""
    name = "pkt_size_75th_percentile"
    category = "stat"
    min_samples = 4
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_length() for pkt in packets])
        return float(np.percentile(sizes, 75))

class PacketSize90thPercentileFeature(Feature):
    """90th percentile of packet sizes."""
    name = "pkt_size_90th_percentile"
    category = "stat"
    min_samples = 10
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_length() for pkt in packets])
        return float(np.percentile(sizes, 90))

class IAT25thPercentileFeature(Feature):
    """25th percentile of inter-arrival times."""
    name = "iat_25th_percentile"
    category = "timing"
    min_samples = 5
    requires_timestamps = True
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        timestamps = np.array([pkt.get_timestamp() for pkt in packets])
        iats = np.diff(timestamps)
        
        if len(iats) < 4:
            return 0.0
        
        return float(np.percentile(iats, 25))

class IAT75thPercentileFeature(Feature):
    """75th percentile of inter-arrival times."""
    name = "iat_75th_percentile"
    category = "timing"
    min_samples = 5
    requires_timestamps = True
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        timestamps = np.array([pkt.get_timestamp() for pkt in packets])
        iats = np.diff(timestamps)
        
        if len(iats) < 4:
            return 0.0
        
        return float(np.percentile(iats, 75))

class IAT90thPercentileFeature(Feature):
    """90th percentile of inter-arrival times."""
    name = "iat_90th_percentile"
    category = "timing"
    min_samples = 10
    requires_timestamps = True
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        timestamps = np.array([pkt.get_timestamp() for pkt in packets])
        iats = np.diff(timestamps)
        
        if len(iats) < 9:
            return 0.0
        
        return float(np.percentile(iats, 90))

class PacketSizeRangeFeature(Feature):
    """Range of packet sizes (max - min)."""
    name = "pkt_size_range"
    category = "stat"
    min_samples = 2
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_length() for pkt in packets])
        return float(np.max(sizes) - np.min(sizes))

class IATRangeFeature(Feature):
    """Range of inter-arrival times (max - min)."""
    name = "iat_range"
    category = "timing"
    min_samples = 3
    requires_timestamps = True
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        timestamps = np.array([pkt.get_timestamp() for pkt in packets])
        iats = np.diff(timestamps)
        
        if len(iats) < 2:
            return 0.0
        
        return float(np.max(iats) - np.min(iats)) 

class PacketSizeIQRFeature(Feature):
    """Interquartile range of packet sizes (75th - 25th percentile)."""
    name = "pkt_size_iqr"
    category = "stat"
    min_samples = 4
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_length() for pkt in packets])
        q75 = np.percentile(sizes, 75)
        q25 = np.percentile(sizes, 25)
        return float(q75 - q25)

class IATIQRFeature(Feature):
    """Interquartile range of inter-arrival times."""
    name = "iat_iqr"
    category = "timing"
    min_samples = 5
    requires_timestamps = True
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        timestamps = np.array([pkt.get_timestamp() for pkt in packets])
        iats = np.diff(timestamps)
        
        if len(iats) < 4:
            return 0.0
        
        q75 = np.percentile(iats, 75)
        q25 = np.percentile(iats, 25)
        return float(q75 - q25)

class PayloadSize25thPercentileFeature(Feature):
    """25th percentile of payload sizes."""
    name = "payload_size_25th_percentile"
    category = "stat"
    min_samples = 4
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_payloadbytes() for pkt in packets])
        return float(np.percentile(sizes, 25))

class PayloadSize75thPercentileFeature(Feature):
    """75th percentile of payload sizes."""
    name = "payload_size_75th_percentile"
    category = "stat"
    min_samples = 4
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_payloadbytes() for pkt in packets])
        return float(np.percentile(sizes, 75))

class PayloadSizeMedianFeature(Feature):
    """Median payload size."""
    name = "payload_size_median"
    category = "stat"
    min_samples = 1
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if not packets:
            return 0.0
        
        sizes = np.array([pkt.get_payloadbytes() for pkt in packets])
        return float(np.median(sizes))

class HeaderSizeMedianFeature(Feature):
    """Median header size."""
    name = "header_size_median"
    category = "stat"
    min_samples = 1
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if not packets:
            return 0.0
        
        sizes = np.array([pkt.get_header_size() for pkt in packets])
        return float(np.median(sizes))

class PacketSizeMADFeature(Feature):
    """Median Absolute Deviation of packet sizes - robust measure."""
    name = "pkt_size_mad"
    category = "stat"
    min_samples = 2
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < self.min_samples:
            return 0.0
        
        sizes = np.array([pkt.get_length() for pkt in packets])
        median_size = np.median(sizes)
        mad = np.median(np.abs(sizes - median_size))
        return float(mad) 