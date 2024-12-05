import tkinter as tk
from compress import compress, decompress
from tkinter import filedialog

def compress_text(input_file, output_file):
    try:   
        compress(input_file, output_file)
    except Exception:
        input_entry.insert(0, Exception)

def decompress_text(input_file, output_file):
    try:   
        decompress(input_file, output_file)
    except Exception:
        input_entry.insert(0, Exception)
    
def get_file():
    filename = filedialog.askopenfilename(initialdir="./", title="Select the file to compress")
    input_entry.insert(0, filename)

window = tk.Tk()
window.title("Compression App")
window.geometry("600x600")

input_text = tk.Label(window, text="Enter Input File path")
input_entry = tk.Entry(window)

output_text = tk.Label(window, text="Enter Output File path")
output_entry = tk.Entry(window)

input_file_button = tk.Button(window, text="...", command=get_file)
compress_button = tk.Button(window, text="Compress", 
                            command=lambda: compress_text(input_entry.get(), output_entry.get()))
decompress_button = tk.Button(window, text="Decompress", 
                              command=lambda: decompress_text(input_entry.get(), output_entry.get()))


input_text.grid(row=2, column=1)
input_entry.grid(row=2, column=2)#, columnspan=20)
input_file_button.grid(row=2, column=3)
output_text.grid(row=3, column=1)
output_entry.grid(row=3, column=2)#, columnspan=20)
compress_button.grid(row=4, column = 1)
decompress_button.grid(row=4, column = 2)


window.mainloop()