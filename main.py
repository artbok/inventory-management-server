from flask import Flask
from routes.users import users_bp
from routes.items import items_bp
from routes.item_requests import item_requests_bp
from routes.replacement_requests import replacement_requests_bp
from routes.planings import planings_bp
from routes.reports import report_bp


app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(items_bp)
app.register_blueprint(item_requests_bp)
app.register_blueprint(replacement_requests_bp)
app.register_blueprint(planings_bp)
app.register_blueprint(report_bp)


@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

app.run()