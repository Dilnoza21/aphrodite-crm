"""
seed_db.py — Generates the Aphrodite Dress CRM database (SQLite).
Run this once before starting the app:  python seed_db.py
It creates aphrodite.db with realistic wholesale-clothing data.
"""
import sqlite3, random, hashlib
from datetime import datetime, timedelta

random.seed(7)
DB = "aphrodite.db"

def h(pw):  # simple password hash for the demo
    return hashlib.sha256(pw.encode()).hexdigest()

conn = sqlite3.connect(DB)
c = conn.cursor()

# ---------- schema ----------
c.executescript("""
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS leads;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS suppliers;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS notifications;

CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, role TEXT, name TEXT);
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT, company TEXT, email TEXT, phone TEXT,
    city TEXT, country TEXT, status TEXT, created_at TEXT, total_orders INTEGER, total_spent REAL);
CREATE TABLE leads (id INTEGER PRIMARY KEY, name TEXT, company TEXT, email TEXT, phone TEXT,
    stage TEXT, value REAL, source TEXT, created_at TEXT);
CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, category TEXT, subcategory TEXT, sku TEXT,
    price REAL, cost REAL, sizes TEXT, colors TEXT, accent TEXT, stock INTEGER, reorder_level INTEGER,
    warehouse TEXT, units_sold INTEGER, rating REAL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, order_number TEXT, customer_id INTEGER, date TEXT,
    total REAL, status TEXT, payment TEXT, items_count INTEGER);
CREATE TABLE order_items (id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER, price REAL);
CREATE TABLE suppliers (id INTEGER PRIMARY KEY, name TEXT, contact TEXT, phone TEXT, email TEXT,
    address TEXT, products TEXT, rating REAL);
CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, role TEXT, department TEXT, email TEXT,
    status TEXT, last_active TEXT);
CREATE TABLE support_tickets (id INTEGER PRIMARY KEY, customer TEXT, subject TEXT, status TEXT,
    priority TEXT, created_at TEXT);
CREATE TABLE notifications (id INTEGER PRIMARY KEY, type TEXT, message TEXT, created_at TEXT, is_read INTEGER);
""")

# ---------- users ----------
c.execute("INSERT INTO users(username,password,role,name) VALUES(?,?,?,?)",
            ("superadmin", h("superadmin1234"), "Super Admin", "Aphrodite Super Admin"))
c.execute("INSERT INTO users(username,password,role,name) VALUES(?,?,?,?)",
            ("admin", h("admin1234"), "Admin", "Aphrodite Admin"))

# ---------- products ----------
adjectives = ["Aurora","Velvet","Celeste","Seraphine","Mirage","Lumière","Étoile","Reverie","Allure",
                "Opaline","Marguerite","Bijou","Soleil","Noir","Ivory","Rosé","Camélia","Divine","Eden","Belle"]
nouns = ["Gown","Slip Dress","Wrap Dress","Maxi","Midi","A-Line","Sheath","Ballgown","Tea Dress","Shift"]
subcats = {"Evening":["Gown","Ballgown","Slip Dress"], "Casual":["Wrap Dress","Tea Dress","Shift","Midi"],
           "Wedding":["Ballgown","A-Line","Sheath","Maxi"], "Luxury":["Gown","Sheath","Maxi","Midi"]}
accents = ["#E11D48","#EC4899","#8B5CF6","#F472B6","#A855F7","#F43F5E","#D946EF","#FB7185","#9333EA","#C026D3"]
colorsets = ["Blush, Ivory, Noir","Rose, Champagne","Violet, Midnight","Crimson, Wine","Lilac, Pearl","Coral, Cream"]
sizes = "XS, S, M, L, XL"

products = []
for i in range(1, 33):
    cat = random.choice(list(subcats.keys()))
    sub = random.choice(subcats[cat])
    name = f"{random.choice(adjectives)} {sub}"
    base = {"Evening":120,"Casual":45,"Wedding":260,"Luxury":340}[cat]
    price = round(base + random.uniform(-15, 90), 2)
    cost = round(price * random.uniform(0.38, 0.55), 2)
    stock = random.randint(0, 240)
    products.append((i, name, cat, sub, f"APH-{1000+i}", price, cost, sizes,
                     random.choice(colorsets), random.choice(accents), stock,
                     30, random.choice(["WH-Tashkent","WH-Almaty","WH-Astana"]),
                     random.randint(20, 900), round(random.uniform(3.8, 5.0), 1)))
