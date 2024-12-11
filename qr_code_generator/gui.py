from tkinter import *
import pyqrcode
from PIL import Image, ImageTk

# packages to be installed pyqrcode, pillow, pypng

def generate_code():
    link_name = name_entry.get()
    link = link_entry.get()
    file_name = link_name + ".png"
    # create qr code for the link
    url = pyqrcode.create(link)
    # convert the qr code to png file and saved it in local directory
    url.png(file_name, scale=8) 
    # read the qr code's png image using imageTk
    image = ImageTk.PhotoImage(Image.open(file_name))
    # Add the image to the canvas as a label
    image_label = Label(image=image)
    image_label.image = image
    canvas.create_window(200, 440, window=image_label)  


root = Tk()

canvas = Canvas(root, width=400, height=600)
canvas.pack()

title = Label(root, text="QR Code Generator", fg="green", font=("Arial", 30))
canvas.create_window(200, 50, window=title)

name_label = Label(root, text="Enter Link Name")
link_label = Label(root, text="Enter Link URL")
name_entry = Entry(root)
link_entry = Entry(root)
generate_button = Button(root, text="Generate QR Code", command=generate_code)
canvas.create_window(200, 100, window=name_label)
canvas.create_window(200, 130, window=name_entry)
canvas.create_window(200, 160, window=link_label)
canvas.create_window(200, 190, window=link_entry)
canvas.create_window(200, 240, window=generate_button)


root.mainloop()