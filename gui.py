import tkinter as tk
from tkinter import messagebox
from database import connect_db
from tkinter import ttk

# Main Window
root = tk.Tk()
style = ttk.Style(root)
style.theme_use("clam")
root.title("Library Management System")
root.geometry("1100x700")
root.configure(bg="#eef2ff")
root.resizable(False, False)


# Sidebar
sidebar = tk.Frame(root, bg="#111827", width=220)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)


# Project Title
title = tk.Label(
    sidebar, text="LIBRARY SYSTEM", font=("Arial", 16, "bold"), bg="#111827", fg="#60a5fa"
)
title.pack(pady=30)


# Add book function(window)
def add_book_window():
    window = tk.Toplevel(root)
    window.title("Add New Book")
    window.geometry("450x450")
    window.configure(bg="#F1F5F9")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Add New Book",
        font=("Arial", 20, "bold"),
        bg="#172554",
        fg="white",
    ).pack(fill="x", pady=20)

    # Book Name
    tk.Label(
        window,
        text="Book Name",
        font=("Arial", 11, "bold"),
        bg="#F1F5F9",
        fg="#334155"
        ).pack()
    
    book_name = tk.Entry(
        window,
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB"
    )
    book_name.pack(pady=5)

    # Author
    tk.Label(
        window, 
        text="Author Name",
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"
        ).pack()
    
    author = tk.Entry(
        window, 
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB"
        )
    author.pack(pady=5)

    # Category
    tk.Label(
        window, 
        text="Category",
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"
        ).pack()
    
    category = tk.Entry(
        window,
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB"
        )
    category.pack(pady=5)

    # Quantity
    tk.Label(
        window, 
        text="Quantity", 
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"
        ).pack()
    
    quantity = tk.Entry(
        window, 
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB"
        )
    quantity.pack(pady=5)

    # Save Function
    def save_book():

        name = book_name.get().strip()
        author_name = author.get().strip()
        book_category = category.get().strip()
        book_quantity = quantity.get().strip()

        if not name or not book_quantity:
            messagebox.showerror("Error", "Book Name and Quantity are required!")
            return

        try:
            qty = int(book_quantity)

            if qty <= 0:
                messagebox.showerror("Error", "Quantity must be greater than zero!")
                return

        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number!")
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror("Database Error", "Database connection failed!")
            return

        try:
            cur = conn.cursor()

            cur.execute(
                """
            INSERT INTO books (book_name, author, category, quantity, available)
            VALUES (%s, %s, %s, %s, %s)""",
                (name, author_name, book_category, qty, qty),
            )

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo("Success", "Book Added Successfully!")

            refresh_dashboard()

            window.destroy()

        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror("Error", str(e))

    # Save Button
    tk.Button(
        window,
        text="Save Book",
        font=("Arial", 12, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        padx=8,
        pady=8,
        command=save_book,
    ).pack(pady=25)


# View book function(window)
def view_books_window():
    window = tk.Toplevel(root)
    window.title("View Books")
    window.geometry("850x450")
    window.configure(bg="#EFF6FF")
    # window.resizable(False, False)

    tk.Label(
        window,
        text="All Library Books",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e293b",
    ).pack(pady=20)

    # Table Frame
    table_frame = tk.Frame(window)
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("ID", "Book Name", "Author", "Category", "Quantity", "Available")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    column_widths = {
        "ID": 60,
        "Book Name": 200,
        "Author": 160,
        "Category": 140,
        "Quantity": 100,
        "Available": 100
    }

    for col in columns:
        tree.heading(col, text=col)
        tree.column(
            col,
            width=column_widths[col],
            anchor="center"
        )

    # Table Styling
    style = ttk.Style()

    style.configure(
        "Treeview",
        background="#ffffff",
        foreground="#1e293b",
        rowheight=35,
        fieldbackground="#ffffff",
        font=("Arial", 10)
    )

    style.configure(
        "Treeview.Heading",
        background="#172554",
        foreground="white",
        font=("Arial", 10, "bold"),
        padding=10
    )

    style.configure(
    "Vertical.TScrollbar",
    background="#cbd5e1",
    troughcolor="#f1f5f9",
    bordercolor="#f1f5f9",
    arrowcolor="#1e293b",
    width=14
    )

    style.map(
        "Vertical.TScrollbar",
        background=[("active", "#64748b")]
    )

    style.map(
        "Treeview",
        background=[("selected", "#3b82f6")],
        foreground=[("selected", "white")]
    )

    #Scroll Bar
    scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=tree.yview
    )

    tree.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)


    # Fetch Records
    conn = connect_db()

    if conn is None:
        messagebox.showerror("Error", "Database connection failed!")
        window.destroy()
        return

    try:
        cur = conn.cursor()

        cur.execute("""
        SELECT book_id, book_name, author, category, quantity, available
        FROM books
        ORDER BY book_id
        """)

        records = cur.fetchall()

        for index, record in enumerate(records):

            if index % 2 == 0:
                tree.insert("", "end", values=record, tags=("evenrow",))

            else:
                tree.insert("", "end", values=record, tags=("oddrow",))


        tree.tag_configure("evenrow", background="#ffffff")

        tree.tag_configure("oddrow", background="#eff6ff")

        cur.close()
        conn.close()

    except Exception as e:
        conn.rollback()
        conn.close()
        messagebox.showerror("Error", str(e))


