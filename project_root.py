from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
import re

root = Tk()
root.title("Gestión de Pedidos de Delivery")

# DECLARACIONES DE COLORES DE LA APLICACIÓN
bg_color = "#f7f9fb"
title_bg_color = "#4a90e2"
button_bg_color = "#4caf50"
button_del_bg_color = "#f44336"
button_fg_color = "#ffffff"
entry_bg_color = "#ffffff"
tree_bg_color = "#eaf2f8"
tree_alt_bg_color = "#ffffff"
tree_heading_bg_color = "#2a76bf"
tree_heading_fg_color = "#ffffff"

# COLOR DEL BACKGROUND
root.configure(bg=bg_color)

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

# DECLARACIÓN DE VARIABLES DEL FORMULARIO
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


# TÍTULO PRINCIPAL
Label(
    root,
    text="Gestor de Pedidos de Delivery",
    bg=title_bg_color,
    fg="white",
    font=("Helvetica", 16, "bold"),
    pady=10
).grid(row=0, column=0, columnspan=2, sticky="nsew")

# FORMULARIO


def open_calendar():
    def select_date():
        selected_date = cal.selection_get().strftime("%d-%m-%Y")
        var_fecha_cliente.set(selected_date)
        calendar_window.destroy()

    calendar_window = Toplevel(root)
    calendar_window.title("Seleccionar Fecha")
    calendar_window.configure(bg=bg_color)

    cal = Calendar(calendar_window, date_pattern="dd-mm-yyyy", background=button_bg_color,
                   foreground=button_fg_color, selectmode="day")
    cal.pack(pady=10)

    btn_select_date = Button(calendar_window, text="Seleccionar", bg=button_bg_color,
                             fg=button_fg_color, command=select_date)
    btn_select_date.pack(pady=10)


Label(root, text="Nombre de Cliente: ", bg=bg_color).grid(
    row=1, column=0, sticky=W)
Entry(root, textvariable=var_nombre_cliente, bg=entry_bg_color).grid(
    row=2, column=0, sticky="nsew")

Label(root, text="Teléfono: ", bg=bg_color).grid(row=1, column=1, sticky=W)
Entry(root, textvariable=var_telefono_cliente,
      bg=entry_bg_color).grid(row=2, column=1, sticky="nsew")

Label(root, text="Dirección: ", bg=bg_color).grid(row=3, column=0, sticky=W)
Entry(root, textvariable=var_direccion_cliente,
      bg=entry_bg_color).grid(row=4, column=0, sticky="nsew")

Label(root, text="Monto total: ", bg=bg_color).grid(row=3, column=1, sticky=W)
Entry(root, textvariable=var_monto_cliente, bg=entry_bg_color).grid(
    row=4, column=1, sticky="nsew")

Label(root, text="Pedido: ", bg=bg_color).grid(row=5, column=0, sticky=W)
Entry(root, textvariable=var_pedido_cliente, bg=entry_bg_color).grid(
    row=6, column=0, sticky="nsew")

Label(root, text="Fecha (dd-mm-aaaa): ",
      bg=bg_color).grid(row=5, column=1, sticky=W)

frame_fecha = Frame(root, bg=bg_color)
frame_fecha.grid(row=6, column=1, sticky="nsew")

entry_fecha = Entry(frame_fecha, textvariable=var_fecha_cliente,
                    bg=entry_bg_color, state="readonly")
entry_fecha.pack(side=LEFT, fill=X, expand=True)

btn_calendar = Button(frame_fecha, text="📅", bg=button_bg_color,
                      fg=button_fg_color, command=open_calendar)
btn_calendar.pack(side=RIGHT)

# TREEVIEW
tree = ttk.Treeview(root, columns=("#1", "#2", "#3", "#4",
                    "#5", "#6", "#7"), show="headings")
tree.heading("#1", text="ID")
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Teléfono")
tree.heading("#4", text="Dirección")
tree.heading("#5", text="Monto")
tree.heading("#6", text="Pedido")
tree.heading("#7", text="Fecha")
tree.grid(row=9, column=0, columnspan=2)

# ESTILOS EN EL TREEVIEW
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview", background=tree_bg_color,
                fieldbackground=tree_bg_color)
style.map("Treeview", background=[("selected", title_bg_color)])
style.configure("Treeview.Heading", background=tree_heading_bg_color,
                foreground=tree_heading_fg_color)

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


def delete_order(selected_items):
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


def update_order(selected_items):
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
            "Atención", "No hay ninguna orden seleccionada"
        )


Button(root, text="Eliminar", bg=button_del_bg_color, fg=button_fg_color, command=lambda: (
    selected_items := tree.selection(), delete_order(selected_items))).grid(row=7, column=0, sticky=E)
Button(root, text="Actualizar", bg=button_bg_color, fg=button_fg_color, command=lambda: (
    selected_items := tree.selection(), update_order(selected_items))).grid(row=7, column=1, sticky=W)
Button(root, text="Guardar", bg=button_bg_color, fg=button_fg_color,
       command=add_order).grid(row=7, column=1, sticky=E)

# LLENADO DE LA TABLA
cursor = connection.cursor()
cursor.execute("SELECT * FROM orders")
rows = cursor.fetchall()
for row in rows:
    tree.insert("", "end", values=row)

root.mainloop()
