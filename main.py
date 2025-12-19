from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import logging

# Import our custom modules
from anomaly_detector import AnomalyDetector
from rag_agent import SentinelAgent

# 1. Initialize the App
app = FastAPI(
    title="Sentinel MLOps Agent",
    description="Autonomous Anomaly Detection & RAG Investigation API",
    version="1.0"
)

# 2. Load the Engines
print("🔋 Starting Sentinel Engines...")
detector = AnomalyDetector()
agent = SentinelAgent()

# 3. Define the Data Format (Validation)
class MetricData(BaseModel):
    timestamp: str
    service_name: str
    cpu_usage: float

# 4. The API Endpoint
@app.post("/monitor")
async def monitor_system(data: MetricData):
    """
    Receives live system data.
    - If Normal: Returns OK.
    - If Anomaly: Triggers Gemini 2.5 to investigate.
    """
    # Step A: Check for Physics/Math Anomaly
    is_anomaly, msg, z_score = detector.update(data.cpu_usage)
    
    if not is_anomaly:
        return {
            "status": "Healthy", 
            "message": msg, 
            "z_score": z_score
        }
    
    # Step B: If Anomaly, Wake up the Agent
    print(f"🚨 ALERT: Anomaly on {data.service_name} detected!")
    
    report = agent.investigate(
        anomaly_value=data.cpu_usage, 
        z_score=z_score
    )
    
    # Return the Full Incident Report
    return {
        "status": "CRITICAL",
        "service": data.service_name,
        "deviation": f"{z_score:.2f} sigma",
        "investigation_report": report
    }

@app.get("/")
def home():
    return {"message": "Sentinel AI Agent is Active. Send POST to /monitor"}

# 5. Run the Server (Mobile Friendly)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)