# Search Book Function(window)
def search_book_window():
    window = tk.Toplevel(root)
    window.title("Search Book")
    window.geometry("700x500")
    window.configure(bg="#F1F5F9")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Search Book by ID",
        font=("Arial", 20, "bold"),
        bg="#F1F5F9",
        fg="#0F172A",
    ).pack(pady=25)

    tk.Label(
        window, 
        text="Enter Book ID",
        font=("Arial", 11, "bold"),
        bg="#F1F5F9",
        fg="#334155"
        ).pack()

    book_id_entry = tk.Entry(
        window,
        font=("Arial", 12),
        relief="solid",
        bd=1, 
        width=30
        )
    book_id_entry.pack(pady=10)

    def search_book():

        book_id = book_id_entry.get().strip()

        if book_id == "":
            messagebox.showerror("Error", "Please Enter Book ID!")
            return

        try:
            book_id = int(book_id)

        except ValueError:
            messagebox.showerror("Error", "Book ID must be a number!")
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror("Error", "Database connection failed!")
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))

            record = cur.fetchone()

            if record:
                tree.delete(*tree.get_children())
                tree.insert("", "end", values=record)

            else:
                messagebox.showinfo("Not Found", "Book Not Found!")

            cur.close()
            conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", str(e))

    # Result Table Frame
    table_frame = tk.Frame(window, bg="#f1f5f9")
    table_frame.pack(fill="both", expand=True, padx=15, pady=5)

    columns = ("ID", "Book Name", "Author", "Category", "Quantity", "Available")

    style = ttk.Style(window)

    style.configure(
        "Search.Treeview",
        background="white",
        foreground="#0f172a",
        rowheight=30,
        fieldbackground="white",
        font=("Arial", 10)
    )

    tree = ttk.Treeview(
        table_frame, 
        columns=columns, 
        show="headings", 
        height=5,
        style="Search.Treeview"
        )
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # search button
    sear_btn = tk.Button(
        window,
        text="Search Book",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1d4ed8",
        activeforeground="white",
        cursor="hand2",
        relief="flat",
        width=20,
        padx=8,
        pady=8,
        command=search_book,
    )
    sear_btn.pack(pady=10)


