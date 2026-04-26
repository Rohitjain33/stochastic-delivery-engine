import logging
from fastapi import FastAPI, HTTPException
from api.schemas import SimulationRequest, SimulationResponse
from simulation.models import Stage
from simulation.engine import run_simulation
from core.metrics import compute_metrics, get_risk_label
from core.logger import setup_logger

setup_logger()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Probabilistic ETA & Delivery Risk Engine",
    version="1.0.0"
)


@app.get("/")
def health():
    return {"status": "ok"}


def get_traffic_factor(level: str) -> float:
    mapping = {
        "low": 0.8,
        "normal": 1.0,
        "high": 1.5
    }
    return mapping.get(level, 1.0)


@app.post("/simulate", response_model=SimulationResponse)
def simulate(request: SimulationRequest):
    logger.info(f"Simulation requested: mode={request.mode}, runs={request.runs}, traffic={request.traffic_level}")
    try:
        # Convert request → Stage objects
        stages = [
            Stage(s.name, s.mean, s.std)
            for s in request.stages
        ]

        # Run simulation
        traffic_factor = get_traffic_factor(request.traffic_level)
        results = run_simulation(
            stages,
            request.runs,
            mode=request.mode,
            traffic_factor=traffic_factor
        )

        # Compute metrics
        metrics = compute_metrics(results, request.sla)

        # Add risk level
        metrics["risk_level"] = get_risk_label(metrics["delay_probability"])

        return metrics

    except Exception as e:
        logger.error(f"Simulation failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
