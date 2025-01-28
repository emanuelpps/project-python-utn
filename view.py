from tkcalendar import Calendar
from tkinter import ttk
from tkinter import StringVar, Button, Entry, Frame, Label, LEFT, RIGHT, W, X, E, Toplevel
from model import add_order, delete_order, update_order


def main_view(root):
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

    # DECLARACIÓN DE VARIABLES DEL FORMULARIO
    tree = ttk.Treeview()
    var_nombre_cliente = StringVar()
    var_telefono_cliente = StringVar()
    var_direccion_cliente = StringVar()
    var_monto_cliente = StringVar()
    var_pedido_cliente = StringVar()
    var_fecha_cliente = StringVar()

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

    Label(root, text="Dirección: ", bg=bg_color).grid(
        row=3, column=0, sticky=W)
    Entry(root, textvariable=var_direccion_cliente,
          bg=entry_bg_color).grid(row=4, column=0, sticky="nsew")

    Label(root, text="Monto total: ", bg=bg_color).grid(
        row=3, column=1, sticky=W)
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
                    foreground=tree_heading_bg_color)
    
    
    Button(root, text="Eliminar", bg=button_del_bg_color, fg=button_fg_color, command=lambda: (
        selected_items := tree.selection(), delete_order(selected_items))).grid(row=7, column=0, sticky=E)
    Button(root, text="Actualizar", bg=button_bg_color, fg=button_fg_color, command=lambda: (
        selected_items := tree.selection(), update_order(selected_items))).grid(row=7, column=1, sticky=W)
    Button(root, text="Guardar", bg=button_bg_color, fg=button_fg_color,
        command=lambda: (add_order(tree, var_nombre_cliente,
              var_telefono_cliente.get(),
              var_direccion_cliente.get(),
              var_monto_cliente.get(),
              var_pedido_cliente.get(),
              var_fecha_cliente.get()))).grid(row=7, column=1, sticky=E)

