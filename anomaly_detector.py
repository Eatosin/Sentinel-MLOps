
import numpy as np
from collections import deque
import logging

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    Real-time statistical anomaly detection using rolling Z-Score analysis.
    Designed to detect data drift in time-series metrics.
    """
    def __init__(self, window_size=20, threshold=2.5):
        self.window_size = window_size
        self.threshold = threshold
        self.data_window = deque(maxlen=window_size)

    def update(self, value):
        """
        Ingest new data point and calculate deviation.
        Returns: (is_anomaly, message, z_score)
        """
        self.data_window.append(value)
        
        if len(self.data_window) < 5:
            return False, "Initializing baseline...", 0.0

        mean = np.mean(self.data_window)
        std_dev = np.std(self.data_window)

        if std_dev == 0:
            return False, "Stable", 0.0

        z_score = (value - mean) / std_dev

        if abs(z_score) > self.threshold:
            logger.warning(f"Anomaly Detected: Value {value} | Deviation {z_score:.2f}")
            return True, f"CRITICAL: Deviation {z_score:.2f} sigma", z_score
        
        return False, "Normal", z_score
