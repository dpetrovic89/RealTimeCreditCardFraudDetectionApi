# FraudShield AI: Real-Time Credit Card Fraud Detection 🚀

[![Fraud Detection CI/CD](https://github.com/dpetrovic89/RealTimeCreditCardFraudDetectionApi/actions/workflows/main.yml/badge.svg)](https://github.com/dpetrovic89/RealTimeCreditCardFraudDetectionApi/actions)

FraudShield AI is a production-ready MLOps ecosystem designed to detect fraudulent credit card transactions in real-time. Built with a 100% free-tier stack, this project demonstrates senior-level engineering across the entire data-to-deployment lifecycle.

## 🏗️ Architecture Stack

- **Model**: LightGBM (89% Recall on real Kaggle data)
- **Serving**: FastAPI + Uvicorn
- **Frontend**: Premium Glassmorphic UI (Vanilla JS/CSS)
- **Data Foundation**: DVC (Data Version Control) + Great Expectations (Validation)
- **MLOps**: MLflow + DagsHub (Experiment Tracking)
- **Infrastructure**: Docker + Kubernetes (Minikube)
- **CI/CD**: GitHub Actions
- **Monitoring**: Evidently AI (Drift Detection) + Prometheus (Metrics)

---

## 🚀 Step-by-Step Deployment Guide

Follow these steps to get the full stack running on your machine.

### 1. Prerequisites
Ensure you have the following installed:
- Python 3.10+
- Docker Desktop
- Minikube (for Kubernetes deployment)
- Git

### 2. Local Setup
```bash
# Clone the repository
git clone https://github.com/dpetrovic89/RealTimeCreditCardFraudDetectionApi.git
cd RealTimeCreditCardFraudDetectionApi

# Install dependencies
pip install -r requirements.txt
```

### 3. Run with Python (Development)
```bash
# Start the FastAPI server
uvicorn src.app:app --host 0.0.0.0 --port 8001 --reload
```
Access the frontend by opening `frontend/index.html` in your browser.

### 4. Run with Docker
```bash
# Build the image
docker build -t fraud-detection-api .

# Run the container
docker run -p 8001:8000 fraud-detection-api
```

### 5. Deploy to Kubernetes (Minikube)
```bash
# Start Minikube
minikube start

# Apply manifests
kubectl apply -f k8s/deployment.yaml

# Expose the service
minikube service fraud-detection-service
```

### 6. Deploy to Vercel (Fastest & Free)
This app is optimized for Vercel Serverless Functions.
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` in the root directory.
3. Your frontend will be at `https://your-project.vercel.app` and API at `/api/predict`.

### 7. Activate CI/CD
To enable automated builds and tests:
1. Go to your GitHub Repo > **Settings** > **Secrets and variables** > **Actions**.
2. Add the following secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username.
   - `DOCKERHUB_TOKEN`: Your Docker Hub Access Token.
3. Every push to `main` will now trigger a build and push to Docker Hub!

---

## 📊 Monitoring & Data Quality
- **Validation**: Run `python scripts/data_validation.py` to check data health via Great Expectations.
- **Drift**: Run `python src/monitor.py` to generate an Evidently AI report (`monitoring/drift_report.html`).
- **Metrics**: Prometheus scrapes API performance data on port 8001.

## 📄 License
This project uses the Kaggle Credit Card Fraud Detection dataset. Distributed under the MIT License.
