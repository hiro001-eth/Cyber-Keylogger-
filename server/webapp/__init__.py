from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'  # use env var in prod

    from .routes import webapp_routes
    app.register_blueprint(webapp_routes)

    return app 