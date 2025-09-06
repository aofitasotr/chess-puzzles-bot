import os
from app import create_app
from app.logger import log_info, log_error
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    try:
        app = create_app()
        host = os.getenv("FLASK_HOST", "0.0.0.0")
        port = int(os.getenv("FLASK_PORT", 5000))
        
        log_info(f"Starting Flask application on {host}:{port}")
        app.run(host=host, port=port, debug=True)
    except Exception as e:
        log_error(f"Failed to start application: {e}")
        raise
