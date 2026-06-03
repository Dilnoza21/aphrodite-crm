# Aphrodite Dress CRM

A full-stack CRM web application for **Aphrodite Dress**, a wholesale ready-made
clothing company. *"Designed so everyone falls in love."*

This is the **dynamic website** built for Learning Aim C of BTEC Unit 6
(Networking in the Cloud). It has a Python (Flask) backend, a real SQLite
database, and an animated front end in a rose / violet / red palette.

---

## What's inside

| File | What it is |
|------|------------|
| `app.py` | Flask backend — serves the pages and a JSON API, with session login |
| `seed_db.py` | Builds the SQLite database and fills it with realistic sample data |
| `index.html` | Animated landing page (the public storefront) |
| `dashboard.html` | The CRM admin dashboard (single-page app) |
| `static/chart.umd.js` | Chart.js library, included locally so charts work offline |
| `requirements.txt` | Python packages needed (just Flask) |

The database file `aphrodite.db` is **not** included — you generate it
yourself in step 2 below (this is part of the assessment evidence).

---

## How to run it (on your own computer)

You need **Python 3** installed.

**1. Install Flask**
```
pip install -r requirements.txt
```

**2. Build the database** (run once)
```
python seed_db.py
```
This creates `aphrodite.db` with 1 admin user, 44 customers, 26 leads,
32 dress products, 120 orders, 12 suppliers, 10 employees, support
tickets and notifications.

**3. Start the server**
```
python app.py
```

**4. Open it in your browser**
```
http://localhost:5000
```

**5. Log in**
- Username: `admin`
- Password: `admin1234`

Click **Sign In** on the landing page, enter those details, and you'll be
taken to the dashboard.

> On Windows, if `python` doesn't work, try `py` instead
> (`py seed_db.py`, `py app.py`).

---

## What the app does

- **Landing page** — an animated storefront with the brand, hero section,
  categories and a sign-in modal.
- **Login** — checks the username and password against the database. The
  password is stored as a SHA-256 hash, not in plain text.
- **Dashboard** — KPI cards (revenue, orders, customers, deliveries), a
  revenue line chart, a sales-by-category doughnut chart, recent orders and
  best-selling products. All numbers come from the database in real time.
- **Modules** — Customers, Leads & Sales, Orders, Support, Products,
  Inventory, Suppliers, Employees, Analytics, Reports, Notifications and
  Settings, organised into groups in the sidebar.

The backend exposes a small JSON API (for example `/api/dashboard`,
`/api/customers`, `/api/orders`). Every data endpoint is protected — if you
are not logged in it returns "401 unauthorized", which you can demonstrate
as part of your security testing.

---

## Deploying to the cloud (for Learning Aim C)

For the assessment you need to host this on a cloud network and show the
networking around it. A simple, free-tier-friendly route on **AWS**:

1. **VPC** — create a Virtual Private Cloud for Aphrodite Dress.
2. **Subnets** — a *public* subnet (for the web server) and a *private*
   subnet (for the database, in a real production setup).
3. **Internet Gateway** — attach it to the VPC so the public subnet can
   reach the internet; add a route in the public subnet's route table.
4. **EC2 instance** — launch a free-tier `t2.micro` (Ubuntu) in the public
   subnet. This is your web server.
5. **Security Group** — allow inbound SSH (port 22, your IP only) and
   HTTP (port 80). This acts as the instance firewall.
6. **Deploy the app** — connect with SSH, install Python and Flask, copy
   these files up, run `python seed_db.py`, then run the app behind a
   production server (e.g. `gunicorn`) on port 80 (or use Nginx in front).
7. **Elastic IP / DNS** — attach a static public IP, and optionally a
   domain name through Route 53, so the site has a stable address.
8. **Load balancer + auto scaling** (for the higher grades) — put an
   Application Load Balancer in front and an Auto Scaling Group behind it,
   so traffic is spread across instances and more are added under load.

Take a screenshot at every step (VPC, subnets, gateway, EC2, security
group, the running site, the load balancer). Those screenshots are the
evidence the practical criteria are marked on.

---

## Notes

- The secret key in `app.py` is a placeholder — change it before any real
  deployment.
- The charts use Chart.js, included locally in `static/` so they render even
  without an internet connection.
- This project is sample coursework for BTEC Unit 6 and uses made-up data.