c.executemany("INSERT INTO products VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", products)

# ---------- customers ----------
first = ["Elena","Marco","Sofia","Liam","Aisha","Noah","Camille","Yusuf","Mia","Diana","Omar","Lucia",
         "Adrian","Nadia","Victor","Leyla","Hugo","Farah","Iris","Daniyar","Selin","Arman","Bianca","Timur"]
last = ["Petrova","Rossi","Khan","Garcia","Ali","Schmidt","Dubois","Karimov","Novak","Costa","Yilmaz",
        "Ibrahim","Laurent","Saidova","Park","Moretti","Tanaka","Hassan","Volkov","Aliyev"]
boutiques = ["Maison","Atelier","Boutique","Studio","Couture House","Threads","Loom","Drapé","Étoile",
             "Velour","La Mode","Glamour","Chic","Élégance","Vesta"]
cities = [("Tashkent","Uzbekistan"),("Almaty","Kazakhstan"),("Astana","Kazakhstan"),("Bishkek","Kyrgyzstan"),
          ("Dubai","UAE"),("Istanbul","Türkiye"),("Baku","Azerbaijan"),("Tbilisi","Georgia"),("Samarkand","Uzbekistan")]
statuses = ["Active","Active","Active","VIP","New","Inactive"]

now = datetime(2026, 6, 1)
customers = []
for i in range(1, 45):
    nm = f"{random.choice(first)} {random.choice(last)}"
    comp = f"{random.choice(boutiques)} {random.choice(last)}"
    city, country = random.choice(cities)
    created = now - timedelta(days=random.randint(5, 900))
    customers.append((i, nm, comp, f"{nm.split()[0].lower()}@{comp.split()[0].lower()}.com",
                      f"+99 {random.randint(700,999)} {random.randint(100,999)} {random.randint(10,99)} {random.randint(10,99)}",
                      city, country, random.choice(statuses), created.strftime("%Y-%m-%d"), 0, 0.0))
c.executemany("INSERT INTO customers VALUES(?,?,?,?,?,?,?,?,?,?,?)", customers)

# ---------- orders + items ----------
order_statuses = ["Pending","Approved","Packed","Shipped","Delivered","Delivered","Delivered","Cancelled"]
payments = ["Bank Transfer","Card","PayPal","Invoice"]
oid = 1; iid = 1
cust_totals = {i: [0, 0.0] for i in range(1, 45)}
for _ in range(120):
    cid = random.randint(1, 44)
    odate = now - timedelta(days=random.randint(0, 180))
    n_items = random.randint(1, 5)
    total = 0.0
    items = []
    for _ in range(n_items):
        p = random.choice(products)
        qty = random.randint(3, 40)  # wholesale quantities
        line = round(p[5] * qty * 0.8, 2)  # wholesale discount
        total += line
        items.append((iid, oid, p[0], qty, p[5])); iid += 1
    status = random.choice(order_statuses)
    c.execute("INSERT INTO orders VALUES(?,?,?,?,?,?,?,?)",
              (oid, f"APH-{674000+oid}", cid, odate.strftime("%Y-%m-%d"),
               round(total, 2), status, random.choice(payments), n_items))
    c.executemany("INSERT INTO order_items VALUES(?,?,?,?,?)", items)
    if status != "Cancelled":
        cust_totals[cid][0] += 1
        cust_totals[cid][1] += total
    oid += 1

for cid, (cnt, spent) in cust_totals.items():
    c.execute("UPDATE customers SET total_orders=?, total_spent=? WHERE id=?", (cnt, round(spent, 2), cid))

# ---------- leads ----------
lead_stages = ["New","Contacted","Negotiation","Won","Lost"]
sources = ["Instagram","Trade Show","Referral","Website","Cold Email","WhatsApp"]
leads = []
for i in range(1, 27):
    nm = f"{random.choice(first)} {random.choice(last)}"
    comp = f"{random.choice(boutiques)} {random.choice(last)}"
    leads.append((i, nm, comp, f"{nm.split()[0].lower()}@{comp.split()[0].lower()}.com",
                  f"+99 {random.randint(700,999)} {random.randint(100,999)} {random.randint(1000,9999)}",
                  random.choice(lead_stages), round(random.uniform(800, 25000), 2),
                  random.choice(sources), (now - timedelta(days=random.randint(0, 60))).strftime("%Y-%m-%d")))
