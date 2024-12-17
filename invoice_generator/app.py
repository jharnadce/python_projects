import json
from tkinter import Tk, Label, Entry, Listbox, Text, Button, END, ANCHOR
from fpdf import FPDF
import os


class Medicine:
    """Handle properties of medicines"""
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Config:
    """Handle config items"""
    def __init__(self, config_file) -> None:
        try:
            with open(config_file, "r") as file:
                self.config = json.load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file {config_file} not fount")
        except json.JSONDecodeError:
            raise Exception(f"Configuration file {config_file} is not a valid json")
        
    def get(self, key, default=None):
        self.config.get(key, default)


class Invoice:
    """Handles invoice related attributes like items and amounts and 
    invoice methods like add items to invoice and generate invoice"""
    def __init__(self):
        self.items = []
        self.total_amount = 0.0

    def add_item(self, medicine, quantity):
        amount = medicine.price * quantity
        self.items.append({"medicine": medicine, 
                           "quantity": quantity, 
                           "amount": amount})
        self.total_amount += amount

    def generate_pdf(self, name, filepath):
        try:
            pdf = FPDF()
            pdf.set_font("times", size = 12)

            pdf.add_page()
            pdf.cell(0, 10, text="Invoice", new_x="LMARGIN", new_y="NEXT", align="C")
            pdf.cell(text=f"Customer: {name}", new_x="LMARGIN", 
                    new_y="NEXT", align="L")
            pdf.ln()
            
            for item in self.items:
                medicine, quantity, amount = item['medicine'].name, item['quantity'], item['amount']
                self.pdf.cell(0, 10, 
                        text=f"Medicine: {medicine}, Quantity: {quantity}, Amount: {amount}",
                        new_x="LMARGIN", new_y="NEXT", align="L")
            
            # Add total amount to PDF
            self.pdf.cell(0, 10, text="Total Amount: " +
                    str(self.total_amount), new_x="LMARGIN", new_y="NEXT", align="L")
        
            self.pdf.output(filepath)
        except Exception as e:
            raise Exception(f"Failed to generate invoice: {e}")


class InvoiceAppGUI:
    def __init__(self, config_file) -> None:
        self.config = Config(config_file)
        
        self.medicines = [
            Medicine(name, price) for name, price in self.config.config.get("medicines", {}).items()
            ]
        self.filepath = self.config.config.get("invoice_pdf_path", "invoice.pdf")
        self.invoice = Invoice()

        self.window = Tk()
        self.window.title("Invoice Generator")
        self.setup_gui()

    def setup_gui(self):
        Label(self.window, text="Select medicine: ").pack()

        self.medicine_list = Listbox(self.window, selectmode="single")
        self.medicine_list.pack()
        for medicine in self.medicines:
            self.medicine_list.insert(END, medicine.name)

        Label(self.window, text="Enter Quantity: ").pack()

        self.quantity_entry = Entry(self.window)
        self.quantity_entry.pack()

        Button(self.window, text="Add medicine", command=self.add_medicine).pack()

        Label(self.window, text="Total Amount: ").pack()

        self.total_entry = Entry(self.window)
        self.total_entry.pack()

        Label(self.window, text="Customer Name: ").pack()

        self.customer_entry = Entry(self.window)
        self.customer_entry.pack()

        Button(self.window, text="Generate Invoice", 
                                     command=self.generate_invoice).pack()

        self.invoice_text = Text(self.window, height=10, width=50)
        self.invoice_text.pack()


    def add_medicine(self):
        try:
            selected_index = self.medicine_list.curselection()
            if not selected_index:
                raise ValueError("Please select a medicine")
            
            quantity = self.quantity_entry.get().strip()
            if not quantity.isdigit() or int(quantity) <= 0:
                raise ValueError("Quantity must be a positive integer")
            
            print(selected_index)
            medicine = self.medicines[selected_index[0]]
            self.invoice.add_item(medicine, int(quantity))
            print(self.invoice.items)
            self.update_invoice_text()
        except ValueError as e:
            self.showerror(str(e))
        except Exception as e:
            self.showerror(f"Unexpected Error: {e}")

    def update_invoice_text(self):
        try:
            self.invoice_text.delete(1.0, END)
            for item in self.invoice.items:
                self.invoice_text.insert(END, 
                                        f"Medicine: {item['medicine'].name}, Quantity: {item['quantity']}, Amount: {item['amount']}\n")
            self.invoice_text.insert(END,
                                     f"Total amount: {self.invoice.total_amount}")
        except Exception as e:
            self.showerror(f"Error updating invoice text: {e}")


    def generate_invoice(self):
        customer_name = self.customer_entry.get().strip()
        if not customer_name:
            self.showerror("Customer name cannot be empty")

        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            self.invoice.generate_pdf(customer_name, self.filepath)
            self.showerror(f"Invoice saved to {self.filepath}")
        except Exception as e:
            self.showerror(f"Error generating invoice: {e}")

    def run(self):
        self.window.mainloop()

    def showerror(self, message):
        Label(self.window, text=message, fg="red").pack()
    

if __name__ == "__main__":
    CONFIG_FILE = "invoice_generator/config.json"
    try:
        app = InvoiceAppGUI(CONFIG_FILE)
        app.run()
    except Exception as e:
        print(f"Application error: {e}")