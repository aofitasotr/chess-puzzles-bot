import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    app = create_app()
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host=host, port=port, debug=True)
