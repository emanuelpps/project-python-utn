from tkinter import *
from tkinter import ttk
import sqlite3


order_id = 0

orders = []


root = Tk()

def create_db():
    connection = sqlite3.connect("orders.db")
    return connection

def orders_table(connection):
    cursor = connection.cursor()
    sql = "CREATE TABLE orders (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT, direccion TEXT, total TEXT, pedido TEXT, fecha TEXT)"
    cursor.execute(sql)
    connection.commit()
    
create_db()
orders_table(connection=create_db())
var_nombre_cliente = StringVar()
var_telefono_cliente = StringVar()
var_direccion_cliente = StringVar()
var_monto_cliente = StringVar()
var_pedido_cliente = StringVar()
var_fecha_cliente = StringVar()

nombre_cliente = Label(root, text="Nombre de Cliente: ")
nombre_cliente.grid(row=0, column=0, sticky=W)
telefono_cliente = Label(root, text="Telefono: ")
telefono_cliente.grid(row=0, column=1, sticky=W)

direccion_cliente = Label(root, text="Direccion: ")
direccion_cliente.grid(row=2, column=0, sticky=W)
monto_cliente = Label(root, text="Monto total: ")
monto_cliente.grid(row=2, column=1, sticky=W)

pedido_cliente = Label(root, text="Pedido: ")
pedido_cliente.grid(row=4, column=0, sticky=W)
fecha_cliente = Label(root, text="Fecha: ")
fecha_cliente.grid(row=4, column=1, sticky=W)

nombre_cliente = Entry(root, textvariable=var_nombre_cliente, width=100)
nombre_cliente.grid(row=1, column=0)
telefono_cliente = Entry(root, textvariable=var_telefono_cliente, width=100)
telefono_cliente.grid(row=1, column=1, sticky=W)

direccion_cliente = Entry(root, textvariable=var_direccion_cliente, width=100)
direccion_cliente.grid(row=3, column=0, sticky=W)
monto_cliente = Entry(root, textvariable=var_monto_cliente, width=100)
monto_cliente.grid(row=3, column=1, sticky=W)

pedido_cliente = Entry(root, textvariable=var_pedido_cliente, width=100)
pedido_cliente.grid(row=5, column=0, sticky=W)
fecha_cliente = Entry(root, textvariable=var_fecha_cliente, width=100)
fecha_cliente.grid(row=5, column=1, sticky=W)


def add_order():
    global order_id
    order_id += 1
    tree.insert("", 0, values=(order_id, var_nombre_cliente.get(), var_telefono_cliente.get(
    ), var_direccion_cliente.get(), var_monto_cliente.get(), var_pedido_cliente.get(), var_fecha_cliente.get()))
    return order_id


def delete_order():
    global order_id
    item = tree.focus()
    tree.delete(item)
    order_id -= 1


boton_guardar = Button(root, text="Guardar", command=add_order)
boton_guardar.grid(row=6, column=1, sticky=E)
boton_eliminar = Button(root, text="Eliminar", command=delete_order)
boton_eliminar.grid(row=6, column=1, sticky=W)


tree = ttk.Treeview(root)
tree.grid(row=7, column=0, columnspan=2)

tree["columns"] = ("#1", "#2", "#3", "#4", "#5", "#6")
tree.column("#0", width=0, stretch=NO)
tree.column("#1", width=80)
tree.column("#2", width=80)
tree.column("#3", width=80)
tree.column("#4", width=80)
tree.column("#5", width=80)
tree.column("#6", width=80)

tree.heading("#1", text="ID", anchor=W)
tree.heading("#2", text="Nombre", anchor=W)
tree.heading("#3", text="Telefono", anchor=W)
tree.heading("#4", text="Direccion", anchor=W)
tree.heading("#5", text="Monto", anchor=W)
tree.heading("#6", text="Pedido", anchor=W)

tree.grid(row=8, column=0, columnspan=2)
root.mainloop()
