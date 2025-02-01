from flask import Flask
from routes.users import users_bp
from routes.items import items_bp
from routes.item_requests import item_requests_bp
from routes.replacement_requests import replacement_requests_bp
from routes.plans import plans_bp


app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(items_bp)
app.register_blueprint(item_requests_bp)
app.register_blueprint(replacement_requests_bp)
app.register_blueprint(plans_bp)


@app.after_request
def add_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


app.run()