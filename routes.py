from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import get_db

routes = Blueprint("routes", __name__)

# Home
@routes.route("/")
def home():
    return render_template("index.html")

# Menu page
@routes.route("/menu", methods=["GET", "POST"])
def menu():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        cur.execute("INSERT INTO menu(name, price) VALUES (%s, %s)", (name, price))
        conn.commit()
        flash("Menu item added!", "success")

    cur.execute("SELECT * FROM menu")
    items = cur.fetchall()

    conn.close()
    return render_template("menu.html", items=items)

# Place order
@routes.route("/order", methods=["GET", "POST"])
def order():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM menu")
    items = cur.fetchall()

    if request.method == "POST":
        item_id = request.form["item_id"]
        qty = int(request.form["quantity"])

        cur.execute("SELECT price FROM menu WHERE id=%s", (item_id,))
        price = cur.fetchone()[0]

        total = price * qty

        cur.execute("INSERT INTO orders(item_id, quantity, total) VALUES (%s, %s, %s)",
                    (item_id, qty, total))
        conn.commit()

        flash("Order placed!", "success")
        return redirect(url_for("routes.orders"))

    return render_template("place_order.html", items=items)

# Orders page
@routes.route("/orders", methods=["GET", "POST"])
def orders():
    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        order_id = request.form["order_id"]
        status = request.form["status"]
        cur.execute("UPDATE orders SET payment_status=%s WHERE id=%s", (status, order_id))
        conn.commit()
        flash("Status Updated!", "success")

    cur.execute("""
        SELECT orders.id, menu.name, orders.quantity, orders.total, orders.payment_status
        FROM orders
        JOIN menu ON menu.id = orders.item_id
    """)
    data = cur.fetchall()

    conn.close()
    return render_template("orders.html", orders=data)
