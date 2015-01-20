from flask import Flask
from flask_bootstrap import Bootstrap
from config import APP_SECRET, SQLALCHEMY_DATABASE_URI
from database import init_db

from unfriended.unfriended import unfriended
from facebook.facebook import facebook


BLUEPRINT_MODULES = [facebook,
                     unfriended]

app = Flask(__name__)
app.secret_key = APP_SECRET
init_db(app)
Bootstrap(app)

for module in BLUEPRINT_MODULES:
    app.register_blueprint(module)


if __name__ == '__main__':
    app.run(debug=True)