c.executemany("INSERT INTO leads VALUES(?,?,?,?,?,?,?,?,?)", leads)

# ---------- suppliers ----------
sup_names = ["Silk Road Textiles","Aurora Fabrics","Lumen Couture Supply","Velvet & Co","Étoile Mills",
             "Maison Threads","Orient Weave","Bella Materials","Noir Fabrik","Pearl Textile Group",
             "Crimson Looms","Atlas Garments"]
suppliers = []
for i, sn in enumerate(sup_names, 1):
    suppliers.append((i, sn, f"{random.choice(first)} {random.choice(last)}",
                      f"+99 {random.randint(700,999)} {random.randint(100,999)} {random.randint(1000,9999)}",
                      f"sales@{sn.split()[0].lower()}.com",
                      f"{random.randint(1,200)} {random.choice(['Textile','Silk','Cotton','Market'])} St, {random.choice(cities)[0]}",
                      random.choice(["Silk, Satin","Cotton, Linen","Lace, Tulle","Velvet, Chiffon"]),
                      round(random.uniform(3.9, 5.0), 1)))
c.executemany("INSERT INTO suppliers VALUES(?,?,?,?,?,?,?,?)", suppliers)

# ---------- employees ----------
roles = [("Admin","Management"),("Sales Manager","Sales"),("Sales Manager","Sales"),
         ("Warehouse Staff","Operations"),("Warehouse Staff","Operations"),
         ("Support Staff","Support"),("Support Staff","Support"),("Sales Manager","Sales"),
         ("Warehouse Staff","Operations"),("Support Staff","Support")]
employees = []
for i, (role, dept) in enumerate(roles, 1):
    nm = f"{random.choice(first)} {random.choice(last)}"
    employees.append((i, nm, role, dept, f"{nm.split()[0].lower()}@aphrodite.com",
                      random.choice(["Online","Online","Away","Offline"]),
                      (now - timedelta(hours=random.randint(0, 72))).strftime("%Y-%m-%d %H:%M")))
c.executemany("INSERT INTO employees VALUES(?,?,?,?,?,?,?)", employees)

# ---------- support tickets ----------
subjects = ["Return request — wrong size","Damaged item on arrival","Late delivery enquiry",
            "Colour mismatch","Bulk discount question","Invoice correction","Reorder availability",
            "Quality complaint","Shipment tracking","Size chart request"]
tickets = []
for i in range(1, 13):
    tickets.append((i, f"{random.choice(first)} {random.choice(last)}", random.choice(subjects),
                    random.choice(["Open","In Progress","Resolved","Closed"]),
                    random.choice(["Low","Medium","High"]),
                    (now - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")))
c.executemany("INSERT INTO support_tickets VALUES(?,?,?,?,?,?)", tickets)

# ---------- notifications ----------
notifs = [
    ("order","New order APH-674121 received from Maison Rossi","2026-06-01 09:12",0),
    ("stock","Low stock alert: Aurora Gown (8 left)","2026-06-01 08:40",0),
    ("customer","New customer registered: Atelier Khan","2026-05-31 17:22",0),
    ("shipping","Order APH-674098 has been shipped","2026-05-31 14:05",1),
    ("payment","Payment received for invoice APH-674077","2026-05-31 11:50",1),
    ("lead","New lead from Instagram: Boutique Volkov","2026-05-30 16:30",1),
    ("stock","Low stock alert: Seraphine Slip Dress (5 left)","2026-05-30 10:15",1),
]
c.executemany("INSERT INTO notifications(type,message,created_at,is_read) VALUES(?,?,?,?)", notifs)

conn.commit()
# quick summary
for t in ["users","customers","leads","products","orders","order_items","suppliers","employees","support_tickets","notifications"]:
    n = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"  {t:<16} {n}")
conn.close()
print("Database created: aphrodite.db")
