from backend.app.atlas_app import create_app
import os

backend = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    backend.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
