# app.py
from flask import Flask
from payslipify.backend.app.routes.financial_data_routes import fin_routes
from payslipify.backend.app.routes.financial_insight_routes import pay_routes
from payslipify.backend.app.routes.take_home_pay_routes import income_routes

app = Flask(__name__)

# Correctly register the blueprints
app.register_blueprint(fin_routes, url_prefix='/finance')
app.register_blueprint(pay_routes, url_prefix='/pay')
app.register_blueprint(income_routes, url_prefix='/income')

if __name__ == '__main__':
    app.run(debug=True)
