from flask import Flask
from config import Config
from extensions import limiter
from controllers.main_controller import main
from controllers.api_controller import api


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    limiter.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(api)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)