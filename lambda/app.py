import os
import time
import sqlite3

from flask import Flask, g, render_template

# App is mounted at /unfriended-flask on the main site
APP_PREFIX = os.environ.get("APP_PREFIX", "/unfriended-flask")
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.db")

app = Flask(__name__, static_url_path=f"{APP_PREFIX}/static")


def get_db():
    """Open a read-only SQLite connection."""
    if "db" not in g:
        g.db = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.before_request
def before_request():
    g.request_start_time = time.time()
    g.request_time = lambda: "%.5fs" % (time.time() - g.request_start_time)


@app.route(f"{APP_PREFIX}/")
def index():
    db = get_db()

    # Get users who have names stored
    users = db.execute(
        "SELECT u.id, u.name, u.fbId, "
        "(SELECT COUNT(*) FROM friends f WHERE f.userFbId = u.fbId) AS friend_count "
        "FROM users u ORDER BY u.name"
    ).fetchall()

    # Get stats for all tracked friend lists (including unnamed users)
    total_users = db.execute(
        "SELECT COUNT(DISTINCT userFbId) FROM friends"
    ).fetchone()[0]

    total_records = db.execute("SELECT COUNT(*) FROM friends").fetchone()[0]

    return render_template(
        "index.html",
        users=users,
        total_users=total_users,
        total_records=total_records,
    )


# Health check (useful for Lambda warm-up)
@app.route(f"{APP_PREFIX}/health")
def health():
    return '{"status": "ok"}', 200, {"Content-Type": "application/json"}
