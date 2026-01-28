import uvicorn
import os
import sys

# Ensure src is in path
sys.path.append(os.getcwd())

if __name__ == "__main__":
    print("Starting Unified Metrics Platform Server...")
    print("Dashboard available at: http://localhost:8000")
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
