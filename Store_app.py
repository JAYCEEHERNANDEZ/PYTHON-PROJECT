import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def get_connection(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
            return None
        
class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CHELAI STORE COUNTER")
        self.root.state("zoomed")

        self.db = Database('localhost', 'root', 'Hernandez14', 'pydatabase')
        self.sales = Sales(self.db)
        self.product = Product(self.db)
        self.cart = Cart()

        self.setup_ui()

    def setup_ui(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        left_frame = Frame(self.root, bg="#5C5470", width=430, height=600, padx=10, pady=10)
        left_frame.grid(row=0, column=0, sticky="ns")
        left_frame.grid_propagate(False)

        Label(left_frame, text="CHELAI STORE COUNTER", bg="#5C5470", fg="black", font=("Copperplate Gothic Bold", 19, "bold")).grid(row=0, column=0, pady=35, padx= 20)

        Label(left_frame, text="PRODUCT NAME:", bg="#5C5470", fg="black", font=("Kanit", 14)).grid(row=1, column=0, pady=5, sticky="w")
        self.product_field = Entry(left_frame, font=("Kanit", 14), width=25)
        self.product_field.grid(row=2, column=0, pady=5)

        Label(left_frame, text="QUANTITY:", bg="#5C5470", fg="black", font=("Kanit", 14)).grid(row=3, column=0, pady=5, sticky="w")
        self.quantity_field = Entry(left_frame, font=("Kanit", 14), width=25)
        self.quantity_field.grid(row=4, column=0, pady=10)

        Button(left_frame, text="Sales Summary", command=self.show_daily_summary, bg="#DFF2EB", font=("Copperplate Gothic Bold", 14), width=15, height=2).grid(row=9, column=0, pady=30)
        Button(left_frame, text="Add Item", command=self.add_to_cart, bg="#DFF2EB", font=("Copperplate Gothic Bold", 14), width=15, height=2).grid(row=5, column=0, pady=30)
        Button(left_frame, text="Checkout", command=self.process_checkout, bg="#DFF2EB", font=("Copperplate Gothic Bold", 14), width=15, height=2).grid(row=6, column=0, pady=30)
        Button(left_frame, text="View Products", command=self.view_stock, bg="#DFF2EB", font=("Copperplate Gothic Bold", 14), width=15, height=2).grid(row=7, column=0, pady=30)

        right_frame = Frame(self.root, bg="#B9B4C7", padx=10, pady=10)
        right_frame.grid(row=0, column=1, sticky="nsew")

        Label(right_frame, text="ITEM SUMMARY", bg="#B9B4C7", font=("Copperplate Gothic Bold", 16, "bold")).pack(anchor="center", fill="x", pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 14), rowheight=40)
        style.configure("Treeview.Heading", font=("Arial", 16, "bold"))

        columns = ("Product Name", "Quantity", "Price", "Total")
        self.cart_tree = ttk.Treeview(right_frame, columns=columns, show="headings", height=15, style="Treeview")

        for col in columns:
            self.cart_tree.heading(col, text=col)
            self.cart_tree.column(col, anchor="center", width=200)
            self.cart_tree.pack(fill="both", expand=True)

        Button(right_frame, text="REMOVE", command=self.remove_from_cart, bg="#DFF2EB", font=("Copperplate Gothic Bold", 12), width=10, height=2).pack(side="left", pady=10, padx=20)

        self.total_label = Label(right_frame, text="TOTAL: ₱0.00", bg="#B9B4C7", font=("Arial", 16, "bold"))
        self.total_label.pack(anchor="e", pady=10)
        self.total_label.pack(anchor="e", padx=100)

    def add_to_cart(self):
        product_name = self.product_field.get()
        quantity = self.quantity_field.get()
        
        try:
            quantity = int(quantity)
            if quantity <= 0:
                messagebox.showerror("Error", "Please enter a valid quantity.")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity. Please enter a valid number.")
            return

        if not product_name:
            messagebox.showerror("Error", "Please enter a product name.")
            return

        conn = self.db.get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Stocks, Price FROM inventory WHERE Product_Name = %s", (product_name,))
            product = cursor.fetchone()

            if product:
                available_stock, price = product
                if quantity > available_stock:
                    messagebox.showerror("Error", f"Insufficient stock available. Only {available_stock} left.")
                    return

                total_price = price * quantity
                self.cart.add_item(product_name, quantity, price)  # Add item to the cart object

                self.cart_tree.insert("", "end", values=(product_name, quantity, f"₱{price:.2f}", f"₱{total_price:.2f}"))
                
                self.update_total_price()

                self.product_field.delete(0, END)
                self.quantity_field.delete(0, END)

            else:
                messagebox.showerror("Error", "Product not found.")
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error retrieving product data: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_total_price(self):
        self.total_label.config(text=f"TOTAL: ₱{self.cart.total_amount:.2f}")

    def process_checkout(self):
        if self.cart.total_amount == 0:
            messagebox.showinfo("Info", "Cart is empty. Please add items before checkout.")
            return

        payment_amount = None
        while payment_amount is None or payment_amount < self.cart.total_amount:
            try:
                payment_amount = float(simpledialog.askstring("Payment", f"Total: ₱{self.cart.total_amount:.2f}\nEnter payment amount:"))
                if payment_amount < self.cart.total_amount:
                    messagebox.showerror("Error", f"Insufficient payment. Please pay at least ₱{self.cart.total_amount:.2f}.")
            except ValueError:
                messagebox.showerror("Error", "Invalid payment amount. Please enter a valid number.")

        change = payment_amount - self.cart.total_amount
        messagebox.showinfo("Success", f"Payment Successful!\nTotal: ₱{self.cart.total_amount:.2f}\nPaid: ₱{payment_amount:.2f}\nChange: ₱{change:.2f}")

        self.sales.record_sale(self.cart.total_amount)

        for item in self.cart.items:
            self.product.update_stock(item[0], item[1])

        self.cart.clear()

        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)

        self.update_total_price()

    def remove_from_cart(self):
        selected_item = self.cart_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an item to remove.")
            return

        for item in selected_item:
            item_values = self.cart_tree.item(item, "values")
            product_name = item_values[0]
            quantity = int(item_values[1])
            price = float(item_values[2][1:].replace(',', ''))  # Remove the currency symbol and commas

            self.cart.remove_item_by_name(product_name, quantity, price)

            self.cart_tree.delete(item)

            self.update_total_price()

    def view_stock(self):
        stock_window = Toplevel(self.root)
        stock_window.title("Current Stock")
        stock_window.state("zoomed")

        style = ttk.Style()
        style.configure("Treeview.Heading", background="#5C5470", foreground="black", font=('Arial', 14, 'bold'))
        style.configure("Treeview", background="#f9f9f9", foreground="black", rowheight=30)

        columns = ("ID", "Product Name", "Price", "Stock")
        stock_tree = ttk.Treeview(stock_window, columns=columns, show="headings", height=15, style="Treeview")

        for col in columns:
            stock_tree.heading(col, text=col)
            stock_tree.column(col, anchor="center")

        stock_tree.pack(fill="both", expand=True)

        conn = self.db.get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM inventory")
            rows = cursor.fetchall()
            for row in rows:
                stock_tree.insert("", "end", values=row)
        finally:
            cursor.close()
            conn.close()

        def add_product():
            product_name = simpledialog.askstring("Add Product", "                  Enter product name:                  ")
            if product_name is None:
                return
            price = simpledialog.askfloat("Add Product", "                  Enter product price:                  ")
            stock = simpledialog.askinteger("Add Product", "                  Enter product stock:                  ")

            if product_name and price and stock is not None:
                conn = self.db.get_connection()
                if not conn:
                    return

                cursor = conn.cursor()
                try:
                    cursor.execute("INSERT INTO inventory (Product_Name, Price, Stocks) VALUES (%s, %s, %s)",
                                (product_name, price, stock))
                    conn.commit()
                    messagebox.showinfo("Success", "Product added successfully!")
                    stock_tree.insert("", "end", values=(cursor.lastrowid, product_name, price, stock))

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error adding product: {e}")
                finally:
                    cursor.close()
                    conn.close()

        def restock_product():
            product_id = simpledialog.askinteger("Restock Product", "                  Enter product ID to restock:                  ")
            if product_id is None:
                return
            quantity = simpledialog.askinteger("Restock Product", f"             Enter quantity to restock for product ID {product_id}:                  ")

            if quantity is not None and quantity > 0:
                conn = self.db.get_connection()
                if not conn:
                    return

                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE inventory SET Stocks = Stocks + %s WHERE ID = %s", (quantity, product_id))
                    conn.commit()
                    messagebox.showinfo("Success", f"Product ID {product_id} restocked successfully!")

                    for item in stock_tree.get_children():
                        if stock_tree.item(item)["values"][0] == product_id:
                            stock_tree.item(item, values=(product_id, stock_tree.item(item)["values"][1],
                                                        stock_tree.item(item)["values"][2],
                                                        stock_tree.item(item)["values"][3] + quantity))

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error restocking product: {e}")
                finally:
                    cursor.close()
                    conn.close()

        def modify_product():
            product_id = simpledialog.askinteger("Modify Product", "                  Enter product ID to modify:                  ")
            if product_id is None:
                return
            new_price = simpledialog.askfloat("Modify Product", "                  Enter new product price:                  ")

            if new_price is not None:
                conn = self.db.get_connection()
                if not conn:
                    return

                cursor = conn.cursor()
                try:
                    cursor.execute("UPDATE inventory SET Price = %s WHERE ID = %s",
                                (new_price, product_id))

                    messagebox.showinfo("Success", f"Product ID {product_id} modified successfully!")
                    conn.commit()

                    for item in stock_tree.get_children():
                        if stock_tree.item(item)["values"][0] == product_id:
                            stock_tree.item(item, values=(product_id, stock_tree.item(item)["values"][1],
                                                        new_price,
                                                        stock_tree.item(item)["values"][3]))

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error modifying product: {e}")
                finally:
                    cursor.close()
                    conn.close()

        def delete_product():
            product_id = simpledialog.askinteger("Delete Product", "                  Enter product ID to delete:                    ")
            if product_id is None:
                return
            confirm = messagebox.askyesno("Delete Product", f"Are you sure you want to delete product ID {product_id}?")
            if confirm:
                conn = self.db.get_connection()
                if not conn:
                    return

                cursor = conn.cursor()
                try:
                    cursor.execute("DELETE FROM inventory WHERE ID = %s", (product_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"Product ID {product_id} deleted successfully!")

                    for item in stock_tree.get_children():
                        if stock_tree.item(item)["values"][0] == product_id:
                            stock_tree.delete(item)

                except mysql.connector.Error as e:
                    messagebox.showerror("Error", f"Error deleting product: {e}")
                finally:
                    cursor.close()
                    conn.close()

        button_frame = Frame(stock_window, bg="#F2F2F2")
        button_frame.pack(pady=10, anchor="center")

        Button(button_frame, text="Add Product", command=add_product, bg="#DFF2EB", font=("Copperplate Gothic Bold", 12), width=15, height=2).pack(side="left", padx=10)
        Button(button_frame, text="Restock Product", command=restock_product, bg="#DFF2EB", font=("Copperplate Gothic Bold", 12), width=15, height=2).pack(side="left", padx=50)
        Button(button_frame, text="Modify Product", command=modify_product, bg="#DFF2EB", font=("Copperplate Gothic Bold", 12), width=15, height=2).pack(side="left", padx=50)
        Button(button_frame, text="Delete Product", command=delete_product, bg="#DFF2EB", font=("Copperplate Gothic Bold", 12), width=15, height=2).pack(side="left", padx=10)

        stock_window.mainloop()

    def show_daily_summary(self):
        summary_window = Toplevel(self.root)
        summary_window.title("Daily Sales Summary")
        summary_window.state("zoomed")

        columns = ("Sale ID", "Total Amount", "Date/Time")
        sales_tree = ttk.Treeview(summary_window, columns=columns, show="headings", height=15)

        for col in columns:
            sales_tree.heading(col, text=col)
            sales_tree.column(col, anchor="center", width=150)

        sales_tree.pack(fill="both", expand=True)

        total_sales_label = Label(summary_window, text="Total Sales: $0.00", font=("Arial", 14, "bold"))
        total_sales_label.pack(pady=5)

        def show_all_sales():
            total_sales = 0.0
            for row in sales_tree.get_children():
                sales_tree.delete(row)

            conn = self.db.get_connection()
            if not conn:
                return

            cursor = conn.cursor()
            try:
                query = "SELECT sale_id, total_amount, timestamp FROM sales"
                cursor.execute(query)

                sales_data = cursor.fetchall()

                if not sales_data:
                    sales_tree.insert("", "end", values=("No sales recorded", "", ""))
                else:
                    for row in sales_data:
                        sale_id = row[0]
                        total_amount = row[1]
                        timestamp = row[2]
                        formatted_amount = f"{total_amount:.2f}"

                        total_sales += total_amount

                        sales_tree.insert("", "end", values=(sale_id, formatted_amount, timestamp))

                total_sales_label.config(text=f"Total Sales: ${total_sales:.2f}")

            except mysql.connector.Error as e:
                messagebox.showerror("Error", f"Error retrieving sales: {e}")
            finally:
                cursor.close()
                conn.close()

        show_all_button = Button(summary_window, text="Show All Sales", command=show_all_sales, bg="#DFF2EB", font=("Copperplate Gothic Bold", 10), width=15, height=2)
        show_all_button.pack(pady=20)

        today = datetime.now().date()
        total_sales = 0.0

        conn = self.db.get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            query = "SELECT sale_id, total_amount, timestamp FROM sales WHERE DATE(timestamp) = %s"
            cursor.execute(query, (today,))

            sales_data = cursor.fetchall()

            if not sales_data:
                sales_tree.insert("", "end", values=("No sales recorded for today", "", ""))
            else:
                for row in sales_data:
                    sale_id = row[0]
                    total_amount = row[1]
                    timestamp = row[2]
                    formatted_amount = f"{total_amount:.2f}"

                    total_sales += total_amount

                    sales_tree.insert("", "end", values=(sale_id, formatted_amount, timestamp))

            total_sales_label.config(text=f"Total Sales: ${total_sales:.2f}")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error retrieving sales: {e}")
        finally:
            cursor.close()
            conn.close()

class Sales:
    def __init__(self, db):
        self.db = db

    def get_daily_sales(self):
        today = datetime.now().date()
        conn = self.db.get_connection()
        if not conn:
            return []

        cursor = conn.cursor()
        try:
            query = "SELECT sale_id, total_amount, timestamp FROM sales WHERE DATE(timestamp) = %s"
            cursor.execute(query, (today,))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()

    def record_sale(self, total_amount):
        conn = self.db.get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            timestamp = datetime.now()
            cursor.execute("INSERT INTO sales (total_amount, timestamp) VALUES (%s, %s)", (total_amount, timestamp))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

class Product:
    def __init__(self, db):
        self.db = db

    def get_product(self, product_name):
        conn = self.db.get_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT Stocks, Price FROM inventory WHERE Product_Name = %s", (product_name,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()

    def update_stock(self, product_name, quantity):
        conn = self.db.get_connection()
        if not conn:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE inventory SET Stocks = Stocks - %s WHERE Product_Name = %s", (quantity, product_name))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

class Cart:
    def __init__(self):
        self.items = []
        self.total_amount = 0.0

    def add_item(self, product_name, quantity, price):
        total_price = price * quantity
        self.items.append((product_name, quantity, price, total_price))
        self.total_amount += total_price

    def remove_item_by_name(self, product_name, quantity, price):
        for index, item in enumerate(self.items):
            if item[0] == product_name and item[1] == quantity and item[2] == price:
                self.total_amount -= item[3]
                del self.items[index]
                break

    def clear(self):
        self.items.clear()
        self.total_amount = 0.0

if __name__ == "__main__":
    root = Tk()
    app = StoreApp(root)
    root.mainloop()