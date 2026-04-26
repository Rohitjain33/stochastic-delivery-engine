import numpy as np

def run_simulation(num_iterations: int = 1000):
    """
    Run a Monte Carlo simulation.
    """
    results = np.random.normal(loc=10, scale=2, size=num_iterations)
    return {"mean": float(np.mean(results)), "std_dev": float(np.std(results))}
