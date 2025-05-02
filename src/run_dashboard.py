import os
import subprocess
import sys

def main():
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Run the dashboard
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard.py"])
    except KeyboardInterrupt:
        print("\nDashboard stopped by user")
    except Exception as e:
        print(f"Error running dashboard: {str(e)}")

if __name__ == "__main__":
    main() 