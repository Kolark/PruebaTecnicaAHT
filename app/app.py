from flask import Flask, render_template, request, redirect, url_for
from markupsafe import escape
from sqlalchemy import create_engine, Integer, VARCHAR
from sqlalchemy.orm import DeclarativeBase, Session, mapped_column
from sqlalchemy import select, URL
from flask_bootstrap import Bootstrap
from sqlalchemy.exc import OperationalError
import time
import os

url = URL.create("mysql+pymysql",username=os.getenv("USER"),password=os.getenv("PASSWORD"),host="db",port=3306, database="inventory_db")

for attempt in range(10):
    try:
        engine = create_engine(url, echo=True)
        conn = engine.connect()
        conn.close()
        break
    except OperationalError as e:
        time.sleep(3)
else:
    raise RuntimeError("Could not connect to MySQL after 10 tries.")


class Base(DeclarativeBase):
    pass

class Inventory(Base):
    __tablename__ = "Inventory"
    id = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = mapped_column(VARCHAR(30), nullable=False)
    price = mapped_column(Integer, nullable=False)
    mac_address = mapped_column(VARCHAR(17),  nullable=False)
    serial_number = mapped_column(VARCHAR(20),nullable=False)
    manufacturer = mapped_column(VARCHAR(15), nullable=False)
    description = mapped_column(VARCHAR(255), nullable=False)
    def __repr__(self) -> str:
        return f"Inventory(id={self.id!r}, name={self.name!r}, price={self.price!r}, mac_address={self.mac_address!r}, serial_number={self.serial_number!r}, manufacturer={self.manufacturer!r}, description={self.description!r})"

Base.metadata.create_all(engine)

session = Session(engine)

app = Flask(__name__)
Bootstrap(app)

@app.route("/", methods=['GET'])
def show_inventory():
    select_inv = select(Inventory)
    inv = session.scalars(select_inv).all()
    return render_template("index.html", inventory = inv)


@app.route("/add", methods=['GET'])
def add_inventory_get():
    return render_template("add.html")

@app.route("/add", methods=['POST'])
def add_inventory_post():
    print("request", request)
    newItem = Inventory(
            name = request.form["name"],
            price = request.form["price"],
            mac_address = request.form["mac_address"],
            serial_number = request.form["serial_number"],
            manufacturer = request.form["manufacturer"],
            description = request.form["description"]
        )
    session.add(newItem)
    session.commit()
    return redirect(url_for('show_inventory'))

@app.route("/edit/<id>", methods=['GET', 'PUT'])
def edit_inventory_get(id):
    select_inv_item = select(Inventory).where(Inventory.id == id)
    item = session.scalars(select_inv_item).one_or_none()
    return render_template("edit.html", query_id = id, current_item= item)

@app.route("/edit/<id>", methods=['POST'])
def edit_inventory_post(id):
    select_inv_item = select(Inventory).where(Inventory.id == id)
    item = session.scalars(select_inv_item).one()
    item.name = request.form["name"] if request.form["name"] != "" else item.name
    item.price = request.form["price"] if request.form["price"] != "" else item.price
    item.mac_address = request.form["mac_address"] if request.form["mac_address"] != "" else item.mac_address
    item.serial_number = request.form["serial_number"] if request.form["serial_number"] != "" else item.serial_number
    item.manufacturer = request.form["manufacturer"] if request.form["manufacturer"] != "" else item.manufacturer
    item.description = request.form["description"] if request.form["description"] != "" else item.description
    session.commit()
    return redirect(url_for('show_inventory'))


@app.route("/delete/<id>",methods=['GET'])
def delete_inventory_get(id):
    select_inv_item = select(Inventory).where(Inventory.id == id)
    item = session.scalars(select_inv_item).one_or_none()
    return render_template("delete.html", query_id = id, current_item= item)

@app.route("/delete/<id>",methods=['GET', 'POST'])
def delete_inventory_post(id):
    select_inv_item = select(Inventory).where(Inventory.id == id)
    item = session.scalars(select_inv_item).one()
    session.delete(item)
    return redirect(url_for('show_inventory'))


if __name__ == '__main__':
   app.run(host='0.0.0.0',port=5000)