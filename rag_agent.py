import os
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

# --- 1. ROBUST KEY LOADING (The Fix) ---
# Get the folder where THIS script is located
current_folder = Path(__file__).parent
env_path = current_folder / ".env"

print(f"🔍 Looking for .env at: {env_path}")

# Force load that specific file
load_dotenv(dotenv_path=env_path)
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ CRITICAL ERROR: API Key still not found.")
    print("   Please check that the file is named exactly '.env' (with the dot).")
    print("   And that inside it says: GEMINI_API_KEY=your_key_here")
    exit() # Stop here if no key
else:
    print("✅ API Key successfully loaded!")
    genai.configure(api_key=api_key)

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