import os
from src.web.app import create_app

if __name__ == '__main__':
    # Create required directories
    os.makedirs('src/static/uploads', exist_ok=True)
    
    # Create and run application
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)