# Update Book Function(window)
def update_book_window():
    window = tk.Toplevel(root)
    window.title("Update Book")
    window.geometry("500x550")
    window.configure(bg="#F1F5F9")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Update Book Details",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#1e293b",
    ).pack(pady=20)

    tk.Label(
        window, 
        text="Enter Book ID", 
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"
        ).pack()

    book_id_entry = tk.Entry(
        window,
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB", 

        )
    book_id_entry.pack(pady=5)

    # Book Details Fields
    tk.Label(
        window, 
        text="Book Name",
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155" 
        ).pack()
    
    name_entry = tk.Entry(
        window, 
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB",
        )
    name_entry.pack(pady=5)

    tk.Label(
        window, 
        text="Author",
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"  
        ).pack()
    
    author_entry = tk.Entry(
        window, 
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB",
        )
    author_entry.pack(pady=5)

    tk.Label(
        window, 
        text="Category",
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"  
        ).pack() 
    
    category_entry = tk.Entry(
        window, 
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB",
        )
    category_entry.pack(pady=5)

    tk.Label(
        window, 
        text="Quantity",
        font=("Arial", 11, "bold"), 
        bg="#F1F5F9",
        fg="#334155"  
        ).pack()
    
    quantiy_entry = tk.Entry(
        window, 
        width=35,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#CBD5E1",
        highlightcolor="#2563EB",
        )
    quantiy_entry.pack(pady=5)
    

    def find_book():

        book_id = book_id_entry.get().strip()

        if book_id == "":
            messagebox.showerror("Error", "Please enter Book ID!")
            return

        try:
            book_id = int(book_id)

        except ValueError:
            messagebox.showerror("Error", "Book ID must be Number!")
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror("Error", "Database connection failed!")
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))

            record = cur.fetchone()

            name_entry.delete(0, tk.END)
            author_entry.delete(0, tk.END)
            category_entry.delete(0, tk.END)
            quantiy_entry.delete(0, tk.END)

           
            if record:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, record[1])

                author_entry.delete(0, tk.END)
                author_entry.insert(0, record[2])

                category_entry.delete(0, tk.END)
                category_entry.insert(0, record[3])

                quantiy_entry.delete(0, tk.END)
                quantiy_entry.insert(0, record[4])

                cur.close()
                conn.close()

            else:
                messagebox.showerror(
                    "Not Found",
                    "Book ID does not exist!"
                    )

                cur.close()
                conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", str(e))

    #Find book button(update window)
    search_btn = tk.Button(
        window,
        text="Find Book",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        padx=8,
        pady=8,
        command=find_book,
    )
    search_btn.pack(pady=15)

        

    def save_updated_book():

        book_id = book_id_entry.get().strip()

        if book_id == "":
            messagebox.showerror(
                "Error",
                "Please enter Book ID!"
            )
            return

        try:
            book_id = int(book_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Book ID must be number!"
            )
            return

        name = name_entry.get().strip()
        author_name = author_entry.get().strip()
        book_category = category_entry.get().strip()
        book_quantity = quantiy_entry.get().strip()

        if not name or not book_quantity:
            messagebox.showerror(
                "Error",
                "Book Name and Quantity are required!"
            )
            return

        try:
            qty = int(book_quantity)

            if qty <= 0:
                messagebox.showerror(
                    "Error",
                    "Quantity must be greater than zero!"
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Quantiy must be a number!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Database Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""SELECT quantity, available 
            FROM books 
            WHERE book_id = %s FOR UPDATE""", (book_id,))

            book_data = cur.fetchone()

            if book_data is None:
                conn.rollback()
                cur.close()
                conn.close()
                messagebox.showerror(
                    "Not Found!",
                    "Book ID does not exist!"
                )
                return

            cur.execute("""SELECT COUNT(*) FROM issued_books
            WHERE book_id = %s AND status = 'Issued'""", (book_id,))

            issued_count = cur.fetchone()[0]

            if qty < issued_count:
                messagebox.showerror(
                    "Invalid Quantity",
                    f"At least {issued_count} copies are currently issued. Quantity cannot be less than this."
                )
                cur.close()
                conn.close()
                return

            cur.execute("""
            UPDATE books SET book_name = %s, author = %s, category = %s, available = %s - %s, quantity = %s
            WHERE book_id = %s
            """, (name, author_name, book_category, qty, issued_count, qty, book_id))

            if cur.rowcount == 0:
                conn.rollback()
                cur.close()
                conn.close()

                messagebox.showerror(
                    "Not Found",
                    "Book ID does not exist!"
                )
                return

            else:
                conn.commit()
                cur.close()
                conn.close()
                
                messagebox.showinfo(
                    "Success",
                    "Book Updated Successfully!"
                )

                window.destroy()


        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror(
                "Error",
                str(e)
            )

    #Update button
    update_button = tk.Button(
        window,
        text="Update Book",
        font=("Arial", 11, "bold"),
        bg="#16a34a",
        fg="white",
        activebackground="#0A872B",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        padx=8,
        pady=8,
        command=save_updated_book
    )
    update_button.pack(pady=15)


# Delete Book function(window)
def delete_book_window():
    window = tk.Toplevel(root)
    window.title("Delete Book")
    window.geometry("700x500")
    window.configure(bg="#F1F5F9")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Delete Book",
        font=("Arial", 20, "bold"),
        bg="#F1F5F9",
        fg="#0F172A",
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Book ID",
        font=("Arial", 11, "bold"),
        bg="#F1F5F9",
        fg="#334155"
    ).pack()

    book_id_entry = tk.Entry(
        window, 
        width=30,
        font=("Arial", 11),
        bg="white",
        fg="#1e293b",
        relief="solid",
        bd=1
        )
    book_id_entry.pack(pady=10)

    #Book Details
    tk.Label(
        window,
        text="Book Details",
        font=("Arial", 14, "bold"),
        bg="#F1F5F9",
        fg="#334155"
    ).pack(pady=10)

    details_frame = tk.Frame(
        window,
        bg="white"
    )
    details_frame.pack(pady=5)

    columns = ("ID", "Book Name", "Author", "Category", "Quantity", "Available")

    style = ttk.Style()

    style.configure(
        "Delete.Treeview",
        background="white",
        foreground="#0F172A",
        fieldbackground="white",
        rowheight=35,
        font=("Arial", 10)
    )

    style.configure(
        "Delete.Treeview.Heading",
        background="#172554",
        foreground="white",
        font=("Arial", 10, "bold"),
        padding=8
    )

    tree = ttk.Treeview(
        details_frame,
        columns=columns,
        show="headings",
        height=1,
        style="Delete.Treeview"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=85, anchor="center")

    tree.pack()

    def find_book():

        book_id = book_id_entry.get().strip()

        if book_id == "":
            messagebox.showerror(
                "Error",
                "Please enter book ID!"
            )
            return

        try:
            book_id = int(book_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Book ID must be a number!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""
            SELECT book_id, book_name, author, category, quantity, available FROM books
            WHERE book_id = %s""", (book_id,))

            record = cur.fetchone()

            tree.delete(*tree.get_children())

            if record:
                tree.insert("", "end", values=record)

            else:
                messagebox.showinfo(
                    "Not Found",
                    "Book ID does not exist!"
                )

                cur.close()
                conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror(
                "Error",
                str(e)
            )

    # Find Book Button
    find_btn = tk.Button(
        window,
        text="Find Book",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        activebackground="#1D4ED8",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        padx=8,
        pady=8,
        command=find_book
    )
    find_btn.pack(pady=15)


    def delete_book():

        book_id = book_id_entry.get().strip()

        if book_id == "":
            messagebox.showerror(
                "Error",
                "Please Enter Book ID!"
            )
            return

        try:
            book_id = int(book_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Book ID must be number!"
            )
            return

        if not tree.get_children():
            messagebox.showerror(
                "Error",
                "Please find a book first!"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this book?"
        )

        if not confirm:
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT COUNT(*) FROM issued_books WHERE book_id = %s", (book_id,))

            issue_count = cur.fetchone()[0]

            if issue_count > 0:
                messagebox.showerror(
                    "Cannot Delete",
                    "This book has transaction history and cannot be deleted!"
                )
                cur.close()
                conn.close()
                return

            cur.execute("DELETE FROM books WHERE book_id = %s", (book_id,))

            if cur.rowcount == 0:
                messagebox.showerror(
                    "Not Found",
                    "Book ID does not exist!"
                )

            else:
                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Book Deleted Successfully!"
                )

                refresh_dashboard()

                window.destroy()

            cur.close()
            conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror(
                "Error",
                str(e)
            )

    # Delete Button
    delete_btn = tk.Button(
        window,
        text="Delete Book",
        font=("Arial", 11, "bold"),
        bg="#dc2626",
        fg="white",
        activebackground="#ac0c0c",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        width=20,
        padx=8,
        pady=8,
        command=delete_book
    )
    delete_btn.pack(pady=15)





