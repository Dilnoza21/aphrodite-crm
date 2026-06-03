# Aphrodite Dress CRM — Sidebar Structure (Recommended)

**Tagline:** "Designed so everyone falls in love."

The navigation is organised into **groups** so the sidebar stays easy to scan. The *Sales* group is the heart of the CRM; *Catalogue & Operations* covers the lighter ERP/WMS side that the CRM integrates with. Logout is pinned separately at the very bottom, next to the signed-in user.

```
Dashboard
│
├─ SALES
│   ├─ Customers
│   ├─ Leads & Sales
│   ├─ Orders
│   └─ Support
│
├─ CATALOGUE & OPERATIONS
│   ├─ Products
│   ├─ Inventory
│   └─ Suppliers
│
├─ STAFF
│   └─ Employees
│
├─ INSIGHTS
│   ├─ Analytics
│   └─ Reports
│
└─ SYSTEM
    ├─ Notifications
    └─ Settings

────────────────────
[ User avatar + name ]
Logout
```

---

## Dashboard

The main overview screen. Pulls the most important numbers and activity into one place so a manager understands company performance at a glance, without opening other pages.

**Main features:** total revenue · monthly orders · new customers · pending deliveries · sales-growth chart · top-selling products · recent activity feed · notifications summary.

**Purpose:** a single-screen summary of the whole business.

---

## SALES

### Customers
Manages all wholesale clients (boutiques, shops, online stores) and their information. Staff can add, edit, search and view full account history.

**Main features:** customer profiles · contact information · company details · account status · order history · notes/communication log · search and filtering.

**Purpose:** maintain strong customer relationships and faster service.

### Leads & Sales
Tracks potential customers and the sales pipeline so reps can move opportunities toward a sale.

**Main features:** lead tracking · sales pipeline · conversion tracking · follow-up reminders · sales-performance stats.

**Lead stages:** New → Contacted → Negotiation → Won / Lost.

**Purpose:** improve sales management and convert leads into customers.

### Orders
Manages every wholesale clothing order from creation to delivery.

**Main features:** create orders · order-status tracking · payment tracking · delivery status · invoice management.

**Order statuses:** Pending → Approved → Packed → Shipped → Delivered (or Cancelled).

**Purpose:** accurate order processing and shipment management.

### Support
Handles customer issues after a sale — returns, complaints, sizing/quality problems — which are common in clothing wholesale. (This is where the *Support Staff* role works, so the role now has a home.)

**Main features:** support tickets · ticket status · linked customer & order · response notes · resolution tracking.

**Ticket statuses:** Open → In Progress → Resolved → Closed.

**Purpose:** resolve customer problems quickly and keep a record of them.

---

## CATALOGUE & OPERATIONS

### Products
Manages the clothing items Aphrodite Dress sells, organised into categories with pricing and details.

**Main features:** product catalogue · categories · product images · sizes and colours · wholesale pricing.

**Categories:** Dresses (Evening · Casual · Wedding) · Luxury Collections. *(Dress types sit as sub-categories under "Dresses" rather than beside it, to avoid overlap.)*

**Purpose:** organise and manage the product range efficiently.

### Inventory
Tracks stock levels and availability — basic warehouse monitoring.

**Main features:** stock-quantity tracking · low-stock alerts · warehouse stock monitoring · inventory updates.

**Inventory fields:** SKU · quantity · reorder level · warehouse location.

**Purpose:** prevent stock shortages and support inventory control.

### Suppliers
Stores information about clothing suppliers and vendors.

**Main features:** supplier profiles · contact information · supplied products · delivery tracking.

**Supplier fields:** supplier name · contact person · phone · email · address.

**Purpose:** improve supplier communication and product sourcing.

---

## STAFF

### Employees
Manages staff accounts, roles and access within the CRM.

**Main features:** employee profiles · department management · user roles · permissions · activity tracking.

**Roles:** Admin · Sales Manager · Warehouse Staff · Support Staff.

**Purpose:** control employee access and support internal staff management.

---

## INSIGHTS

### Analytics
Interactive business intelligence — visual charts a manager can explore to spot trends.

**Main features:** revenue charts · customer-growth charts · product-performance analysis · regional sales stats.

**Chart types:** bar · pie · line.

**Purpose:** support decision-making with live, visual analytics.

### Reports
Generates detailed, exportable documents for management and record-keeping. *(Distinct from Analytics: Analytics is for exploring on screen; Reports is for producing a finished document.)*

**Main features:** sales reports · customer reports · inventory reports · employee-performance reports · revenue reports.

**Export options:** PDF · Excel.

**Purpose:** analyse performance and keep formal records.

---

## SYSTEM

### Notifications
System alerts and important updates in real time.

**Main features:** new-order alerts · low-stock warnings · delivery updates · payment reminders · customer-activity alerts.

**Examples:** "New customer registered" · "Low stock for luxury dresses" · "Order #1024 shipped".

**Purpose:** keep staff informed of important activity as it happens.

### Settings
Manage system preferences and account settings.

**Main features:** profile settings · password management · security settings · theme customisation · backup settings.

**Purpose:** let users and admins configure the CRM.

---

## Logout (pinned at bottom)

Securely signs the user out and ends the active session.

**Purpose:** protect accounts and system security. Placed at the very bottom of the sidebar, separated from the navigation and shown next to the signed-in user's name — the standard, expected pattern.

---

## Summary of what changed from your version

1. **Grouped the 13 modules** into Sales / Catalogue & Operations / Staff / Insights / System, so the sidebar scans cleanly.
2. **Added a Support module** under Sales, giving the *Support Staff* role a place to work and covering returns/complaints (important for clothing).
3. **Fixed product categories** — dress types nested under "Dresses" instead of beside it.
4. **Pinned Logout** to the bottom, separated from the nav, next to the user.
5. **Sharpened Analytics vs Reports** (explore on screen vs export a document) and added a communication log to Customers so customer messages have a home without a separate Messages module.
