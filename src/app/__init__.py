from flask import Flask


# Alex Martelli's 'Borg'
class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class App(Borg):
    """
    Singleton class that shares app properties accross
    all components in the application
    """
    def __init__(self, **config):
        Borg.__init__(self)
        self.app = Flask(__name__)

    def init_config(self, **config):
        for k, v in config.items():
            self.app.config[k] = v
        # secret encryption key
        if 'SECRET_KEY' in config:
            app.secret_key = config['SECRET_KEY']

    def init_urls(self):
        # Reads urls definition from URLs file and bind routes and views
        if 'URLS' in self.app.config:
            for route in self.app.config['URLS']:
                self.app.add_url_rule(
                    route[0], view_func=route[1].as_view(route[2]))


app = App()


def init_app(**config):
    """
    Initalize an app, call this method once from start_app
    """
    app.init_config(**config)
    app.init_urls()
    return app.app


def get_app():
    """
    Get current app, call this method  from anywhere inside the application
    """
    return app.app
