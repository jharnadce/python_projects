import tkinter as tk
import bcrypt

def match_password(user):
    # The below 2 lines will ideally be executed in a different script 
    # to generate the original hash
    actual_password = b'myPassword'
    actual_hashvalue = bcrypt.hashpw(actual_password, bcrypt.gensalt())

    # convert user value to bytes
    user_bytes = bytes(user, encoding='utf-8')
    # check hash against actual hash value
    
    if bcrypt.checkpw(user_bytes, actual_hashvalue):
        print("Login Successful")
    else:
        print("Invalid Password")


window = tk.Tk()

window.title("Log in here")
window.geometry("300x300")
label = tk.Label(window, text="Enter password")
password_entry = tk.Entry(window)
login_button = tk.Button(window, text="Log In", command=lambda: match_password(password_entry.get()))

label.grid(row=1, column=1)
password_entry.grid(row=1, column=2)
login_button.grid(row=2, column=2)

window.mainloop()