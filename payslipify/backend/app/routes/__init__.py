# backend/app/__init__.py

from flask import Flask
from app.routes.financial_data_routes import router as financial_data_router

def create_app():
    app = Flask(__name__)

    # Register your blueprint/routes here
    app.register_blueprint(financial_data_router)

    return app
