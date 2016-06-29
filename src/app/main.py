from .urls import URLS
from app import init_app


def start_app(config):
    """
    Initialize an app
    """
    config['URLS'] = URLS
    app = init_app(**config)

    # Development server will run just in DEBUG mode
    if app.config['DEBUG']:
        app.run(
            host=app.config['HOST'], port=app.config['PORT'])
