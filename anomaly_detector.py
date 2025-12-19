import numpy as np
from collections import deque

class AnomalyDetector:
    def __init__(self, window_size=20, threshold=2.5):
        """
        Physics-based Anomaly Detection.
        We keep a 'window' of recent data to establish a baseline.
        If a new data point deviates by > 2.5 Standard Deviations (Z-Score),
        we flag it as an anomaly.
        
        :param window_size: How many recent data points to remember.
        :param threshold: The Z-Score limit (Physics standard is usually 3-sigma, we use 2.5).
        """
        self.window_size = window_size
        self.threshold = threshold
        # A deque is like a list that automatically drops old data when full
        self.data_window = deque(maxlen=window_size)

    def update(self, value):
        """
        Ingest new data, update statistics, and check for drift.
        Returns: (is_anomaly, message, current_z_score)
        """
        # 1. Add new value to history
        self.data_window.append(value)
        
        # 2. Need enough data to establish a baseline (at least 5 points)
        if len(self.data_window) < 5:
            return False, "Initializing baseline...", 0.0

        # 3. Calculate Physics Metrics (Mean & Standard Deviation)
        mean = np.mean(self.data_window)
        std_dev = np.std(self.data_window)

        # Avoid division by zero if flatline
        if std_dev == 0:
            return False, "Stable", 0.0

        # 4. Calculate Z-Score (How far is this point from the 'Normal'?)
        z_score = (value - mean) / std_dev

        # 5. Check Threshold
        if abs(z_score) > self.threshold:
            return True, f"CRITICAL: Anomaly Detected! Value {value} is {z_score:.2f}σ deviation.", z_score
        
        return False, "Normal", z_score

# --- Quick Test Block (Runs only if you play this file directly) ---
if __name__ == "__main__":
    print("🔬 Initializing Sentinel Detector...")
    detector = AnomalyDetector()
    
    # 1. Simulate Normal Traffic (Values around 50)
    normal_data = [50, 52, 49, 51, 50, 48, 53, 50, 51, 49]
    for val in normal_data:
        detector.update(val)
        print(f"Input: {val} | Status: OK")

    # 2. Simulate a SUDDEN SPIKE (Anomaly)
    spike = 120 # Massive jump
    is_anomaly, msg, z = detector.update(spike)
    print(f"\n⚠️ Input: {spike} | {msg}")