from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import re

root = Tk()
root.title("Gestión de Órdenes")

# CONEXION A LA DB


def create_db():
    connection = sqlite3.connect("orders.db")
    return connection

# CREACION DE LA TABLA SI NO EXISTE


def orders_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            telefono TEXT,
            direccion TEXT,
            total TEXT,
            pedido TEXT,
            fecha TEXT
        )
    """)
    connection.commit()


connection = create_db()
orders_table(connection)

# DECALRACION DE VARIABLES DEL FORMULARIO

var_nombre_cliente = StringVar()
var_telefono_cliente = StringVar()
var_direccion_cliente = StringVar()
var_monto_cliente = StringVar()
var_pedido_cliente = StringVar()
var_fecha_cliente = StringVar()


# VALIDACIONES


def validate_name(nombre):
    return re.fullmatch(r'[a-zA-Z]+', nombre)


def validate_phone(telefono):
    return re.fullmatch(r'\d{0,10}', telefono)


def validate_address(direccion):
    return len(direccion.strip()) > 0


# FORMULARIO
Label(root, text="Nombre de Cliente: ").grid(row=0, column=0, sticky=W)
Entry(root, textvariable=var_nombre_cliente).grid(
    row=1, column=0, sticky="nsew")

Label(root, text="Teléfono: ").grid(row=0, column=1, sticky=W)
Entry(root, textvariable=var_telefono_cliente).grid(
    row=1, column=1, sticky="nsew")

Label(root, text="Dirección: ").grid(row=2, column=0, sticky=W)
Entry(root, textvariable=var_direccion_cliente).grid(
    row=3, column=0, sticky="nsew")

Label(root, text="Monto total: ").grid(row=2, column=1, sticky=W)
Entry(root, textvariable=var_monto_cliente).grid(
    row=3, column=1, sticky="nsew")

Label(root, text="Pedido: ").grid(row=4, column=0, sticky=W)
Entry(root, textvariable=var_pedido_cliente).grid(
    row=5, column=0, sticky="nsew")

Label(root, text="Fecha (dd-mm-aaaa): ").grid(row=4, column=1, sticky=W)
Entry(root, textvariable=var_fecha_cliente).grid(
    row=5, column=1, sticky="nsew")


tree = ttk.Treeview(root, columns=("#1", "#2", "#3", "#4",
                    "#5", "#6", "#7"), show="headings")
tree.heading("#1", text="ID", anchor=W)
tree.heading("#2", text="Nombre", anchor=W)
tree.heading("#3", text="Teléfono", anchor=W)
tree.heading("#4", text="Dirección", anchor=W)
tree.heading("#5", text="Monto", anchor=W)
tree.heading("#6", text="Pedido", anchor=W)
tree.heading("#7", text="Fecha", anchor=W)
tree.grid(row=8, column=0, columnspan=2)

# BOTONES Y SUS RESPECTIVAS FUNCIONES


def add_order():
    data = (
        var_nombre_cliente.get(),
        var_telefono_cliente.get(),
        var_direccion_cliente.get(),
        var_monto_cliente.get(),
        var_pedido_cliente.get(),
        var_fecha_cliente.get()
    )

    if not validate_name(data[0]):
        messagebox.showerror("Error", "El nombre solo debe contener letras.")
        return
    if not validate_phone(data[1]):
        messagebox.showerror(
            "Error", "El teléfono debe contener hasta 10 dígitos.")
        return
    if not validate_address(data[2]):
        messagebox.showerror("Error", "La dirección no es válida.")
        return

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO orders (nombre, telefono, direccion, total, pedido, fecha) VALUES (?, ?, ?, ?, ?, ?)", data)
    connection.commit()
    last_id = cursor.lastrowid
    tree.insert("", "end", values=(last_id, *data))


def delete_order():
    selected_items = tree.selection()
    if selected_items:
        for selected_item in selected_items:
            item = tree.item(selected_item)
            order_id_to_delete = item['values'][0]
            cursor = connection.cursor()
            cursor.execute("DELETE FROM orders WHERE id = ?",
                           (order_id_to_delete,))
            connection.commit()
            tree.delete(selected_item)
            messagebox.showwarning(
                "Atención", "La orden fue eliminada con exito")


def update_order():
    selected_items = tree.selection()
    if selected_items:
        for selected_item in selected_items:
            item = tree.item(selected_item)
            order_id = item['values'][0]
            new_data = (
                var_nombre_cliente.get(),
                var_telefono_cliente.get(),
                var_direccion_cliente.get(),
                var_monto_cliente.get(),
                var_pedido_cliente.get(),
                var_fecha_cliente.get()
            )
            cursor = connection.cursor()
            cursor.execute("""
                UPDATE orders
                SET nombre = ?, telefono = ?, direccion = ?, total = ?, pedido = ?, fecha = ?
                WHERE id = ?
            """, (*new_data, order_id))
            connection.commit()
            tree.item(selected_item, values=(order_id, *new_data))
            messagebox.showinfo(
                "Actualizado", "La orden fue actualizada correctamente")
    else:
        messagebox.showwarning(
            "Atención", "No hay ninguna orden seleccionada para actualizar."
        )


Button(root, text="Guardar", command=add_order).grid(
    row=6, column=1, sticky=E)
Button(root, text="Eliminar", command=delete_order).grid(
    row=6, column=1, sticky=W)
Button(root, text="Actualizar", command=update_order).grid(
    row=6, column=0, sticky=E
)

# LLENADO DE LA TABLA
cursor = connection.cursor()
cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()
for row in rows:
    tree.insert("", "end", values=row)

root.mainloop()
