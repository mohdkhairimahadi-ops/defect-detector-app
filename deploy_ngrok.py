# deploy_ngrok.py
from pyngrok import ngrok
import subprocess
import time
import threading

# Your Ngrok authtoken (replace with yours)
NGROK_TOKEN = "y352d7PJPKXaxYD5A45LrGDUhy6E_3VzbwRLQ5P6Kr3hHWTLfv"  # From ngrok.com dashboard

def run_streamlit():
    """Run Streamlit in background."""
    subprocess.Popen([
        "streamlit", "run", "app.py",
        "--server.port", "8501",
        "--server.headless", "true",  # No browser auto-open
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ])

if __name__ == "__main__":
    # Set Ngrok auth
    ngrok.set_auth_token(NGROK_TOKEN)
    
    # Start Streamlit in thread
    streamlit_thread = threading.Thread(target=run_streamlit)
    streamlit_thread.daemon = True
    streamlit_thread.start()
    
    # Wait for Streamlit to start (5-10 sec)
    time.sleep(10)
    
    # Create tunnel to port 8501
    public_url = ngrok.connect(8501, "http")
    print(f"🚀 Your app is live at: {public_url}")
    print("Press Ctrl+C to stop.")
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok.disconnect(public_url)
        print("Tunnel closed.")