# Add Student Function(window)
def add_student_window():
    window = tk.Toplevel(root)
    window.title("Add New Student")
    window.geometry("450x450")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Add New Student",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=20)

    #Student Name
    tk.Label(window, text="Student Name", bg="white").pack()
    student_name = tk.Entry(window, width=35)
    student_name.pack(pady=5)

    #Student Email
    tk.Label(window, text="Email", bg="white").pack()
    student_email = tk.Entry(window, width=35)
    student_email.pack(pady=5)

    #Student Phone Number
    tk.Label(window, text="Phone Number", bg="white").pack()
    student_phone = tk.Entry(window, width=35)
    student_phone.pack(pady=5)

    def save_student():
        name = student_name.get().strip()
        email = student_email.get().strip()
        phone = student_phone.get().strip()

        if not name or not email or not phone:
            messagebox.showerror(
                "Error",
                "All fields are required!"
            )
            return

        if "@" not in email or "." not in email:
            messagebox.showerror(
                "Error",
                "Please enter a valid email!"
            )
            return

        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror(
                "Invalid Phone",
                "Phone Number must be 10 digits!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Database Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""INSERT INTO students (student_name, email, phone)
            VALUES (%s, %s, %s)""", (name, email, phone))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Students Added Successfully!"
            )

            refresh_dashboard()

            window.destroy()

        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror(
                "Error",
                str(e)
            )

    #Save Button(students)
    save_btn = tk.Button(
        window,
        text="Save Student",
        font=("Arial", 12, "bold"),
        bg="#2563eb",
        fg="white",
        width=20,
        pady=8,
        command=save_student
    )
    save_btn.pack(pady=20)


#View student Window
def view_student_window():
    window = tk.Toplevel(root)
    window.title("View Students")
    window.geometry("850x450")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="All Registered Students",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=20)

    #Table frame
    table_frame = tk.Frame(
        window,
        bg="white"
    )
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("ID", "Student Name", "Email", "Phone")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    tree.pack(fill="both", expand=True)

    #Fetch Student Records
    conn = connect_db()

    if conn is None:
        messagebox.showerror(
            "Error",
            "Database connection failed!"
        )
        window.destroy()
        return

    try:
        cur = conn.cursor()

        cur.execute("""SELECT student_id, student_name, email, phone FROM students
        ORDER BY student_id""")

        records = cur.fetchall()

        for record in records:
            tree.insert("", "end", values=record)

        cur.close()
        conn.close()

    except Exception as e:
        conn.rollback()
        conn.close()
        messagebox.showerror(
            "Error",
            str(e)
        )



# Search Student Function(window)
def search_student_window():
    window = tk.Toplevel(root)
    window.title("Search Student")
    window.geometry("850x450")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Search Student by ID",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter Student ID",
        bg="white",
    ).pack()

    student_id_entry = tk.Entry(window, width=30)
    student_id_entry.pack(pady=10)

    #Result Table Frame
    table_frame = tk.Frame(
        window,
        bg="white"
    )
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("ID", "Student Name", "Email", "Phone")

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=5
    )
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    tree.pack(fill="both", expand=True)

    #search student
    def search_student():

        student_id = student_id_entry.get().strip()

        if student_id == "":
            messagebox.showerror(
                "Error",
                "Please Enter Student ID!"
            )
            return

        try:
            student_id = int(student_id)

        except ValueError:
                messagebox.showerror(
                    "Error",
                    "Student ID must be number!"
                )
                return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""SELECT student_id, student_name, email, phone FROM students
            WHERE student_id = %s""", (student_id,))

            record = cur.fetchone()

            tree.delete(*tree.get_children())

            if record:
                tree.insert("", "end", values=record)

            else:
                messagebox.showinfo(
                    "Not Found",
                    "Student Not Found!"
                )

            cur.close()
            conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror(
                "Error",
                str(e)
            )

    # Search Button
    search_btn = tk.Button(
        window,
        text="Search Student",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        width=20,
        pady=8,
        command=search_student
    )
    search_btn.pack(pady=15)



