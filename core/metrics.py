import numpy as np


def compute_metrics(results: list, sla: float) -> dict:
    results = np.array(results)

    expected_time = float(np.mean(results))
    p95_time = float(np.percentile(results, 95))
    delay_probability = float(np.mean(results > sla))

    return {
        "expected_time": round(expected_time, 2),
        "p95_time": round(p95_time, 2),
        "delay_probability": round(delay_probability, 4),
    }


def get_risk_label(delay_prob: float) -> str:
    if delay_prob > 0.5:
        return "HIGH"
    elif delay_prob > 0.2:
        return "MEDIUM"
    return "LOW"
