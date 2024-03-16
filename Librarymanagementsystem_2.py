import json
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

class Book:
    def __init__(self, title, author, isbn, quantity):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity

    def display_details(self):
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"ISBN: {self.isbn}")
        print(f"Quantity: {self.quantity}")

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'quantity': self.quantity
        }

class Patron:
    def __init__(self, name, id, contact_info):
        self.name = name
        self.id = id
        self.contact_info = contact_info
        self.borrowed_books = []

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"ID: {self.id}")
        print(f"Contact Information: {self.contact_info}")

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'contact_info': self.contact_info,
            'borrowed_books': [book.to_dict() for book in self.borrowed_books]
        }

class Transaction:
    def __init__(self, book, patron, due_date=None):
        self.book = book
        self.patron = patron
        self.due_date = due_date

    def checkout_book(self):
        if self.book.quantity > 0:
            self.book.quantity -= 1
            self.patron.borrow_book(self.book)
            self.due_date = datetime.now() + timedelta(days=14)  # Due in 14 days
        else:
            print("Sorry, the book is out of stock.")

    def return_book(self):
        if self.book in self.patron.borrowed_books:
            self.book.quantity += 1
            self.patron.return_book(self.book)
        else:
            print("This book was not borrowed by the patron.")

    def calculate_fine(self):
        pass

    def to_dict(self):
        return {
            'book': self.book.to_dict(),
            'patron': self.patron.to_dict(),
            'due_date': str(self.due_date)
        }

class Library:
    def __init__(self):
        self.books = []
        self.patrons = []
        self.transactions = []

    def search_books(self, title):
        found_books = [book for book in self.books if title.lower() in book.title.lower()]
        return found_books

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, book):
        self.books.remove(book)

    def add_patron(self, patron):
        self.patrons.append(patron)

    def remove_patron(self, patron):
        self.patrons.remove(patron)

    def handle_transaction(self, transaction):
        self.transactions.append(transaction)
        transaction.checkout_book()

    def generate_reports(self):
        pass

    def save_data(self, file_name):
        data = {
            'books': [book.to_dict() for book in self.books],
            'patrons': [patron.to_dict() for patron in self.patrons],
            'transactions': [transaction.to_dict() for transaction in self.transactions]
        }
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def load_data(self, file_name):
        with open(file_name, 'r') as file:
            data = json.load(file)
            self.books = [Book(**book_data) for book_data in data['books']]
            self.patrons = [Patron(**patron_data) for patron_data in data['patrons']]
            self.transactions = [Transaction(**transaction_data) for transaction_data in data['transactions']]

    def retrieve_books_info(self):
        book_info = ""
        for book in self.books:
            book_info += f"Title: {book.title}\nAuthor: {book.author}\nISBN: {book.isbn}\nQuantity: {book.quantity}\n\n"
        return book_info

    def display_books_info(self):
        info_window = tk.Toplevel()
        info_window.title("Library Books Information")

        book_info_label = tk.Label(info_window, text=self.retrieve_books_info())
        book_info_label.pack()

        close_button = tk.Button(info_window, text="Close", command=info_window.destroy)
        close_button.pack()

    def run_ui(self):
        self.window = tk.Tk()
        self.window.title("Library Management System")

        tk.Button(self.window, text="Add Book", command=self.add_book_ui).grid(row=0, column=0)
        tk.Button(self.window, text="Display Books Info", command=self.display_books_info).grid(row=0, column=1)

        self.window.mainloop()

    def add_book_ui(self):
        add_book_window = tk.Toplevel(self.window)
        add_book_window.title("Add Book")

        tk.Label(add_book_window, text="Book Title:").grid(row=0, column=0)
        tk.Label(add_book_window, text="Author:").grid(row=1, column=0)
        tk.Label(add_book_window, text="ISBN:").grid(row=2, column=0)
        tk.Label(add_book_window, text="Quantity:").grid(row=3, column=0)

        title_entry = tk.Entry(add_book_window)
        author_entry = tk.Entry(add_book_window)
        isbn_entry = tk.Entry(add_book_window)
        quantity_entry = tk.Entry(add_book_window)

        title_entry.grid(row=0, column=1)
        author_entry.grid(row=1, column=1)
        isbn_entry.grid(row=2, column=1)
        quantity_entry.grid(row=3, column=1)

        add_button = tk.Button(add_book_window, text="Add", command=lambda: self.add_book_from_ui(add_book_window, title_entry, author_entry, isbn_entry, quantity_entry))
        add_button.grid(row=4, column=0, columnspan=2)

    def add_book_from_ui(self, add_book_window, title_entry, author_entry, isbn_entry, quantity_entry):
        title = title_entry.get()
        author = author_entry.get()
        isbn = isbn_entry.get()
        quantity = int(quantity_entry.get())

        new_book = Book(title, author, isbn, quantity)
        self.add_book(new_book)

        messagebox.showinfo("Success", "Book added successfully.")

        add_book_window.destroy()
        self.save_data('library_data.json')

if __name__ == "__main__":
    library = Library()
    library.run_ui()