# Update Student Function(window)
def update_student_window():
    window = tk.Toplevel(root)
    window.title("Update Student")
    window.geometry("500x550")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Update Students Details",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=20)

    tk.Label(
        window,
        text="Enter Student ID",
        font=("Arial", 11),
        bg="white"
    ).pack()

    student_id_entry = tk.Entry(window, width=30)
    student_id_entry.pack(pady=10)

    #Student Details Fields
    tk.Label(window, text="Student Name", bg="white").pack()
    name_entry = tk.Entry(window, width=35)
    name_entry.pack(pady=5)

    tk.Label(window, text="Email", bg="white").pack()
    email_entry = tk.Entry(window, width=35)
    email_entry.pack(pady=5)

    tk.Label(window, text="Phone", bg="white").pack()
    phone_entry = tk.Entry(window, width=35)
    phone_entry.pack(pady=5)

    def find_student():
        
        student_id = student_id_entry.get().strip()
    
        if student_id == "":
            messagebox.showerror("Error", "Please enter Student ID!")
            return

        try:
            student_id = int(student_id)

        except ValueError:
            messagebox.showerror("Error", "Student ID must be Number!")
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror("Error", "Database connection failed!")
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT * FROM students WHERE student_id = %s", (student_id,))

            record = cur.fetchone()

            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)

            
            if record:
                name_entry.delete(0, tk.END)
                name_entry.insert(0, record[1])

                email_entry.delete(0, tk.END)
                email_entry.insert(0, record[2])

                phone_entry.delete(0, tk.END)
                phone_entry.insert(0, record[3])

                cur.close()
                conn.close()

            else:
                messagebox.showerror(
                    "Not Found",
                    "Student ID does not exist!"
                    )

                cur.close()
                conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror("Error", str(e))

    #Find Student button(update window)
    search_btn = tk.Button(
        window,
        text="Find Student",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        width=20,
        padx=8,
        command=find_student,
    )
    search_btn.pack(pady=15)


    def save_updated_student():

        student_id = student_id_entry.get().strip()

        if student_id == "":
            messagebox.showerror(
                "Error",
                "Please enter Student ID!"
            )
            return

        try:
            student_id = int(student_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Student ID must be number!"
            )
            return

        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()

        if not name or not email or not phone:
            messagebox.showerror(
                "Error",
                "All fields are required!"
            )
            return
    
        if "@" not in email or "." not in email:
            messagebox.showerror(
                "Error",
                "Please enter a valid email!"
            )
            return
    
        if not phone.isdigit() or len(phone) != 10:
            messagebox.showerror(
                "Invalid Phone",
                "Phone Number must be 10 digits!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Database Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""
            UPDATE students SET student_name = %s, email = %s, phone = %s
            WHERE student_id = %s
            """, (name, email, phone, student_id))

            if cur.rowcount == 0:
                conn.rollback()
                cur.close()
                conn.close()

                messagebox.showerror(
                    "Not Found",
                    "Student ID does not exist!"
                )
                return

            else:
                conn.commit()
                cur.close()
                conn.close()
                
                messagebox.showinfo(
                    "Success",
                    "Student Details Updated Successfully!"
                )

                window.destroy()


        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror(
                "Error",
                str(e)
            )

    #Update button
    update_button = tk.Button(
        window,
        text="Update Student",
        font=("Arial", 11, "bold"),
        bg="#16a34a",
        fg="white",
        width="20",
        pady=8,
        command=save_updated_student
    )
    update_button.pack(pady=15)



# Delete Student Function(window)
def delete_student_window():
    window = tk.Toplevel(root)
    window.title("Delete Student")
    window.geometry("850x450")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Delete Student",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Student ID",
        font=("Arial", 11),
        bg="white"
    ).pack()

    student_id_entry = tk.Entry(window, width=30)
    student_id_entry.pack(pady=10)

    #Student Details
    tk.Label(
        window,
        text="Student Details",
        font=("Arial", 14, "bold"),
        bg="white"
    ).pack(pady=10)

    details_frame = tk.Frame(
        window,
        bg="white"
    )
    details_frame.pack(pady=5)

    columns = ("ID", "Student Name", "Email", "Phone")

    tree = ttk.Treeview(
        details_frame,
        columns=columns,
        show="headings",
        height=1
    )

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    tree.pack()

    def find_student():

        student_id = student_id_entry.get().strip()

        if student_id == "":
            messagebox.showerror(
                "Error",
                "Please enter Student ID!"
            )
            return

        try:
            student_id = int(student_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Student ID must be a number!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""
            SELECT student_id, student_name, email, phone FROM students
            WHERE student_id = %s""", (student_id,))

            record = cur.fetchone()

            tree.delete(*tree.get_children())

            if record:
                tree.insert("", "end", values=record)

            else:
                messagebox.showinfo(
                    "Not Found",
                    "Student ID does not exist!"
                )

                cur.close()
                conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror(
                "Error",
                str(e)
            )

    # Find Student Button
    find_btn = tk.Button(
        window,
        text="Find Student",
        font=("Arial", 11, "bold"),
        bg="#2563eb",
        fg="white",
        width=20,
        padx=8,
        command=find_student
    )
    find_btn.pack(pady=10)


    def delete_student():

        student_id = student_id_entry.get().strip()

        if student_id == "":
            messagebox.showerror(
                "Error",
                "Please Enter Student ID!"
            )
            return

        try:
            student_id = int(student_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Student ID must be number!"
            )
            return

        if not tree.get_children():
            messagebox.showerror(
                "Error",
                "Please find a Student first!"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this Student Details?"
        )

        if not confirm:
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

        
            cur.execute("SELECT COUNT(*) FROM issued_books WHERE student_id = %s", (student_id,))

            issue_count = cur.fetchone()[0]

            if issue_count > 0:
                messagebox.showerror(
                    "Cannot Delete",
                    "This student has transaction history and cannot be deleted!"
                )
                cur.close()
                conn.close()
                return

            cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))

            if cur.rowcount == 0:
                messagebox.showerror(
                    "Not Found",
                    "Student ID does not exist!"
                )

            else:
                conn.commit()

                messagebox.showinfo(
                    "Success",
                    "Student Details Deleted Successfully!"
                )

                refresh_dashboard()

                window.destroy()

            cur.close()
            conn.close()

        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror(
                "Error",
                str(e)
            )

    # Delete Button
    delete_btn = tk.Button(
        window,
        text="Delete Student",
        font=("Arial", 11, "bold"),
        bg="#dc2626",
        fg="white",
        width=20,
        pady=8,
        command=delete_student
    )
    delete_btn.pack(pady=20)



