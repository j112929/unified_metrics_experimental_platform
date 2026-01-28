import numpy as np
from typing import List, Optional, Tuple
from abc import ABC, abstractmethod

class AnomalyResult:
    def __init__(self, is_anomaly: bool, score: float, expected_range: Tuple[float, float]):
        self.is_anomaly = is_anomaly
        self.score = score
        self.expected_range = expected_range

class BaseDetector(ABC):
    @abstractmethod
    def fit(self, data: List[float]):
        pass

    @abstractmethod
    def predict(self, value: float) -> AnomalyResult:
        pass

class ZScoreDetector(BaseDetector):
    def __init__(self, threshold: float = 3.0):
        self.threshold = threshold
        self.mean = 0.0
        self.std = 1.0
        self.initialized = False

    def fit(self, data: List[float]):
        if not data:
            return
        self.mean = np.mean(data)
        self.std = np.std(data)
        # Avoid division by zero
        if self.std == 0:
            self.std = 1e-6
        self.initialized = True

    def predict(self, value: float) -> AnomalyResult:
        if not self.initialized:
            return AnomalyResult(False, 0.0, (0.0, 0.0))
        
        z_score = (value - self.mean) / self.std
        is_anomaly = abs(z_score) > self.threshold
        
        lower_bound = self.mean - (self.threshold * self.std)
        upper_bound = self.mean + (self.threshold * self.std)
        
        return AnomalyResult(
            is_anomaly=is_anomaly,
            score=z_score,
            expected_range=(lower_bound, upper_bound)
        )
