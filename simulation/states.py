import random

states = ["ON_TIME", "DELAYED", "SEVERE"]

transition_matrix = {
    "ON_TIME": {"ON_TIME": 0.7, "DELAYED": 0.25, "SEVERE": 0.05},
    "DELAYED": {"ON_TIME": 0.2, "DELAYED": 0.6, "SEVERE": 0.2},
    "SEVERE": {"ON_TIME": 0.1, "DELAYED": 0.3, "SEVERE": 0.6},
}


def next_state(current):
    probs = transition_matrix[current]
    return random.choices(list(probs.keys()), weights=probs.values())[0]
