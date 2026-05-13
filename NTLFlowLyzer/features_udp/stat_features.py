"""General statistics describing flow rates, sizes, and timing."""
from .base import Feature
import numpy as np

def hurst_rs(series: np.ndarray) -> float:
    """Calculate Hurst exponent using R/S analysis - Song et al. 2020."""
    if len(series) < 2:
        return 0.5  # Default to random walk
    
    # Ensure we have a numpy array
    series = np.array(series)
    n = len(series)
    
    # Calculate mean
    mean = np.mean(series)
    
    # Mean-adjusted series
    y = series - mean
    
    # Cumulative sum
    z = np.cumsum(y)
    
    # Range
    R = np.max(z) - np.min(z)
    
    # Standard deviation
    S = np.std(series, ddof=1)
    
    if S == 0:
        return 0.5
    
    # R/S statistic
    RS = R / S
    
    # Hurst exponent: H = log(R/S) / log(n/2)
    if n > 2 and RS > 0:
        H = np.log(RS) / np.log(n / 2)
        # Clamp to valid range [0, 1]
        return max(0.0, min(1.0, H))
    else:
        return 0.5

class DurationFeature(Feature):
    """Flow duration in seconds - T = t_last - t_first."""
    name = "duration"
    category = "stat"
    
    def extract(self, flow) -> float:
        return flow.get_flow_last_seen() - flow.get_flow_start_time()

class PktCountFeature(Feature):
    """Total packet count in flow."""
    name = "pkt_count"
    category = "stat"
    
    def extract(self, flow) -> int:
        return len(flow.get_packets())

class ByteCountFeature(Feature):
    """Total byte count in flow."""
    name = "byte_count"
    category = "stat"
    
    def extract(self, flow) -> int:
        return sum(packet.get_length() for packet in flow.get_packets())

class PpsFeature(Feature):
    """Packets per second - n/T."""
    name = "pps"
    category = "stat"
    
    def extract(self, flow) -> float:
        duration = flow.get_flow_last_seen() - flow.get_flow_start_time()
        if duration <= 0:
            return 0.0
        return len(flow.get_packets()) / duration

class BpsFeature(Feature):
    """Bits per second - (byte_count × 8)/T."""
    name = "bps"
    category = "stat"
    
    def extract(self, flow) -> float:
        duration = flow.get_flow_last_seen() - flow.get_flow_start_time()
        if duration <= 0:
            return 0.0
        byte_count = sum(packet.get_length() for packet in flow.get_packets())
        return (byte_count * 8) / duration

class AvgPktSizeFeature(Feature):
    """Average packet size in bytes - mean packet length."""
    name = "avg_pkt_size"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if not packets:
            return 0.0
        return sum(packet.get_length() for packet in packets) / len(packets)

class SizeVarFeature(Feature):
    """Packet size variance - σ²_s."""
    name = "size_var"
    category = "stat"
    
    def extract(self, flow) -> float:
        sizes = [packet.get_length() for packet in flow.get_packets()]
        if not sizes:
            return 0.0
        return np.var(sizes)

class MinPktFeature(Feature):
    """Minimum packet size."""
    name = "min_pkt"
    category = "stat"
    
    def extract(self, flow) -> int:
        sizes = [packet.get_length() for packet in flow.get_packets()]
        return min(sizes) if sizes else 0

class MaxPktFeature(Feature):
    """Maximum packet size."""
    name = "max_pkt"
    category = "stat"
    
    def extract(self, flow) -> int:
        sizes = [packet.get_length() for packet in flow.get_packets()]
        return max(sizes) if sizes else 0

class PktSizeSkewFeature(Feature):
    """Packet size skewness - third standardized moment."""
    name = "pkt_size_skew"
    category = "stat"
    
    def extract(self, flow) -> float:
        sizes = np.array([packet.get_length() for packet in flow.get_packets()])
        if len(sizes) < 3:
            return 0.0
        
        mean = np.mean(sizes)
        std = np.std(sizes)
        if std == 0:
            return 0.0
        
        # Skewness = E[(X - μ)³] / σ³
        return np.mean(((sizes - mean) / std) ** 3)

class PktSizeKurtFeature(Feature):
    """Packet size kurtosis - fourth standardized moment."""
    name = "pkt_size_kurt"
    category = "stat"
    
    def extract(self, flow) -> float:
        sizes = np.array([packet.get_length() for packet in flow.get_packets()])
        if len(sizes) < 4:
            return 0.0
        
        mean = np.mean(sizes)
        std = np.std(sizes)
        if std == 0:
            return 0.0
        
        # Kurtosis = E[(X - μ)⁴] / σ⁴
        return np.mean(((sizes - mean) / std) ** 4)

class TotalIatFeature(Feature):
    """Total inter-arrival time - sum of Δt between consecutive packets."""
    name = "total_iat"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0.0
        
        total_iat = 0.0
        for i in range(1, len(packets)):
            total_iat += packets[i].get_timestamp() - packets[i-1].get_timestamp()
        return total_iat

