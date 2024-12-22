import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry


# Database setup
def setup_database():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    # Check if the column exists and add it if not
    c.execute("PRAGMA table_info(products)")
    columns = [col[1] for col in c.fetchall()]
    if "date_added" not in columns:
        c.execute("ALTER TABLE products ADD COLUMN date_added TEXT NOT NULL DEFAULT '2024-01-01'")
    conn.commit()
    conn.close()


def add_product_to_db(name, quantity, price, date_added):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, quantity, price, date_added) VALUES (?, ?, ?, ?)",
              (name, quantity, price, date_added))
    conn.commit()
    conn.close()


def view_products_from_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()
    return products


def delete_product_from_db(product_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id=?", (product_id,))
    conn.commit()
    conn.close()


def update_product_in_db(product_id, name, quantity, price, date_added):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute("UPDATE products SET name=?, quantity=?, price=?, date_added=? WHERE id=?",
              (name, quantity, price, date_added, product_id))
    conn.commit()
    conn.close()


# GUI Functions
def add_product():
    def save_product():
        name = entry_name.get()
        quantity = entry_quantity.get()
        price = entry_price.get()
        date_added = entry_date.get()

        if not name or not quantity or not price or not date_added:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            quantity = int(quantity)
            price = float(price)
            add_product_to_db(name, quantity, price, date_added)
            messagebox.showinfo("Success", "Product added successfully!")
            top.destroy()
            refresh_table()
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or price!")

    top = Toplevel()
    top.title("Add Product")
    top.configure(bg="#3e8e41")  # Background color of the window

    # Labels and entry widgets
    Label(top, text="Product Name", bg="#3e8e41", fg="white").grid(row=0, column=0, padx=10, pady=10)
    entry_name = Entry(top)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    Label(top, text="Quantity", bg="#3e8e41", fg="white").grid(row=1, column=0, padx=10, pady=10)
    entry_quantity = Entry(top)
    entry_quantity.grid(row=1, column=1, padx=10, pady=10)

    Label(top, text="Price", bg="#3e8e41", fg="white").grid(row=2, column=0, padx=10, pady=10)
    entry_price = Entry(top)
    entry_price.grid(row=2, column=1, padx=10, pady=10)

    Label(top, text="Date Added", bg="#3e8e41", fg="white").grid(row=3, column=0, padx=10, pady=10)
    entry_date = DateEntry(top, date_pattern='yyyy-mm-dd', background='darkblue', foreground='white', borderwidth=2)
    entry_date.grid(row=3, column=1, padx=10, pady=10)

    # Button with interactive color
    Button(top, text="Save", command=save_product, bg="#4CAF50", fg="white", activebackground="#45a049",
           activeforeground="white").grid(row=4, column=0, columnspan=2, pady=20)


def delete_product():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a product to delete!")
        return

    product_id = tree.item(selected_item)["values"][0]
    delete_product_from_db(product_id)
    messagebox.showinfo("Success", "Product deleted successfully!")
    refresh_table()


def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    products = view_products_from_db()
    for product in products:
        tree.insert("", "end", values=product)


# Main Window
def main_window():
    global tree
    setup_database()

    root = Tk()
    root.title("Inventory Management System")
    root.geometry("800x500")
    root.configure(bg="#3e8e41")  # Background color for the main window

    # Title label
    title_label = Label(root, text="Inventory Management System", font=("Arial", 20), bg="#3e8e41", fg="white")
    title_label.pack(pady=20)

    # Table
    columns = ("ID", "Name", "Quantity", "Price", "Date Added")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Price", text="Price")
    tree.heading("Date Added", text="Date Added")

    # Center align the column content
    for col in columns:
        tree.column(col, anchor="center")

    tree.pack(fill=BOTH, expand=True)

    refresh_table()

    # Buttons with interactive color
    frame = Frame(root, bg="#3e8e41")
    frame.pack(pady=20)

    Button(frame, text="Add Product", command=add_product, bg="#4CAF50", fg="white", activebackground="#45a049",
           activeforeground="white").grid(row=0, column=0, padx=10)
    Button(frame, text="Delete Product", command=delete_product, bg="#f44336", fg="white", activebackground="#e53935",
           activeforeground="white").grid(row=0, column=1, padx=10)

    root.mainloop()


if __name__ == "__main__":
    main_window()
