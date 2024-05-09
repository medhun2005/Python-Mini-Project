import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk
import mysql.connector
from tkinter import ttk

# Connect to MySQL Workbench
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aaaa",
    database="library"
)
cursor = conn.cursor()

# Function to add a book
def add_book():
    title = title_entry.get()
    author = author_entry.get() 
    cursor.execute('''INSERT INTO books (title, author, status) VALUES (%s, %s, %s)''', (title, author, 'Available'))
    conn.commit()
    messagebox.showinfo("Success", "Book added successfully")

def view_books():
    cursor.execute('''SELECT * FROM books WHERE status=%s''', ('Available',))
    books = cursor.fetchall()
    if books:
        book_list_window = Toplevel(root)
        book_list_window.title("Available Books")
        book_list_window.geometry("500x500")

        # Load the background image for the book list window
        book_list_background_image = Image.open("book-image-2.jpg")
        book_list_background_image = book_list_background_image.resize((500, 500))
        book_list_background_photo = ImageTk.PhotoImage(book_list_background_image)

        # Create a label with the background image
        book_list_background_label = tk.Label(book_list_window, image=book_list_background_photo)
        book_list_background_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        book_list_background_label.lower()

        # Display the book list
        book_list_text = tk.Text(book_list_window)
        book_list_text.pack(fill=tk.BOTH, expand=True)

        book_list = '\n'.join([f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {book[3]}" for book in books])
        book_list_text.insert(tk.END, book_list)
        book_list_text.config(state=tk.DISABLED)  # Make the text widget read-only

    else:
        messagebox.showinfo("Available Books", "No books available")

def delete_book():
    book_id = book_id_entry.get()
    cursor.execute('''SELECT * FROM books WHERE id=%s''', (book_id,))
    book = cursor.fetchone()
    if book:
        cursor.execute('''DELETE FROM books WHERE id=%s''', (book_id,))
        conn.commit()
        messagebox.showinfo("Success", "Book deleted successfully")
    else:
        messagebox.showerror("Error", "Book not found")

def issue_book():
    book_id = book_id_entry.get()
    cursor.execute('''SELECT * FROM books WHERE id=%s''', (book_id,))
    book = cursor.fetchone()
    if book:
        if book[3] == 'Available':
            cursor.execute('''UPDATE books SET status=%s WHERE id=%s''', ('Issued', book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book issued successfully")
        else:
            messagebox.showerror("Error", "Book already issued")
    else:
        messagebox.showerror("Error", "Book not found")

def return_book():
    book_id = book_id_entry.get()
    cursor.execute('''SELECT * FROM books WHERE id=%s''', (book_id,))
    book = cursor.fetchone()
    if book:
        if book[3] == 'Issued':
            cursor.execute('''UPDATE books SET status=%s WHERE id=%s''', ('Available', book_id))
            conn.commit()
            messagebox.showinfo("Success", "Book returned successfully")
        else:
            messagebox.showerror("Error", "Book not issued")
    else:
        messagebox.showerror("Error", "Book not found")

def login():
    username = username_entry.get()
    password = password_entry.get()
    # Replace these credentials with your actual login credentials
    if username == "medhun" and password == "aaaa":
        login_window.destroy()
        root.deiconify()
    else:
        messagebox.showerror("Error", "Invalid username or password")

# GUI setup
root = tk.Tk()
root.title("Library Management System")
root.geometry("700x700")
root.withdraw()  # Hide the main window initially

# Load the background image
background_image = Image.open("pexels-itfeelslikefilm-590493 (1).jpg")
background_image = background_image.resize((700,700))  # Resize the image to fit the window
background_photo = ImageTk.PhotoImage(background_image)

# Create a label with the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(relx=0, rely=0, relwidth=1, relheight=1)  # Place the label in the entire window
background_label.lower()

# Label for "Rise and Shine Library"
heading_label = tk.Label(root, text="Rise and Shine Library", font=("Helvetica", 20),bg="orange")
heading_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

# Labels and Entry Widgets
title_label = tk.Label(root, text="Title:",bg="orange")
title_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
title_entry = tk.Entry(root)
title_entry.grid(row=1, column=1, padx=10, pady=5, sticky="W")

author_label = tk.Label(root, text="Author:",bg="orange")
author_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
author_entry = tk.Entry(root)
author_entry.grid(row=2, column=1, padx=10, pady=5, sticky="W")

add_button = tk.Button(root, text="Add Book", command=add_book, width=8)
add_button.grid(row=3, column=0, columnspan=2,padx=150, pady=10,sticky="WE")

book_id_label = tk.Label(root, text="Book ID:",bg="orange")
book_id_label.grid(row=4, column=0, padx=10, pady=5, sticky="E")
book_id_entry = tk.Entry(root)
book_id_entry.grid(row=4, column=1, padx=10, pady=5, sticky="W")

issue_button = tk.Button(root, text="Issue Book", command=issue_book)
issue_button.grid(row=5, column=0, columnspan=2,padx=150, pady=10, sticky="WE")

return_button = tk.Button(root, text="Return Book", command=return_book)
return_button.grid(row=6, column=0, columnspan=2,padx=150, pady=10, sticky="WE")

view_button = tk.Button(root, text="View Available Books", command=view_books)
view_button.grid(row=7, column=0, columnspan=2,padx=150, pady=10, sticky="WE")

delete_button = tk.Button(root, text="Delete Book", command=delete_book)
delete_button.grid(row=8, column=0, columnspan=2,padx=150, pady=10, sticky="WE")
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Create the login window
login_window = tk.Toplevel(root)
login_window.title("Library Management System Login")
login_window.geometry("400x300")

# Add background image
login_background_image = Image.open("pexels-ivo-rainha-527110-1290141 (1).jpg")
login_background_image= login_background_image.resize((400,300))
login_background_photo = ImageTk.PhotoImage(login_background_image)
login_background_label = tk.Label(login_window, image=login_background_photo)
login_background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Label for "Rise and Shine Library"
heading_labe2 = tk.Label(login_window, text="Rise and Shine Library", font=("Helvetica", 20),bg="orange")
heading_labe2.grid(row=0, column=2, columnspan=3, padx=10, pady=10, sticky="WE")

# Username label and entry
username_label = tk.Label(login_window, text="Username:",bg="orange")
username_label.grid(row=1, column=0, padx=10, pady=5, sticky="E")
username_entry = tk.Entry(login_window)
username_entry.grid(row=1, column=2, padx=10, pady=5, sticky="W")

# Password label and entry
password_label = tk.Label(login_window, text="Password:",bg="orange")
password_label.grid(row=2, column=0, padx=10, pady=5, sticky="E")
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=2, column=2, padx=10, pady=5, sticky="W")

# Login button
login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=4, column=2, columnspan=2, padx=20, pady=20, sticky="WE")

root.mainloop()
cursor.close()
conn.close()
