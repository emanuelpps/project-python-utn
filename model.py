import sqlite3
import re
from tkinter import messagebox
# CONEXIÓN A LA DB


def create_db():
    connection = sqlite3.connect("orders.db")
    return connection

# CREACIÓN DE LA TABLA SI NO EXISTE


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


# BOTONES Y SUS RESPECTIVAS FUNCIONES


def add_order(tree, var_nombre_cliente,
              var_telefono_cliente,
              var_direccion_cliente,
              var_monto_cliente,
              var_pedido_cliente,
              var_fecha_cliente):
    data = (
        var_nombre_cliente,
        var_telefono_cliente,
        var_direccion_cliente,
        var_monto_cliente,
        var_pedido_cliente,
        var_fecha_cliente
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


def delete_order(tree, selected_items):
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


def update_order(tree, selected_items,
                 var_nombre_cliente,
                 var_telefono_cliente,
                 var_direccion_cliente,
                 var_monto_cliente,
                 var_pedido_cliente,
                 var_fecha_cliente):
    if selected_items:
        for selected_item in selected_items:
            item = tree.item(selected_item)
            order_id = item['values'][0]
            new_data = (
                var_nombre_cliente,
                var_telefono_cliente,
                var_direccion_cliente,
                var_monto_cliente,
                var_pedido_cliente,
                var_fecha_cliente
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
            "Atención", "No hay ninguna orden seleccionada"
        )


# VALIDACIONES


def validate_name(nombre):
    return re.fullmatch(r'[\s a-zA-Z]+', nombre)


def validate_phone(telefono):
    return re.fullmatch(r'\d{0,10}', telefono)


def validate_address(direccion):
    return len(direccion.strip()) > 0