#Issue book window
def issue_books_window():
    window = tk.Toplevel(root)
    window.title("Issue Books")
    window.geometry("500x450")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Issue Books",
        font=("Arial", 22, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=25)

    #Book ID
    tk.Label(window, text="Book ID", bg="white").pack()
    book_id_entry = tk.Entry(window, width=35)
    book_id_entry.pack(pady=8)

    #Student ID
    tk.Label(window, text="Student ID", bg="white").pack()
    student_id_entry = tk.Entry(window, width=35)
    student_id_entry.pack(pady=8)

    #Return Date
    tk.Label(window, text="Return Date(YYYY-MM-DD)", bg="white").pack()
    return_date_entry = tk.Entry(window, width=35)
    return_date_entry.pack(pady=8)


    #Issue book function
    def issue_book():

        book_id = book_id_entry.get().strip()
        student_id = student_id_entry.get().strip()
        return_date = return_date_entry.get().strip()

        if not book_id or not student_id or not return_date:
            messagebox.showerror(
                "Error",
                "All fields are required!"
            )
            return

        try:
            book_id = int(book_id)
            student_id = int(student_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "IDs must be Number!"
            )
            return

        try:
            from datetime import date

            return_date_obj = date.fromisoformat(return_date)

            if return_date_obj < date.today():
                messagebox.showerror(
                    "Invalid Date",
                    "Return Date cannot be in past!"
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Return Date must be YYYY-MM-DD!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Database Error",
                "Databse connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("SELECT available FROM books WHERE book_id = %s FOR UPDATE",(book_id,))

            book = cur.fetchone()

            if book is None:
                messagebox.showerror(
                    "Error",
                    "Book Id not found!"
                )
                cur.close()
                conn.close()
                return

            if book[0] <= 0:
                messagebox.showerror(
                    "Unavailable",
                    "This book is currently not available!"
                )
                cur.close()
                conn.close()
                return


            cur.execute("SELECT student_id FROM students WHERE student_id = %s", (student_id,))

            student = cur.fetchone()

            if student is None:
                messagebox.showerror(
                    "Error",
                    "Student Id not found!"
                )
                cur.close()
                conn.close()
                return

            cur.execute("""INSERT INTO issued_books (book_id, student_id, issue_date, expected_return_date, status)
            VALUES (%s, %s, CURRENT_DATE, %s, 'Issued')
            """, (book_id, student_id, return_date))

            cur.execute("""UPDATE books SET available = available - 1 WHERE book_id = %s""", (book_id,))

            conn.commit()

            cur.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Book Issued Successfully!"
            )

            refresh_dashboard()

            window.destroy()

        except Exception as e:
            conn.rollback()
            conn.close()

            messagebox.showerror(
                "Database Error",
                str(e)
            )         

    tk.Button(
        window,
        text="Issue Book",
        font=("Arial", 12, "bold"),
        bg="#2563eb",
        fg="white",
        width=20,
        padx=8,
        command=issue_book
    ).pack(pady=25)



#Return books window
def return_books_window():
    window = tk.Toplevel(root)
    window.title("Return Books")
    window.geometry("850x450")
    window.configure(bg="white")
    window.resizable(False, False)

    tk.Label(
        window,
        text="Return Books",
        font=("Arial", 20, "bold"),
        bg="white",
        fg="#1e293b"
    ).pack(pady=25)

    tk.Label(
        window,
        text="Enter Issue ID",
        font=("Arial", 11),
        bg="white"
    ).pack(pady=10)

    issue_id_entry = tk.Entry(window, width=30)
    issue_id_entry.pack(pady=5)

    def return_book():

        issue_id = issue_id_entry.get().strip()

        if not issue_id:
            messagebox.showerror(
                "Error",
                "Please enter Issue ID!"
            )
            return

        try:
            issue_id = int(issue_id)

        except ValueError:
            messagebox.showerror(
                "Error",
                "Issue ID must be number!"
            )
            return

        conn = connect_db()

        if conn is None:
            messagebox.showerror(
                "Error",
                "Database connection failed!"
            )
            return

        try:
            cur = conn.cursor()

            cur.execute("""SELECT book_id, status 
            FROM issued_books 
            WHERE issue_id = %s FOR UPDATE""", (issue_id,))

            record = cur.fetchone()

            if record is None:
                conn.rollback()
                cur.close()
                conn.close()
                messagebox.showerror(
                    "Error",
                    "Issued ID not found!"
                )
                return

            book_id, status = record

            if status !="Issued":
                conn.rollback()
                cur.close()
                conn.close()
                messagebox.showwarning(
                    "Warning",
                    "This book is not currently issued."
                )
                return

            cur.execute("""UPDATE issued_books SET status = 'Returned', actual_return_date = CURRENT_DATE
            WHERE issue_id = %s""", (issue_id,))

            cur.execute("""UPDATE books SET available = available + 1
            WHERE book_id = %s""", (book_id,))

            conn.commit()
            cur.close()
            conn.close()

            messagebox.showinfo(
                "Success",
                "Book Returned Successfully!"
            )

            refresh_dashboard()

            window.destroy()

        except Exception as e:
            conn.rollback()
            conn.close()
            messagebox.showerror(
                "Database Error",
                str(e)
            )

    tk.Button(
            window,
            text="Return Book",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            width=20,
            padx=8,
            command=return_book
        ).pack(pady=25)



# Library summary report(window)
def library_summary_report():

    conn = connect_db()

    if conn is None:
        messagebox.showerror(
            "Database Error",
            "Database connection failed!"
        )
        return

    try:
        cur = conn.cursor()

        cur.execute("SELECT COALESCE(SUM(quantity), 0), COUNT(*) FROM books")
        total_copies, total_titles = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE status = 'Issued' ")
        issued_books = cur.fetchone()[0]

        cur.execute("SELECT COALESCE(SUM(available), 0) FROM books")
        available_books = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE status = 'Returned'")
        returned_books = cur.fetchone()[0]


        report_window = tk.Toplevel(root)
        report_window.title("Library Summary")
        report_window.geometry("600x500")
        report_window.configure(bg="#f1f5f9")
        report_window.resizable(False, False)


        tk.Label(
            report_window,
            text="Library Summary Report",
            font=("Arial", 22, "bold"),
            bg="#f1f5f9",
            fg="#1e293b"
        ).pack(pady=25)

        report_data = [
            ("Total Book Copies", total_copies),
            ("Total Book Titles", total_titles),
            ("Total Students", total_students),
            ("Currently Issued Books", issued_books),
            ("Available Book Copies", available_books),
            ("Returned Books", returned_books)
            ]

        for label, value in report_data:

            row = tk.Frame(report_window, bg="white")
            row.pack(fill="x", padx=40, pady=6)

            tk.Label(
                row,
                text=label,
                font=("Arial", 12),
                bg="white",
                fg="#334155"
            ).pack(side="left", padx=15, pady=12)

            tk.Label(
                row,
                text=str(value),
                font=("Arial", 12, "bold"),
                bg="white",
                fg="#2563eb"
            ).pack(side="right", padx=15)

        cur.close()

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

    finally:
        conn.close()



