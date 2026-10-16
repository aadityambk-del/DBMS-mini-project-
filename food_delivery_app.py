import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# Database connection function
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pass@123",
            # Must match the database created by food_delivery.sql.
            database="aaditya"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Connection Error", f"Error connecting to database: {e}")
        return None

# Main application class
class FoodDeliveryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Food Delivery System")
        self.root.geometry("900x700")
        
        # Apply modern ttk theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TButton', padding=6, relief="flat", background="#e0e0e0")
        self.style.configure('Heading.TLabel', font=('Segoe UI', 16, 'bold'), foreground="#333333")

        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title Label
        ttk.Label(main_frame, text="Online Food Delivery Management", style='Heading.TLabel').pack(pady=(0, 15))
        ttk.Label(main_frame, text="Select a Table to Manage:", font=('Segoe UI', 11)).pack(anchor=tk.W, pady=(0, 10))

        # Canvas and Scrollbar for buttons in case window is small
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.canvas = tk.Canvas(canvas_frame, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons to manage tables
        self.manage_buttons = {
            "Customers": self.manage_customers,
            "Restaurants": self.manage_restaurants,
            "Delivery Agents": self.manage_delivery_agents,
            "Food Items": self.manage_food,
            "Hands Out": self.manage_hands_out,
            "Carts": self.manage_carts,
            "Offers": self.manage_offers,
            "Reviews": self.manage_reviews,
            "Payments": self.manage_payments,
            "Online Payments": self.manage_online,
            "Offline Payments": self.manage_offline,
            "Bills": self.manage_bills,
            "Customer Care": self.manage_customer_care
        }

        for table_name, action in self.manage_buttons.items():
            btn = ttk.Button(self.scrollable_frame, text=f"Manage {table_name}", command=action, width=30)
            btn.pack(pady=4, anchor="w")

    def manage_customers(self):
        self.manage_table("Customer", ["c_id", "c_fullname", "c_address", "c_mobileno"])

    def manage_restaurants(self):
        self.manage_table("Restaurant", ["r_regino", "r_gstino", "r_mobileno", "r_address", "c_id"])

    def manage_delivery_agents(self):
        self.manage_table("Delivery_Agent", ["da_contactno", "da_id", "da_tracking", "da_otp", "r_regino"])

    def manage_food(self):
        self.manage_table("Food", ["f_no", "f_description", "f_type", "f_pricefilter", "c_id", "da_contactno"])

    def manage_hands_out(self):
        self.manage_table("Hands_Out", ["r_regino", "f_no"], key_count=2)

    def manage_carts(self):
        self.manage_table("Cart", ["ca_no", "ca_addon", "ca_totalprice", "ca_type", "c_id"])

    def manage_offers(self):
        self.manage_table("Offers", ["o_coupon", "o_rewardpoints", "o_premium", "o_discount", "c_id", "ca_no"])

    def manage_reviews(self):
        self.manage_table("Review", ["c_id", "r_regino", "r_stars", "r_message"], key_count=2)

    def manage_payments(self):
        self.manage_table("Payment", ["p_upiid", "p_mode", "p_cod", "p_wallet", "c_id"])

    def manage_online(self):
        self.manage_table("Online", ["p_upiid", "gpay"])

    def manage_offline(self):
        self.manage_table("Offline", ["p_upiid", "cash"])

    def manage_bills(self):
        self.manage_table("Bill", ["b_no", "b_date", "b_amt", "b_time", "ca_no", "p_upiid"])

    def manage_customer_care(self):
        self.manage_table("Customer_Care", ["cc_email", "cc_refund", "cc_complaint", "cc_paymentissue", "c_id", "da_contactno"])

    def manage_table(self, table_name, columns, key_count=1):
        table_window = tk.Toplevel(self.root)
        table_window.title(f"Manage {table_name}")
        table_window.geometry("850x600")
        main_container = ttk.Frame(table_window, padding=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Treeview frame with scrollbars
        tree_frame = ttk.Frame(main_container)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="w")

        tree.grid(row=0, column=0, sticky="nsew")
        tree_scroll_y.grid(row=0, column=1, sticky="ns")
        tree_scroll_x.grid(row=1, column=0, sticky="ew")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        keys = columns[:key_count]

        # Action buttons frame
        action_frame = ttk.LabelFrame(main_container, text=" Actions ", padding=10)
        action_frame.pack(fill=tk.X, pady=5)

        ttk.Button(action_frame, text="Insert", command=lambda: self.show_insert_fields(main_container, table_name, columns, tree)).pack(side=tk.LEFT, padx=5, expand=True)
        ttk.Button(action_frame, text="Update", command=lambda: self.show_update_fields(main_container, table_name, columns, keys, tree)).pack(side=tk.LEFT, padx=5, expand=True)
        ttk.Button(action_frame, text="Delete", command=lambda: self.show_delete_fields(main_container, table_name, keys, tree)).pack(side=tk.LEFT, padx=5, expand=True)
        ttk.Button(action_frame, text="Retrieve", command=lambda: self.show_retrieve_fields(main_container, table_name, columns, keys)).pack(side=tk.LEFT, padx=5, expand=True)

        self.view_all_data(tree, table_name)

    def clear_dynamic_frames(self, container):
        for widget in container.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.cget("text") not in [" Actions "]:
                widget.destroy()

    def show_insert_fields(self, container, table_name, columns, tree):
        self.clear_dynamic_frames(container)
        insert_frame = ttk.LabelFrame(container, text=" Insert New Record ", padding=10)
        insert_frame.pack(fill=tk.X, pady=10)

        entries = []
        grid_frame = ttk.Frame(insert_frame)
        grid_frame.pack(fill=tk.X, pady=5)

        for i, col in enumerate(columns):
            row = i // 2
            col_idx = (i % 2) * 2
            ttk.Label(grid_frame, text=f"{col}:").grid(row=row, column=col_idx, sticky=tk.W, padx=5, pady=3)
            entry = ttk.Entry(grid_frame, width=25)
            entry.grid(row=row, column=col_idx+1, sticky=tk.W, padx=5, pady=3)
            entries.append(entry)

        def add_record():
            filled = [(col, entry.get()) for col, entry in zip(columns, entries) if entry.get() != ""]
            cols = [c for c, v in filled]
            values = [v for c, v in filled]
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({', '.join(['%s'] * len(cols))})", values)
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Record added successfully.")
                    self.view_all_data(tree, table_name)
                    insert_frame.destroy()
                except mysql.connector.IntegrityError as err:
                    messagebox.showerror("Error", f"Duplicate entry or integrity error: {err}")
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        btn_frame = ttk.Frame(insert_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Save Record", command=add_record).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=insert_frame.destroy).pack(side=tk.RIGHT, padx=5)

    def show_update_fields(self, container, table_name, columns, keys, tree):
        self.clear_dynamic_frames(container)
        update_frame = ttk.LabelFrame(container, text=" Update Record ", padding=10)
        update_frame.pack(fill=tk.X, pady=10)

        entries = []
        grid_frame = ttk.Frame(update_frame)
        grid_frame.pack(fill=tk.X, pady=5)

        for i, col in enumerate(columns):
            row = i // 2
            col_idx = (i % 2) * 2
            lbl_text = f"{col} (Key):" if col in keys else f"{col}:"
            ttk.Label(grid_frame, text=lbl_text).grid(row=row, column=col_idx, sticky=tk.W, padx=5, pady=3)
            entry = ttk.Entry(grid_frame, width=25)
            entry.grid(row=row, column=col_idx+1, sticky=tk.W, padx=5, pady=3)
            entries.append(entry)

        def update_record():
            values = [entry.get() or None for entry in entries]
            n = len(keys)
            conn = create_connection()
            if conn:
                try:
                    set_part = ", ".join([f"{col} = %s" for col in columns[n:]])
                    where_part = " AND ".join([f"{k} = %s" for k in keys])
                    update_stmt = f"UPDATE {table_name} SET {set_part} WHERE {where_part}"
                    cursor = conn.cursor()
                    cursor.execute(update_stmt, values[n:] + values[:n])
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Record updated successfully.")
                    self.view_all_data(tree, table_name)
                    update_frame.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        btn_frame = ttk.Frame(update_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Save Changes", command=update_record).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=update_frame.destroy).pack(side=tk.RIGHT, padx=5)

    def show_delete_fields(self, container, table_name, keys, tree):
        self.clear_dynamic_frames(container)
        delete_frame = ttk.LabelFrame(container, text=" Delete Record ", padding=10)
        delete_frame.pack(fill=tk.X, pady=10)

        key_entries = []
        grid_frame = ttk.Frame(delete_frame)
        grid_frame.pack(fill=tk.X, pady=5)

        for i, k in enumerate(keys):
            ttk.Label(grid_frame, text=f"Enter {k}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            entry = ttk.Entry(grid_frame, width=30)
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)
            key_entries.append(entry)

        def delete_record():
            key_values = [entry.get() for entry in key_entries]
            if not all(key_values):
                messagebox.showerror("Error", "Please fill in all key fields to delete.")
                return

            conn = create_connection()
            if conn:
                try:
                    where_part = " AND ".join([f"{k} = %s" for k in keys])
                    cursor = conn.cursor()
                    cursor.execute(f"DELETE FROM {table_name} WHERE {where_part}", key_values)
                    conn.commit()
                    label = ", ".join([f"{k} = {v}" for k, v in zip(keys, key_values)])
                    if cursor.rowcount == 0:
                        messagebox.showinfo("Not Found", "No record found with the provided key(s).")
                    else:
                        messagebox.showinfo("Success", f"Record with {label} deleted successfully.")
                    conn.close()
                    self.view_all_data(tree, table_name)
                    delete_frame.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        btn_frame = ttk.Frame(delete_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Delete", command=delete_record).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=delete_frame.destroy).pack(side=tk.RIGHT, padx=5)

    def show_retrieve_fields(self, container, table_name, columns, keys):
        self.clear_dynamic_frames(container)
        retrieve_frame = ttk.LabelFrame(container, text=" Retrieve Record ", padding=10)
        retrieve_frame.pack(fill=tk.X, pady=10)

        key_entries = []
        grid_frame = ttk.Frame(retrieve_frame)
        grid_frame.pack(fill=tk.X, pady=5)

        for i, k in enumerate(keys):
            ttk.Label(grid_frame, text=f"Enter {k}:").grid(row=i, column=0, sticky=tk.W, padx=5, pady=3)
            entry = ttk.Entry(grid_frame, width=30)
            entry.grid(row=i, column=1, sticky=tk.W, padx=5, pady=3)
            key_entries.append(entry)

        def retrieve_record():
            key_values = [entry.get() for entry in key_entries]
            if not all(key_values):
                messagebox.showerror("Error", "Please fill in all key fields to retrieve.")
                return

            conn = create_connection()
            if conn:
                try:
                    where_part = " AND ".join([f"{k} = %s" for k in keys])
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE {where_part}", key_values)
                    record = cursor.fetchone()
                    if record:
                        record_str = "\n".join([f"{col}: {val}" for col, val in zip(columns, record)])
                        messagebox.showinfo("Record Found", f"Record Details:\n\n{record_str}")
                    else:
                        messagebox.showinfo("Not Found", "No record found with the provided key(s).")
                    conn.close()
                    retrieve_frame.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

        btn_frame = ttk.Frame(retrieve_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        ttk.Button(btn_frame, text="Search", command=retrieve_record).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=retrieve_frame.destroy).pack(side=tk.RIGHT, padx=5)

    def view_all_data(self, tree, table_name):
        conn = create_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table_name}")
                records = cursor.fetchall()
                for row in tree.get_children():
                    tree.delete(row)
                for record in records:
                    tree.insert("", "end", values=record)
                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FoodDeliveryApp(root)
    root.mainloop()
