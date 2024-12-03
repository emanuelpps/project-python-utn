from tkinter import *

root = Tk()

nombre_cliente = Label(root, text="Nombre de Cliente: ")
nombre_cliente.grid(row=0, column=0)
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

nombre_cliente = Entry(root)
nombre_cliente.grid(row=1, column=0)
telefono_cliente = Entry(root)
telefono_cliente.grid(row=1, column=1, sticky=W)

direccion_cliente = Entry(root)
direccion_cliente.grid(row=3, column=0, sticky=W)
monto_cliente = Entry(root)
monto_cliente.grid(row=3, column=1, sticky=W)

pedido_cliente = Entry(root)
pedido_cliente.grid(row=5, column=0, sticky=W)
fecha_cliente = Entry(root)
fecha_cliente.grid(row=5, column=1, sticky=W)


root.mainloop()
