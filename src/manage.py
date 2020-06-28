from src.app import create_app
from src.settings import DevConfig

app = create_app(config_object=DevConfig)

if __name__ == '__main__':
    """Main Application
    python manage.py
    """
    app.run(host='127.0.0.1', port=5000, threaded=True, use_reloader=True)

