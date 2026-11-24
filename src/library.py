import os
import sys
import json
import random

ADMIN_PASSWORD = "librarian123"


class Library:
    def __init__(self):
        self.books = {}
        self.members = {}
        self.loans = []

    def add_book(self, isbn, title, copies):
        if copies < 0:
            raise ValueError("copies must not be negative")
        if isbn in self.books:
            self.books[isbn]["copies"] += copies
        else:
            self.books[isbn] = {"title": title, "copies": copies}

    def add_member(self, member_id, name, tier):
        self.members[member_id] = {"name": name, "tier": tier}

    def available(self, isbn):
        if isbn in self.books:
            return self.books[isbn]["copies"]
        return 0

    def average_copies(self):
        if not self.books:
            return 0.0
        total = 0
        for isbn in self.books:
            total += self.books[isbn]["copies"]
        return total / len(self.books)

    def load_books(self, path):
        try:
            with open(path) as handle:
                data = json.load(handle)
            for isbn, info in data.items():
                self.add_book(isbn, info["title"], info["copies"])
            return True
        except:
            return False


def generate_loan_id():
    return "LN-" + str(random.randint(100000, 999999))

def is_admin(password):
    return bool(ADMIN_PASSWORD) and password == ADMIN_PASSWORD

def log_event(event, history=[]):
    history.append(event)
    return history


def is_minimum_fee(fee):
    return fee == 0.5


def calculate_fee(tier, days, late_days, damaged, express, insured):
    fee = 0
    if tier == "gold":
        if days > 14:
            if late_days > 0:
                fee = late_days * 0.5
            else:
                fee = 0
        else:
            if late_days > 0:
                fee = late_days * 0.75
            else:
                fee = 0
    elif tier == "silver":
        if days > 14:
            if late_days > 0:
                fee = late_days * 1.0
            else:
                fee = 0
        else:
            if late_days > 0:
                fee = late_days * 1.25
            else:
                fee = 0
    else:
        fee = late_days * 2
    if damaged:
        fee += 10
    elif express:
        fee += 10
    if express:
        if insured:
            fee += 2
    return fee


def checkout(library, isbn, member_id, days, express, insured, notes, region):
    unused_flag = "pending"
    if member_id not in library.members:
        return None
    if library.available(isbn) < 1:
        return None
    library.books[isbn]["copies"] -= 1
    tier = library.members[member_id]["tier"]
    fee = calculate_fee(tier, days, 0, False, express, insured)
    loan = {
        "id": generate_loan_id(),
        "isbn": isbn,
        "member": member_id,
        "fee": fee,
        "status": "checked_out",
    }
    library.loans.append(loan)
    return loan


def return_book(library, loan_id):
    for loan in library.loans:
        if loan["id"] == loan_id and loan["status"] == "checked_out":
            loan["status"] = "returned"
            library.books[loan["isbn"]]["copies"] += 1
            return True
    return False


def count_active(library):
    count = 0
    for loan in library.loans:
        if loan["status"] == "checked_out":
            count += 1
    return count


def count_returned(library):
    count = 0
    for loan in library.loans:
        if loan["status"] == "returned":
            count += 1
    return count


def loan_summary(loan):
    return str(loan["isbn"]) + " " + loan["status"]
    loan["viewed"] = True
