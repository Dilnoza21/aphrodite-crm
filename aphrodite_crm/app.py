"""
app.py — Aphrodite Dress CRM backend (Flask + SQLite).
Run:  python seed_db.py   (once, to build the database)
      python app.py        (starts the server at http://localhost:5000)
Login:  username = admin   password = admin1234
"""
import sqlite3, hashlib, os, datetime, random
from functools import wraps
from flask import Flask, jsonify, request, session, send_from_directory, redirect

app = Flask(__name__, static_folder="static")
app.secret_key = "aphrodite-dress-secret-key-change-in-production"
DB = os.path.join(os.path.dirname(__file__), "aphrodite.db")


def db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def rows(q, args=()):
    conn = db()
    data = [dict(r) for r in conn.execute(q, args).fetchall()]
    conn.close()
    return data


def one(q, args=()):
    conn = db()
    r = conn.execute(q, args).fetchone()
    conn.close()
    return dict(r) if r else None


def login_required(f):
    @wraps(f)
    def wrap(*a, **k):
        if not session.get("user"):
            return jsonify({"error": "unauthorized"}), 401
        return f(*a, **k)
    return wrap


# ---------------- pages ----------------
@app.route("/")
def landing():
    return send_from_directory(".", "index.html")


@app.route("/dashboard")
def dashboard():
    return send_from_directory(".", "dashboard.html")


# ---------------- auth ----------------
@app.route("/api/login", methods=["POST"])
def api_login():
    d = request.get_json(force=True)
    u = one("SELECT * FROM users WHERE username=?", (d.get("username", "").strip(),))
    if u and u["password"] == hashlib.sha256(d.get("password", "").encode()).hexdigest():
        session["user"] = u["username"]
        return jsonify({"ok": True, "name": u["name"], "role": u["role"]})
    return jsonify({"ok": False, "error": "Invalid username or password"}), 401


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.clear()
    return jsonify({"ok": True})


@app.route("/api/me")
def api_me():
    if session.get("user"):
        u = one("SELECT name, role FROM users WHERE username=?", (session["user"],))
        return jsonify({"auth": True, **u})
    return jsonify({"auth": False})


# ---------------- dashboard stats ----------------
@app.route("/api/dashboard")
@login_required
def api_dashboard():
    revenue = one("SELECT COALESCE(SUM(total),0) v FROM orders WHERE status!='Cancelled'")["v"]
    orders = one("SELECT COUNT(*) v FROM orders")["v"]
    customers = one("SELECT COUNT(*) v FROM customers")["v"]
    pending = one("SELECT COUNT(*) v FROM orders WHERE status IN('Pending','Approved','Packed','Shipped')")["v"]
    # monthly revenue for the chart
    monthly = rows("""SELECT substr(date,1,7) m, ROUND(SUM(total),2) v
                      FROM orders WHERE status!='Cancelled' GROUP BY m ORDER BY m""")
    by_cat = rows("""SELECT p.category cat, ROUND(SUM(oi.qty*oi.price),2) v
                     FROM order_items oi JOIN products p ON p.id=oi.product_id
                     GROUP BY p.category ORDER BY v DESC""")
    top = rows("""SELECT name, category, price, units_sold, rating, accent
                  FROM products ORDER BY units_sold DESC LIMIT 6""")
    recent = rows("""SELECT o.order_number, c.company customer, o.date, o.total, o.status
                     FROM orders o JOIN customers c ON c.id=o.customer_id
                     ORDER BY o.date DESC, o.id DESC LIMIT 7""")
    status_counts = rows("SELECT status, COUNT(*) n FROM orders GROUP BY status")
    return jsonify({
        "kpi": {"revenue": revenue, "orders": orders, "customers": customers, "pending": pending},
        "monthly": monthly, "by_category": by_cat, "top_products": top,
        "recent_orders": recent, "status_counts": status_counts
    })


# ---------------- list endpoints ----------------
@app.route("/api/customers")
@login_required
def api_customers():
    return jsonify(rows("SELECT * FROM customers ORDER BY total_spent DESC"))


@app.route("/api/leads")
@login_required
def api_leads():
    return jsonify(rows("SELECT * FROM leads ORDER BY created_at DESC"))


@app.route("/api/orders")
@login_required
def api_orders():
    return jsonify(rows("""SELECT o.*, c.company customer FROM orders o
                           JOIN customers c ON c.id=o.customer_id ORDER BY o.date DESC, o.id DESC"""))


@app.route("/api/products")
@login_required
def api_products():
    return jsonify(rows("SELECT * FROM products ORDER BY units_sold DESC"))


