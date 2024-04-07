# atlas_app.py
from app import create_app  # Adjust the import according to your actual package structure
import os

backend = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    backend.run(host='0.0.0.0', port=port, debug=False)
