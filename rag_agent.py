import os
import google.generativeai as genai
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)

# --- CONFIGURATION ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    logger.error("GEMINI_API_KEY not found. Agent functionality disabled.")

# Initialize Model
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')

class SentinelAgent:
    """
    Autonomous Agent that performs Root Cause Analysis (RCA) on system logs using RAG.
    """
    def __init__(self):
        # Simulated Vector Database
        self.system_logs = {
            "CPU_SPIKE": "Log 10:42am - Process 'minerd' started using 99% CPU. Unknown user 'xmr_bot'.",
            "MEMORY_LEAK": "Log 10:45am - OutOfMemoryError: Java Heap Space. Service 'PaymentGateway' crashed.",
            "NETWORK_LAG": "Log 10:50am - DDOS detected from IP Block 192.168.x.x. Latency increased to 5000ms."
        }

    def investigate(self, anomaly_value, z_score):
        """
        Retrieves context and generates an incident report.
        """
        logger.info(f"Agent triggered. Analyzing Anomaly: {anomaly_value} (Z={z_score:.2f})")
        
        # Retrieval Logic (Heuristic for demo)
        if anomaly_value > 100:
            context = self.system_logs["CPU_SPIKE"]
        elif anomaly_value > 80:
            context = self.system_logs["MEMORY_LEAK"]
        else:
            context = self.system_logs["NETWORK_LAG"]

        prompt = f"""
        ROLE: Autonomous MLOps Engineer.
        
        ALERT:
        - Metric Value: {anomaly_value}
        - Statistical Deviation: {z_score:.2f} sigma
        
        LOG CONTEXT:
        "{context}"
        
        TASK:
        1. Identify Root Cause.
        2. Recommend Immediate Mitigation.
        3. Keep output technical and concise.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Inference Failed: {e}")
            return "Analysis Unavailable."
