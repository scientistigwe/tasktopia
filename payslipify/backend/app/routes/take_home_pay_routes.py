# fin_routes.py
from flask import Blueprint

income_routes = Blueprint('income_routes', __name__)

@income_routes.route('/')
def index():
    return "Income Routes Page"