class MeanIatFeature(Feature):
    """Mean inter-arrival time."""
    name = "mean_iat"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0.0
        
        iats = []
        for i in range(1, len(packets)):
            iats.append(packets[i].get_timestamp() - packets[i-1].get_timestamp())
        
        return np.mean(iats) if iats else 0.0

class IatStdFeature(Feature):
    """Inter-arrival time standard deviation."""
    name = "iat_std"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0.0
        
        iats = []
        for i in range(1, len(packets)):
            iats.append(packets[i].get_timestamp() - packets[i-1].get_timestamp())
        
        return np.std(iats) if iats else 0.0

class IatSkewFeature(Feature):
    """Inter-arrival time skewness."""
    name = "iat_skew"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 3:
            return 0.0
        
        iats = np.array([packets[i].get_timestamp() - packets[i-1].get_timestamp() 
                        for i in range(1, len(packets))])
        
        mean = np.mean(iats)
        std = np.std(iats)
        if std == 0:
            return 0.0
        
        return np.mean(((iats - mean) / std) ** 3)

class IatKurtFeature(Feature):
    """Inter-arrival time kurtosis."""
    name = "iat_kurt"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 4:
            return 0.0
        
        iats = np.array([packets[i].get_timestamp() - packets[i-1].get_timestamp() 
                        for i in range(1, len(packets))])
        
        mean = np.mean(iats)
        std = np.std(iats)
        if std == 0:
            return 0.0
        
        return np.mean(((iats - mean) / std) ** 4)

class JitterFeature(Feature):
    """Packet jitter measurement - RMS variation of IATs, Chen et al. 2016."""
    name = "jitter"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0.0
        
        iats = [packets[i].get_timestamp() - packets[i-1].get_timestamp() 
                for i in range(1, len(packets))]
        
        if not iats:
            return 0.0
        
        mean_iat = np.mean(iats)
        # Jitter = sqrt(mean((iat - mean_iat)²))
        return np.sqrt(np.mean((np.array(iats) - mean_iat) ** 2))

class BurstCntFeature(Feature):
    """Number of packet bursts - burst defined as Δt ≤ 1 ms."""
    name = "burst_cnt"
    category = "stat"
    
    def extract(self, flow) -> int:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0
        
        burst_count = 0
        in_burst = False
        
        for i in range(1, len(packets)):
            iat = packets[i].get_timestamp() - packets[i-1].get_timestamp()
            if iat <= 0.001:  # 1 ms threshold
                if not in_burst:
                    burst_count += 1
                    in_burst = True
            else:
                in_burst = False
        
        return burst_count

class MeanBurstLenFeature(Feature):
    """Mean burst length - average packets per burst."""
    name = "mean_burst_len"
    category = "stat"
    
    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0.0
        
        burst_lengths = []
        current_burst_len = 1
        in_burst = False
        
        for i in range(1, len(packets)):
            iat = packets[i].get_timestamp() - packets[i-1].get_timestamp()
            if iat <= 0.001:  # 1 ms threshold
                if not in_burst:
                    in_burst = True
                    current_burst_len = 2  # Include previous packet
                else:
                    current_burst_len += 1
            else:
                if in_burst:
                    burst_lengths.append(current_burst_len)
                in_burst = False
                current_burst_len = 1
        
        # Don't forget the last burst if we ended in one
        if in_burst:
            burst_lengths.append(current_burst_len)
        
        return np.mean(burst_lengths) if burst_lengths else 0.0

class IdleRatioFeature(Feature):
    """Ratio of idle time to total time - time gaps > 1s divided by duration."""
    name = "idle_ratio"
    category = "stat"
    bulk_window = 1.0

    def extract(self, flow) -> float:
        packets = flow.get_packets()
        if len(packets) < 2:
            return 0.0
        
        duration = flow.get_flow_last_seen() - flow.get_flow_start_time()
        if duration <= 0:
            return 0.0
        
        idle_time = 0.0
        threshold = self.bulk_window
        for i in range(1, len(packets)):
            iat = packets[i].get_timestamp() - packets[i-1].get_timestamp()
            if iat > threshold:
                idle_time += iat
        
        return idle_time / duration

class HurstExponentFeature(Feature):
    """Hurst exponent via R/S analysis on packet sizes - Song et al. 2020."""
    name = "hurst_exponent"
    category = "stat"
    
    def extract(self, flow) -> float:
        sizes = [packet.get_length() for packet in flow.get_packets()]
        if len(sizes) < 2:
            return 0.5
        return hurst_rs(np.array(sizes))
class MedianIATFeature(Feature):
    """Median inter-arrival time."""
    name = "median_iat"
    category = "stat"
    min_samples = 2
    requires_timestamps = True

    def extract(self, flow) -> float:
        times = [p.get_timestamp() for p in flow.get_packets()]
        if len(times) < 2:
            return 0.0
        iats = np.diff(times)
        return float(np.median(iats))
