from flask import Blueprint

pay_routes = Blueprint('pay_routes', __name__)

@pay_routes.route('/')
def index():
    return "Pay Routes Page"
