from tkinter import *
from fpdf import FPDF

class InvoiceGenerator:
    """
    A GUI application to generate a pdf invoice for a pharmacy by selecting
    medicines and their quantity. The invoice is saved to a local folder
    """
    def __init__(self):
        self.medicine_price = {
            "Medicine A": 40.0,
            "Medicine B": 20.0,
            "Medicine C": 30.0,
            "Medicine D": 25.0,
            "Medicine E": 50.0
            }

        self.invoice_items = []
        self.total_amount = 0.0
        self.pdf = FPDF()
        self.filepath = "invoice_generator/invoice.pdf"

        # Declare the gui
        self.window = Tk()
        self.window.title("Invoice Generator")
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the main app window"""
        self.medicine_label = Label(self.window, text="Select medicine: ")
        self.medicine_label.pack()


        self.medicine_list = Listbox(self.window, selectmode="single")
        self.medicine_list.pack()


        for medicine in self.medicine_price.keys():
            self.medicine_list.insert(END, medicine)

        self.quantity_label = Label(self.window, text="Enter Quantity: ")
        self.quantity_label.pack()

        self.quantity_entry = Entry(self.window)
        self.quantity_entry.pack()


        self.total_button = Button(self.window, text="Add medicine", command=self.add_medicine)
        self.total_button.pack()

        self.total_label = Label(self.window, text="Total Amount: ")
        self.total_label.pack()

        self.total_entry = Entry(self.window)
        self.total_entry.pack()

        self.customer_label = Label(self.window, text="Customer Name: ")
        self.customer_label.pack()

        self.customer_entry = Entry(self.window)
        self.customer_entry.pack()

        self.invoice_button = Button(self.window, text="Generate Invoice", 
                                     command=self.generate_invoice)
        self.invoice_button.pack()

        self.invoice_text = Text(self.window, height=10, width=50)
        self.invoice_text.pack()

    def add_medicine(self):
        """Functionality to add medicines to the invoice along with quantity and amount"""
        if not self.medicine_list.curselection():
            self.total_entry.delete(0, END)
            self.total_entry.insert(END, "Select Medicine")
            return
        
        if not self.quantity_entry.get():
            self.total_entry.delete(0, END)
            self.total_entry.insert(END, "Enter Quantity")
            return 
        
        try:
            Q = int(self.quantity_entry.get())
            medicine = self.medicine_list.get(ANCHOR)
            P = self.medicine_price[medicine]
            amount = P * Q
            self.invoice_items.append((medicine, Q, amount))
            self.total_entry.delete(0, END)
            self.total_entry.insert(END, str(self.calculate_total()))
            self.update_invoice_text()

        except Exception as e:
            self.total_entry.delete(0, END)
            self.total_entry.insert(END, e)

    def update_invoice_text(self):
        """Show the selected medicines and details in the invoice text at the bottom"""
        self.invoice_text.delete(1.0, END)
        for medicine in self.invoice_items:
            self.invoice_text.insert(
                END, 
                f"Medicine: {medicine[0]}, Quantity: {medicine[1]}, Amount: {medicine[2]} \n")

    def calculate_total(self):
        """Calculate total amount"""
        for medicine in self.invoice_items:
            self.total_amount += int(medicine[2])
        return self.total_amount
            
    def generate_invoice(self):
        """Generate the PDF invoice"""
        # Return empty pdf if there are no items in the invoice
        if len(self.invoice_items) == 0:
            self.show_error(f"Please select medicines")
            return
        
        # Show error if customer name is missing
        if self.customer_entry.get():
            customer_name = self.customer_entry.get()
        else:
            self.show_error(f"Please enter customer name")
            return
        
        # Update PDF if the invoice contains some items
        self.pdf.set_font("times", size = 12)

        self.pdf.add_page()
        self.pdf.cell(0, 10, text="Invoice", new_x="LMARGIN", new_y="NEXT", align="C")
        self.pdf.cell(text=f"Customer: {customer_name}", new_x="LMARGIN", 
                new_y="NEXT", align="L")
        self.pdf.ln()
        # table = pdf.table()
        # for row in table.row()
        for medicine in self.invoice_items:
            self.pdf.cell(0, 10, 
                    text=f"Medicine: {medicine[0]}, Quantity: {medicine[1]}, Amount: {medicine[2]}",
                    new_x="LMARGIN", new_y="NEXT", align="L")
        
        # Add total amount to PDF
        self.pdf.cell(0, 10, text="Total Amount: " +
                str(self.calculate_total()), new_x="LMARGIN", new_y="NEXT", align="L")
    
        self.pdf.output(self.filepath)

    def show_error(self, message):
        self.error_label = Label(self.window, text=message)
        self.error_label.pack()

    def run(self):
        """Run the main event loop for the GUI"""
        self.window.mainloop()

if __name__ == "__main__":
    invoice = InvoiceGenerator()
    invoice.run()
    