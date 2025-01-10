import tkinter as tk
from tkinter import messagebox

# Data structure for items
items = {
    "item1": {"name": "Pen", "price": 10},
    "item2": {"name": "Notebook", "price": 50},
    "item3": {"name": "Eraser", "price": 5},
}

class BillingSystemApp:
    def __init__(self, root):  # Corrected __init__
        self.root = root
        self.root.title("Billing System")
        self.root.geometry("600x400")
        self.selected_items = {}
        
        self.create_widgets()

    def create_widgets(self):
        # Title
        tk.Label(self.root, text="Billing System", font=("Arial", 20)).pack(pady=10)

        # Add Item Section
        self.add_item_frame = tk.Frame(self.root)
        self.add_item_frame.pack(pady=10)

        tk.Label(self.add_item_frame, text="Add New Item", font=("Arial", 14)).grid(row=0, column=0, columnspan=2)

        tk.Label(self.add_item_frame, text="Item Name:").grid(row=1, column=0, pady=5, sticky=tk.W)
        self.new_item_name = tk.Entry(self.add_item_frame)
        self.new_item_name.grid(row=1, column=1, pady=5)

        tk.Label(self.add_item_frame, text="Item Price (₹):").grid(row=2, column=0, pady=5, sticky=tk.W)
        self.new_item_price = tk.Entry(self.add_item_frame)
        self.new_item_price.grid(row=2, column=1, pady=5)

        tk.Button(self.add_item_frame, text="Add Item", command=self.add_item).grid(row=3, column=0, columnspan=2, pady=10)

        # Available Items Section
        self.items_frame = tk.Frame(self.root)
        self.items_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.update_items_display()

        # Total Calculation Section
        self.total_frame = tk.Frame(self.root)
        self.total_frame.pack(pady=10)

        tk.Button(self.total_frame, text="Calculate Total", command=self.calculate_total).pack(side=tk.LEFT, padx=5)
        tk.Label(self.total_frame, text="Total: ₹", font=("Arial", 12)).pack(side=tk.LEFT)
        self.total_label = tk.Label(self.total_frame, text="0", font=("Arial", 12))
        self.total_label.pack(side=tk.LEFT)

    def update_items_display(self):
        # Clear the items frame
        for widget in self.items_frame.winfo_children():
            widget.destroy()

        # Display Available Items
        tk.Label(self.items_frame, text="Available Items", font=("Arial", 14)).pack(pady=10)
        self.items_list_frame = tk.Frame(self.items_frame)
        self.items_list_frame.pack()

        for item_id, item in items.items():
            frame = tk.Frame(self.items_list_frame)
            frame.pack(fill=tk.X, pady=5)

            tk.Label(frame, text=f"{item['name']} - ₹{item['price']}", width=30, anchor=tk.W).pack(side=tk.LEFT)
            
            quantity = tk.Entry(frame, width=5)
            quantity.insert(0, "0")
            quantity.pack(side=tk.LEFT, padx=5)
            self.selected_items[item_id] = quantity

            tk.Button(frame, text="Edit Price", command=lambda i=item_id: self.edit_price(i)).pack(side=tk.LEFT)

    def add_item(self):
        name = self.new_item_name.get().strip()
        price = self.new_item_price.get().strip()

        if not name or not price:
            messagebox.showerror("Error", "Both fields are required!")
            return

        try:
            price = int(price)
            item_id = f"item{len(items) + 1}"
            items[item_id] = {"name": name, "price": price}
            messagebox.showinfo("Success", "Item added successfully!")
            self.update_items_display()
            self.new_item_name.delete(0, tk.END)
            self.new_item_price.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number!")

    def edit_price(self, item_id):
        def save_price():
            new_price = price_entry.get().strip()
            if not new_price:
                messagebox.showerror("Error", "Price cannot be empty!")
                return
            try:
                new_price = int(new_price)
                items[item_id]["price"] = new_price
                messagebox.showinfo("Success", "Price updated successfully!")
                edit_window.destroy()
                self.update_items_display()
            except ValueError:
                messagebox.showerror("Error", "Price must be a number!")

        # Edit Price Window
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Price")
        edit_window.geometry("300x150")

        tk.Label(edit_window, text=f"Edit Price for {items[item_id]['name']}", font=("Arial", 12)).pack(pady=10)
        price_entry = tk.Entry(edit_window)
        price_entry.insert(0, items[item_id]["price"])
        price_entry.pack(pady=10)

        tk.Button(edit_window, text="Save", command=save_price).pack(pady=10)

    def calculate_total(self):
        total = 0
        for item_id, quantity_entry in self.selected_items.items():
            try:
                quantity = int(quantity_entry.get().strip())
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
                total += items[item_id]["price"] * quantity
            except ValueError:
                messagebox.showerror("Error", f"Invalid quantity for {items[item_id]['name']}. Please enter a valid number.")
                return
        self.total_label.config(text=str(total))


if __name__ == "__main__":  # Corrected __name__ check
    root = tk.Tk()
    app = BillingSystemApp(root)
    root.mainloop()
