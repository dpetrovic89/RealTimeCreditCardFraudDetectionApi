FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for LightGBM
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure model is available or provide a placeholder
# In production, we'd download from MLflow registry
# Hugging Face default port is 7860
EXPOSE 7860

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "7860"]