# Issue books report(window)
def issued_books_report():

    conn = connect_db()

    if conn is None:
        messagebox.showerror(
        "Database Error",
        "Database connection failed!"
        )
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                ib.issue_id,
                b.book_name,
                s.student_name,
                ib.issue_date,
                ib.expected_return_date,
                ib.status
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.book_id
            JOIN students s ON ib.student_id = s.student_id
            WHERE ib.status = 'Issued'
            ORDER BY ib.issue_id DESC
        """)

        records = cur.fetchall()

        report_window = tk.Toplevel(root)
        report_window.title("Issued Books Report")
        report_window.geometry("950x500")
        report_window.configure(bg="#f1f5f9")

        tk.Label(
            report_window,
            text="Issued Books Report",
            font=("Arial", 22, "bold"),
            bg="#f1f5f9",
            fg="#1e293b"
        ).pack(pady=20)

        columns = (
            "Issue ID",
            "Book Name",
            "Student Name",
            "Issue Date",
            "Expected Return",
            "Status"
        )

        tree = ttk.Treeview(
            report_window,
            columns=columns,
            show="headings"
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=145, anchor="center")

        tree.pack(fill="both", expand=True, padx=20, pady=15)

        for record in records:
            tree.insert("", "end", values=record)

        if not records:
            messagebox.showinfo(
                "Issued Books",
                "No currently issued books found."
            )

        cur.close()

    except Exception as e:
        messagebox.showerror("Error", str(e))

    finally:
        conn.close()




# Returned Books Report(window)
def returned_books_report():

    conn = connect_db()

    if conn is None:
        messagebox.showerror(
            "Database Error",
            "Database connection failed!"
        )
        return

    try:
        cur = conn.cursor()

        cur.execute("""
            SELECT
                ib.issue_id,
                b.book_name,
                s.student_name,
                ib.issue_date,
                ib.expected_return_date,
                ib.actual_return_date,
                ib.status
            FROM issued_books ib
            JOIN books b ON ib.book_id = b.book_id
            JOIN students s ON ib.student_id = s.student_id
            WHERE ib.status = 'Returned'
            ORDER BY ib.issue_id DESC
        """)

        records = cur.fetchall()

        report_window = tk.Toplevel(root)
        report_window.title("Returned Books Report")
        report_window.geometry("1100x500")
        report_window.configure(bg="#f1f5f9")

        tk.Label(
            report_window,
            text="Returned Books Report",
            font=("Arial", 22, "bold"),
            bg="#f1f5f9",
            fg="#1e293b"
        ).pack(pady=20)

        columns = (
            "Issue ID",
            "Book Name",
            "Student Name",
            "Issue Date",
            "Expected Return",
            "Actual Return",
            "Status"
        )

        tree = ttk.Treeview(
            report_window,
            columns=columns,
            show="headings"
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        tree.pack(fill="both", expand=True, padx=20, pady=15)

        for record in records:
            tree.insert("", "end", values=record)

        if not records:
            messagebox.showinfo(
                "Returned Books",
                "No returned books found."
            )

        cur.close()

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

    finally:
        conn.close()



# Dashboard window(to count books, students and issued books..)
def get_dashboard_counts():

    conn = connect_db()

    if conn is None:
        messagebox.showerror(
            "Database Error",
            "Database connection failed!"
        )
        return 0, 0, 0

    cur = None

    try:
        
        cur = conn.cursor()

        cur.execute("SELECT COALESCE (SUM(quantity), 0) FROM books")
        total_books = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM students")
        total_students = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM issued_books WHERE status = 'Issued'")
        issued_books = cur.fetchone()[0]

        return total_books, total_students, issued_books

    except Exception as e:
        conn.rollback()

        messagebox.showerror(
            "Database Error",
            str(e)
        )
        return 0, 0, 0

    finally:
        if cur is not None:
            cur.close()

        conn.close()
        




# Navigation Function
def show_page(page):

    #Book Management
    if page == "Books":
        add_book_window()

    elif page == "View Books":
        view_books_window()

    elif page == "Search Book":
        search_book_window()

    elif page == "Update Book":
        update_book_window()

    elif page == "Delete Book":
        delete_book_window()

    #Student Management

    elif page == "Add Student":
        add_student_window()

    elif page == "View Student":
        view_student_window()

    elif page == "Search Student":
        search_student_window()

    elif page == "Update Student":
        update_student_window()

    elif page == "Delete Student":
        delete_student_window()

    # Transactions
    
    elif page == "Issue Books":
        issue_books_window()

    elif page == "Return Books":
        return_books_window()

    # Reports

    elif page == "Library Summary":
        library_summary_report()

    elif page == "Issued Books Report":
        issued_books_report()

    elif page == "Returned Books Report":
        returned_books_report()

    #Dashboard count
    
    elif page == "Dashboard":
        refresh_dashboard()


    else:
        messagebox.showinfo("Navigation", page + " section will be added soon!")


# Sidebar Buttons
def toggle_submenu(frame, button):

    if frame.winfo_ismapped():
        frame.pack_forget()
        button.config(text=button.cget("text").replace("▼", "▶"))

    else:
        frame.pack(fill="x")
        button.config(text=button.cget("text").replace("▶", "▼"))


def create_menu(parent, title, items):

    # Main Menu Button
    menu_button = tk.Button(
        parent,
        text=title + "  ▶",
        font=("Arial", 11, "bold"),
        bg="#1e293b",
        fg="white",
        activebackground="#2563eb",
        activeforeground="white",
        relief="flat",
        anchor="w",
        padx=20,
        pady=15,
    )
    menu_button.pack(fill="x", padx=12, pady=4)

    # Submenu Frame
    submenu = tk.Frame(parent, bg="#0f1728")

    # Submenu Buttons
    for label, page in items:

        tk.Button(
            submenu,
            text="  " + label,
            font=("Arial", 11),
            bg="#172554",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=20,
            pady=10,
            command=lambda p=page: show_page(p),
        ).pack(fill="x", padx=15, pady=2)

    # Expand / Collapse
    menu_button.config(command=lambda: toggle_submenu(submenu, menu_button))


# Dashboard Button
tk.Button(
    sidebar,
    text="Dashboard",
    font=("Arial", 12, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    relief="flat",
    anchor="w",
    padx=20,
    pady=12,
    command=lambda: show_page("Dashboard"),
).pack(fill="x", padx=12, pady=4)


# Books Management
create_menu(
    sidebar,
    "Books Management",
    [
        ("Add Book", "Books"),
        ("View Books", "View Books"),
        ("Search Book", "Search Book"),
        ("Update Book", "Update Book"),
        ("Delete Book", "Delete Book"),
    ],
)

# Stuent Management
create_menu(
    sidebar,
    "Student Management",
    [
        ("Add Student", "Add Student"),
        ("View Student", "View Student"),
        ("Search Student", "Search Student"),
        ("Update Student", "Update Student"),
        ("Delete Student", "Delete Student"),
    ],
)

# Transactions
create_menu(
    sidebar,
    "Transactions",
    [("Issue Books", "Issue Books"), ("Return Books", "Return Books")],
)

# Reports
create_menu(
    sidebar,
    "Reports",
    [
        ("Library Summary", "Library Summary"),
        ("Issued Books Report", "Issued Books Report"),
        ("Returned Books Report", "Returned Books Report"),
    ],
)

# Main Content Area
main_frame = tk.Frame(root, bg="#eef2ff")
main_frame.pack(side="left", fill="both", expand=True)


# Dashboard Heading
heading = tk.Label(
    main_frame, text="Dashboard", font=("Arial", 28, "bold"), bg="#f1f5f9", fg="#0f172a"
)
heading.pack(anchor="w", padx=30, pady=(30, 5))


subtitle = tk.Label(
    main_frame,
    text="Welcome to Library Management system",
    font=("Arial", 12),
    bg="#f1f5f9",
    fg="#64748b",
)
subtitle.pack(anchor="w", padx=32)


# Cards Frame
cards_frame = tk.Frame(
    main_frame,
    bg="#f1f5f9",
)
cards_frame.pack(fill="x", padx=20, pady=35)


# Dashboard Card Function
def create_card(parent, title, value, color):
    card = tk.Frame(
        parent,
        bg="white",
        width=225,
        height=150,
        highlightbackground="#bfdbfe",
        highlightthickness=0,
    )
    card.pack(side="left", padx=15, pady=8)
    card.pack_propagate(False)

    tk.Frame(
        card,
        bg=color,
        height=5,
    ).pack(fill="x")

    tk.Label(
        card,
        text=title,
        font=("Arial", 13, "bold"),
        bg="white",
        fg="#475569",
    ).pack(pady=(25, 8))

    value_label = tk.Label(
        card,
        text=value,
        font=("Arial", 34, "bold"),
        bg="white",
        fg=color
    )
    value_label.pack()

    return value_label


total_books, total_students, issued_books = get_dashboard_counts()
# Dashboard Cards
books_value_label = create_card(cards_frame, "Total Book Copies", total_books, "#2563eb")
students_value_label = create_card(cards_frame, "Total Students", total_students, "#16a34a")
issued_value_label = create_card(cards_frame, "Issued Books", issued_books, "#ea580c")

def refresh_dashboard():

    total_books, total_students, issued_books = get_dashboard_counts()

    books_value_label.config(text=total_books)

    students_value_label.config(text=total_students)

    issued_value_label.config(text=issued_books)



# Welcome Section
welcome_frame = tk.Frame(
    main_frame, bg="white", highlightbackground="#bfdbfe", highlightthickness=1
)
welcome_frame.pack(fill="x", padx=35, pady=15)

tk.Label(
    welcome_frame,
    text="Welcome Admin!",
    font=("Arial", 22, "bold"),
    bg="white",
    fg="#1d4ed8",
).pack(anchor="w", padx=25, pady=(25, 12))

tk.Label(
    welcome_frame,
    text="Manage Books, students and library recods easily.",
    font=("Arial", 12),
    bg="white",
    fg="#475569",
).pack(anchor="w", padx=25, pady=(0, 25))

# Footer
footer = tk.Label(
    main_frame,
    text="Library Management System | Python Tkinter",
    font=("Arial", 10),
    bg="#f1f5f9",
    fg="#64748b",
)
footer.pack(side="bottom", pady=20)