@app.route("/api/inventory")
@login_required
def api_inventory():
    return jsonify(rows("""SELECT name, sku, category, stock, reorder_level, warehouse, accent,
                           CASE WHEN stock=0 THEN 'Out of Stock'
                                WHEN stock<reorder_level THEN 'Low' ELSE 'In Stock' END status
                           FROM products ORDER BY stock ASC"""))


@app.route("/api/suppliers")
@login_required
def api_suppliers():
    return jsonify(rows("SELECT * FROM suppliers ORDER BY rating DESC"))


@app.route("/api/employees")
@login_required
def api_employees():
    return jsonify(rows("SELECT * FROM employees ORDER BY id"))


@app.route("/api/support")
@login_required
def api_support():
    return jsonify(rows("SELECT * FROM support_tickets ORDER BY created_at DESC"))


@app.route("/api/notifications")
@login_required
def api_notifications():
    return jsonify(rows("SELECT * FROM notifications ORDER BY created_at DESC"))


# ---------------- CRUD (create / update / delete) ----------------
def today():
    return datetime.date.today().isoformat()

ACCENTS = ["#E11D48", "#EC4899", "#8B5CF6", "#F472B6", "#A855F7",
           "#F43F5E", "#D946EF", "#FB7185", "#9333EA", "#C026D3"]

# Each entity: which table, which fields the form sends, and defaults for the rest.
ENTITIES = {
    "customers": {"table": "customers",
                  "fields": ["name", "company", "email", "phone", "city", "country", "status"],
                  "defaults": lambda: {"created_at": today(), "total_orders": 0, "total_spent": 0.0}},
    "leads": {"table": "leads",
              "fields": ["name", "company", "email", "phone", "stage", "value", "source"],
              "defaults": lambda: {"created_at": today()}},
    "products": {"table": "products",
                 "fields": ["name", "category", "sku", "price", "cost", "stock", "colors"],
                 "defaults": lambda: {"subcategory": "", "sizes": "XS, S, M, L, XL",
                                      "accent": random.choice(ACCENTS), "reorder_level": 30,
                                      "warehouse": "WH-Tashkent", "units_sold": 0, "rating": 5.0}},
    "suppliers": {"table": "suppliers",
                  "fields": ["name", "contact", "phone", "email", "address", "products"],
                  "defaults": lambda: {"rating": 5.0}},
    "employees": {"table": "employees",
                  "fields": ["name", "role", "department", "email", "status"],
                  "defaults": lambda: {"last_active": today()}},
    "support": {"table": "support_tickets",
                "fields": ["customer", "subject", "priority", "status"],
                "defaults": lambda: {"created_at": today()}},
}


@app.route("/api/<entity>", methods=["POST"])
@login_required
def api_create(entity):
    cfg = ENTITIES.get(entity)
    if not cfg:
        return jsonify({"error": "unknown entity"}), 404
    d = request.get_json(force=True)
    data = {f: d.get(f) for f in cfg["fields"]}
    data.update(cfg["defaults"]())
    cols = ",".join(data.keys())
    ph = ",".join(["?"] * len(data))
    conn = db()
    cur = conn.execute(f"INSERT INTO {cfg['table']}({cols}) VALUES({ph})", list(data.values()))
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return jsonify({"ok": True, "id": rid})


@app.route("/api/<entity>/<int:rid>", methods=["PUT"])
@login_required
def api_update(entity, rid):
    cfg = ENTITIES.get(entity)
    if not cfg:
        return jsonify({"error": "unknown entity"}), 404
    d = request.get_json(force=True)
    sets = [f"{f}=?" for f in cfg["fields"] if f in d]
    vals = [d[f] for f in cfg["fields"] if f in d]
    if sets:
        vals.append(rid)
        conn = db()
        conn.execute(f"UPDATE {cfg['table']} SET {','.join(sets)} WHERE id=?", vals)
        conn.commit()
        conn.close()
    return jsonify({"ok": True})


@app.route("/api/<entity>/<int:rid>", methods=["DELETE"])
@login_required
def api_delete(entity, rid):
    cfg = ENTITIES.get(entity)
    if not cfg:
        return jsonify({"error": "unknown entity"}), 404
    conn = db()
    conn.execute(f"DELETE FROM {cfg['table']} WHERE id=?", (rid,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})


if __name__ == "__main__":
    if not os.path.exists(DB):
        print("Database not found. Run:  python seed_db.py")
    app.run(host="0.0.0.0", port=5000, debug=True)