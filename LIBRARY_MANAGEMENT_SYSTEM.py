import json
from datetime import datetime, timedelta

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
        # Implement logic for checking out a book
        if self.book.quantity > 0:
            self.book.quantity -= 1
            self.patron.borrow_book(self.book)
            self.due_date = datetime.now() + timedelta(days=14)  # Due in 14 days
        else:
            print("Sorry, the book is out of stock.")

    def return_book(self):
        # Implement logic for returning a book
        if self.book in self.patron.borrowed_books:
            self.book.quantity += 1
            self.patron.return_book(self.book)
        else:
            print("This book was not borrowed by the patron.")

    def calculate_fine(self):
        # Implement logic for calculating fines (if applicable)
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
        # Implement search functionality
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
        # Implement logic for handling transactions
        transaction.checkout_book()  # Assuming it's a checkout transaction by default

    def generate_reports(self):
        # Implement report generation functionality
        pass

    def save_data(self, file_name):
        # Implement data persistence using JSON or other file-based systems
        data = {
            'books': [book.to_dict() for book in self.books],
            'patrons': [patron.to_dict() for patron in self.patrons],
            'transactions': [transaction.to_dict() for transaction in self.transactions]
        }
        with open(file_name, 'w') as file:
            json.dump(data, file)

    def load_data(self, file_name):
        # Implement loading data from file
        with open(file_name, 'r') as file:
            data = json.load(file)
            self.books = [Book(**book_data) for book_data in data['books']]
            self.patrons = [Patron(**patron_data) for patron_data in data['patrons']]
            self.transactions = [Transaction(**transaction_data) for transaction_data in data['transactions']]

    # Additional methods for managing patrons, transactions, and reports can be implemented here



# Sample usage:
library = Library()

titlebook=input("Input the title of the book")
authorbook=input("Input the author of the book")
isbnbook=input("Enter the ISBN code of the book")
qtbook=input("Enter the quantity of books taken")

book1 = Book(titlebook, authorbook, isbnbook, qtbook)

patronname=input("Enter patron name")
patronID=input("Enter patron ID")
patroncontact=input("Enter patron contact information")

patron1 = Patron(patronname, patronID, patroncontact)

transaction1 = Transaction(book1, patron1)
library.add_book(book1)
library.add_patron(patron1)
library.handle_transaction(transaction1)
# Save data to a file
library.save_data('library_data.json')

# Load data from a file
library.load_data('library_data.json')

# Perform transactions
transaction1 = Transaction(book1, patron1)
library.handle_transaction(transaction1)

