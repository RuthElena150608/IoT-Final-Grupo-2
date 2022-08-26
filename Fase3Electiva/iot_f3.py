from pickle import NONE
import tkinter as tk
from tkinter import CENTER, END, PhotoImage, ttk
from turtle import bgcolor, width
from dataBaseMongodb import mongo
import ConectionMqtt as conectionMqqtt
from faker import Faker
from PIL import Image, ImageTk


mongoDb = mongo()
ve = 1
pulsedBotton = 0
appmain = tk.Tk()
appmain.geometry("650x320")
appmain.resizable(False, False)
appmain.title("Proyecto de Electiva")
appmain.iconbitmap("img/semaforo.ico")
appmain.config(
    bg="white",
    relief="groove"

)

offFrame = tk.Frame()
offFrame.pack(side="right", anchor="n")
offFrame.config(
    bg="white",
    width="200",
    height="200"
)
rojoFrame = tk.Frame()
rojoFrame.pack(side="right", anchor=tk.N)
rojoFrame.config(
    bg="white",
    width="200",
    height="200"
)
verdeFrame = tk.Frame()
verdeFrame.pack(side="right", anchor=tk.N)
verdeFrame.config(
    bg="white",
    width="200",
    height="200"
)
amarilloFrame = tk.Frame()
amarilloFrame.pack(side="right", anchor=tk.N)
amarilloFrame.config(
    bg="white",
    width="200",
    height="200"
)
amarilloFrame.forget()
rojoFrame.forget()
verdeFrame.forget()


img_off = tk.PhotoImage(file="img/off.gif")
img_amarillo = tk.PhotoImage(file="img/amarillo.gif")
img_verde = tk.PhotoImage(file="img/verde.gif")
img_rojo = tk.PhotoImage(file="img/rojo.gif")

img_semaforo_label_amarilloframe = tk.Label(
    amarilloFrame,
    image=img_amarillo,
    width="100",
    height="150"
).place(x=10, y=10)

img_semaforo_label_rojoframe = tk.Label(
    rojoFrame,
    image=img_rojo,
    width="100",
    height="150"
).place(x=10, y=10)

img_semaforo_label_verdeframe = tk.Label(
    verdeFrame,
    image=img_verde,
    width="100",
    height="150"
).place(x=10, y=10)

img_semaforo_label_offframe = tk.Label(
    offFrame,
    image=img_off,
    width="100",
    height="150"
).place(x=10, y=10)


img_txt_label_verdeframe = tk.Label(
    verdeFrame,
    text="Puedes Pasar",
    fg="springGreen2",
    bg="black",
    font=("Arial", 16)
).place(x=-5, y=155)

img_txt_label_rojoframe = tk.Label(
    rojoFrame,
    text="Rojo, Esperar...",
    fg="red2",
    bg="black",
    font=("Arial", 16)
).place(x=-5, y=155)

img_txt_label_amarilloframe = tk.Label(
    amarilloFrame,
    text="No aceleres...",
    fg="gold",
    bg="black",
    font=("Arial", 16)
).place(x=-5, y=155)



def fuctioExecute():
    global d
    d = 0
    global pulsedBotton
    pulsedBotton = 1
    refresh_color()


def cambio():
    global ve
    global i
    global pulsedBotton
    ex = Faker()
    ip = ex.ipv4()
    if ve == 1:
        verdeFrame.pack(side="right", anchor=tk.N)
        amarilloFrame.forget()
        rojoFrame.forget()
        offFrame.forget()
        ve = 2
        mongoDb.insertCollection("Verde", ip)
        conectionMqqtt.run("Verde", ip)
        return("springGreen2")

    elif ve == 2:

        amarilloFrame.pack(side="right", anchor=tk.N)
        verdeFrame.forget()
        rojoFrame.forget()
        offFrame.forget()
        ve = 3
        mongoDb.insertCollection("Amarrillo", ip)
        conectionMqqtt.run("Amarrillo", ip)
        return("orange")
    elif ve == 3:
        rojoFrame.pack(side="right", anchor=tk.N)
        amarilloFrame.forget()
        verdeFrame.forget()
        offFrame.forget()
        ve = 1
        mongoDb.insertCollection("Rojo", ip)
        conectionMqqtt.run("Rojo", ip)
        return("red2")


img = Image.open('./img/pushBotton.jpeg')
img = img.resize((150, 50))
img = ImageTk.PhotoImage(img)
btn_cambio_appmain = tk.Button(
    appmain,
    image=img,
    font=("Arial 10 bold"),
    fg="dark violet",
    bg="snow",
    cursor="hand2",
    command=fuctioExecute
).place(x=100, y=5)

# Codigoo
style = ttk.Style(appmain)
style.theme_use("clam")
style.configure("Treeview.Heading", background="black", foreground="white")


def table():
    tabla = ttk.Treeview(appmain, columns=('Metros', 'Color', 'Ip'))
    tabla.column("#0", width=80)
    tabla.column('Metros', width=60, anchor=CENTER)
    tabla.column('Color', width=60, anchor=CENTER)
    tabla.column('Ip', width=120, anchor=CENTER)

    tabla.heading("#0", text="Pasos", anchor=CENTER)
    tabla.heading('Metros', text='Metros', anchor=CENTER)
    tabla.heading('Color', text='Color', anchor=CENTER)
    tabla.heading('Ip', text='Ip', anchor=CENTER)

    for i in range(mongoDb.countCollection()):
        datos = mongoDb.getCollection(i)
        tabla.insert("", END, text=datos[0], values=(
            datos[1], datos[2], datos[3]))
    tabla.place(x=40, y=70)
    


after_id = None


def refresh_color():
    global d
    global pulsedBotton
    global after_id
    color = None
    d += 1
    if(pulsedBotton > 0):
        color = cambio()
        if(after_id != None):
            appmain.after_cancel(after_id)
        pulsedBotton = 0
        d = 0
        table()
    if(d == 10):
        color = cambio()
        pulsedBotton = 0
        d = 0
        table()
    after_id = appmain.after(1000, refresh_color)
    pulsedBotton = 0


table()

appmain.mainloop()
