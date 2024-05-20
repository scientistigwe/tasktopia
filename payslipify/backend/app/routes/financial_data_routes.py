# fin_routes.py
from flask import Blueprint

fin_routes = Blueprint('fin_routes', __name__)

@fin_routes.route('/')
def index():
    return "Financial Routes Page"
