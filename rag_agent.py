import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- CLOUD-READY KEY LOADING ---
# 1. Try to load from environment (Cloud/Render)
api_key = os.getenv("GEMINI_API_KEY")

# 2. If not found, try loading from local .env file (Phone/Local)
if not api_key:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # If still missing, we don't crash, we just warn (so the app can at least start)
    print("⚠️ Warning: GEMINI_API_KEY not found. Agent will rely on environment variables.")
else:
    genai.configure(api_key=api_key)

# --- MODEL CONFIGURATION ---
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
except:
    model = genai.GenerativeModel('gemini-pro')
    
# ... (Rest of the code remains the same: class SentinelAgent...)

# --- 2. MODEL CONFIGURATION (Direct) ---
# We use the specific model you confirmed you have.
print("📡 Connecting to Gemini 2.5 Flash...")
model = genai.GenerativeModel('gemini-2.5-flash')

class SentinelAgent:
    def __init__(self):
        self.system_logs = {
            "CPU_SPIKE": "Log 10:42am - Process 'minerd' started using 99% CPU. Unknown user 'xmr_bot'.",
            "MEMORY_LEAK": "Log 10:45am - OutOfMemoryError: Java Heap Space. Service 'PaymentGateway' crashed.",
            "NETWORK_LAG": "Log 10:50am - DDOS detected from IP Block 192.168.x.x. Latency increased to 5000ms."
        }

    def investigate(self, anomaly_value, z_score):
        print("🤖 Sentinel Agent analyzing logs...")
        
        if anomaly_value > 100:
            context = self.system_logs["CPU_SPIKE"]
        elif anomaly_value > 80:
            context = self.system_logs["MEMORY_LEAK"]
        else:
            context = self.system_logs["NETWORK_LAG"]

        prompt = f"""
        You are Sentinel, an Autonomous MLOps Agent.
        
        **ALERT:** Anomaly Detected!
        - Metric Value: {anomaly_value}
        - Deviation: {z_score:.2f} sigma
        
        **RETRIEVED LOGS:**
        "{context}"
        
        **TASK:**
        Identify the root cause and recommend a fix. Short and technical.
        """
        
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Model Error: {str(e)}"

if __name__ == "__main__":
    agent = SentinelAgent()
    print("🔥 Simulation: Testing Agent...")
    report = agent.investigate(120, 4.5)
    print("\n--- 📄 REPORT ---")
    print(report)
