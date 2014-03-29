from flask import Flask
from config import APP_SECRET

from routes.home import home
from facebook.facebook import facebook

BLUEPRINT_MODULES = [
        home,
        facebook
        ]

app = Flask(__name__)
app.secret_key = APP_SECRET

for module in BLUEPRINT_MODULES:
    app.register_blueprint(module)

if __name__ == '__main__':
    app.run(debug=True)