from flask import Blueprint, jsonify

financial_routes = Blueprint('financial_routes', __name__)

@financial_routes.route('/', methods=['GET'])
def index():
    return 'hello.html'

