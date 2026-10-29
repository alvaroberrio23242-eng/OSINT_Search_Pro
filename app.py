import os

from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config
from extensions import limiter
from controllers.main_controller import main
from controllers.api_controller import api

# En modo "report-only" no bloquea nada: revisa la consola del navegador antes de hacerla obligatoria.
_CSP_REPORT_ONLY = (
    "default-src 'self'; "
    "script-src 'self'; "
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
    "font-src 'self' https://fonts.gstatic.com; "
    "img-src 'self' data: https://api.qrserver.com; "
    "connect-src 'self'; "
    "frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["MAX_CONTENT_LENGTH"] = 256 * 1024

    # Detras de Render hay un proxy: sin ProxyFix todos los visitantes compartirian la misma IP en el limitador.
    saltos = 0 if os.environ.get("OSP_DEV") == "1" else int(os.environ.get("OSP_PROXY_HOPS", 1))
    if saltos:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=saltos, x_proto=saltos)

    limiter.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(api)

    @app.after_request
    def cabeceras_seguridad(resp):
        resp.headers.setdefault("X-Content-Type-Options", "nosniff")
        resp.headers.setdefault("X-Frame-Options", "DENY")
        resp.headers.setdefault("Referrer-Policy", "no-referrer")
        resp.headers.setdefault("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        resp.headers.setdefault("Content-Security-Policy-Report-Only", _CSP_REPORT_ONLY)
        if request.is_secure:
            resp.headers.setdefault("Strict-Transport-Security", "max-age=31536000")
        return resp

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=os.environ.get("OSP_DEV") == "1")
