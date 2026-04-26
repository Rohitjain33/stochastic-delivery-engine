import numpy as np

class Stage:
    def __init__(self, name: str, mean: float, std: float):
        self.name = name
        self.mean = mean
        self.std = std

    def sample(self, traffic_factor: float = 1.0) -> float:
        adjusted_mean = self.mean * traffic_factor
        value = np.random.normal(adjusted_mean, self.std)
        return max(value, 0)
