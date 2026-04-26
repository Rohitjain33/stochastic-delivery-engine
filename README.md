# Probabilistic Delivery Risk Engine

A production-grade stochastic simulation engine designed to model complex delivery estimate dynamics (ETAs). It uses advanced probabilistic modeling—including Monte Carlo simulations, Random Walk modeling, and Markov Chains—to effectively determine ETA risk under a variety of traffic configurations.

> **Mathematical Formulation**: For a deep dive into the formal formulas and mathematics powering this engine, please see [FORMULATION.md](FORMULATION.md).

## Features
- **Monte Carlo Simulations**: Evaluate base expected times, P95 timelines, and delay probabilities.
- **Random Walk Dynamics**: Account for stochastic noise and time drift across multiple operational stages (Pickup, Transit, Drop).
- **Markov Chain Sub-States**: Realistically simulate shifting delivery conditions moving dynamically between `ON_TIME`, `DELAYED`, and `SEVERE` delay states.
- **Traffic Modeling**: Extrapolate external map conditions mathematically by layering traffic-specific multipliers securely into the engine.
- **Streamlit Dashboard**: A beautiful frontend visualizing the outcome distribution geometries.
- **FastAPI Backend**: A highly performant, fully validated API architecture natively structured for production.

---

## Getting Started

This architecture gracefully relies on [Astral's `uv`](https://github.com/astral-sh/uv) to manage its dependencies aggressively. 

### Running Locally (Without Docker)

You will need two terminal tabs open for this approach.

1. **Start the API Backend**:
   ```bash
   uv run uvicorn api.main:app --reload
   ```
   *The API will run at [http://127.0.0.1:8000](http://127.0.0.1:8000). You can immediately visit the interactive Swagger Docs at `/docs`.*

2. **Start the Streamlit UI** (in a new terminal tab):
   ```bash
   uv run streamlit run ui/app.py
   ```
   *The UI will instantly open in your browser at [http://localhost:8501](http://localhost:8501).*

*(Note: In your previous terminal run, Streamlit failed to complete because the backend was likely shut down while Streamlit was looking for it! Make sure the backend terminal stays open while using Streamlit.)*

### Running Production via Docker

If you prefer deploying a containerized stack natively, simply spin it up using Docker:
```bash
docker-compose up --build
```
> Note: Make sure your Docker daemon is fully active. If your system tells you `--build` is an unknown flag while utilizing `docker compose`, you likely need to invoke the legacy V1 binary via `docker-compose`.

---

## Repository Structure

```text
├── api/             # FastAPI schemas and core endpoint routing logic
├── core/            # Centralized metrics calculations and system-wide logging
├── simulation/      # Disaggregated Monte Carlo, Random Walk, and Markov Chain models
├── ui/              # The beautifully interactive Streamlit frontend
├── Dockerfile       # Standard isolated container specification
├── docker-compose.yml 
└── pyproject.toml   # Modern Python dependency lock file natively leveraging uv
```
