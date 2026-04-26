import numpy as np
from typing import List
from simulation.models import Stage
from simulation.states import next_state

def simulate_delivery(stages: List[Stage], traffic_factor: float = 1.0) -> float:
    total_time = 0.0

    for stage in stages:
        total_time += stage.sample(traffic_factor)

    return total_time


def random_walk_delivery(stages: List[Stage]) -> float:
    """
    Simulate delivery using Random Walk with drift
    """
    total_time = 0.0

    for stage in stages:
        # drift = expected time
        drift = stage.mean
        
        # noise = randomness
        noise = np.random.normal(0, stage.std)

        total_time += drift + noise

    return max(total_time, 0)


def random_walk_with_state(stages: List[Stage]) -> float:
    total_time = 0.0
    state = "ON_TIME"

    for stage in stages:
        state = next_state(state)

        delay_multiplier = {
            "ON_TIME": 1.0,
            "DELAYED": 1.3,
            "SEVERE": 1.8
        }[state]

        noise = np.random.normal(0, stage.std)
        total_time += (stage.mean * delay_multiplier) + noise

    return max(total_time, 0)


def run_simulation(stages: List[Stage], num_runs: int = 10000, mode: str = "independent", traffic_factor: float = 1.0) -> list:
    results = []

    for _ in range(num_runs):
        if mode == "random_walk":
            total_time = random_walk_delivery(stages)
        elif mode == "markov":
            total_time = random_walk_with_state(stages)
        else:
            total_time = simulate_delivery(stages, traffic_factor)

        results.append(total_time)

    return results
