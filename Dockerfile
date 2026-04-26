FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install uv for fast dependency resolution and installation
RUN pip install --no-cache-dir uv

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install project dependencies using uv
RUN uv sync --frozen

# Copy the rest of the application files
COPY . .

# Expose the port Uvicorn runs on
EXPOSE 8000

# Command to run the Fast API server
CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
