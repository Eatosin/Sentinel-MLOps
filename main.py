from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
import uvicorn
import logging
import os

from anomaly_detector import AnomalyDetector
from rag_agent import SentinelAgent

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SentinelAPI")

app = FastAPI(
    title="Sentinel MLOps Agent",
    description="Autonomous Anomaly Detection & Incident Response API.",
    version="1.0.0"
)

# Initialize Services
try:
    detector = AnomalyDetector()
    agent = SentinelAgent()
    logger.info("Sentinel Engines Initialized.")
except Exception as e:
    logger.critical(f"Startup Failure: {e}")

class MetricData(BaseModel):
    timestamp: str
    service_name: str
    cpu_usage: float

@app.post("/monitor")
async def monitor_system(data: MetricData):
    # 1. Physics Check
    is_anomaly, msg, z_score = detector.update(data.cpu_usage)
    
    if not is_anomaly:
        return {
            "status": "Healthy", 
            "message": msg, 
            "z_score": z_score
        }
    
    # 2. Agent Investigation
    logger.warning(f"Critical Alert on {data.service_name}")
    report = agent.investigate(data.cpu_usage, z_score)
    
    return {
        "status": "CRITICAL",
        "service": data.service_name,
        "deviation": f"{z_score:.2f} sigma",
        "incident_report": report
    }

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
