import mysql.connector
import random
import re

# Database setup
def initialize_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mohi@@ni@@Sharma2307",
        database="banking_system"
    )
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS banking_system")
    cursor.execute("USE banking_system")

    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        account_number VARCHAR(10) UNIQUE NOT NULL,
                        dob DATE NOT NULL,
                        city VARCHAR(255) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        balance DECIMAL(15, 2) NOT NULL CHECK (balance >= 2000),
                        contact_number VARCHAR(10) NOT NULL,
                        email VARCHAR(255) NOT NULL,
                        address TEXT NOT NULL,
                        active BOOLEAN DEFAULT TRUE
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        account_number VARCHAR(10) NOT NULL,
                        type VARCHAR(50) NOT NULL,
                        amount DECIMAL(15, 2) NOT NULL,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(account_number) REFERENCES users(account_number)
                    )''')

    conn.commit()
    conn.close()

# Helper functions
def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def validate_password(password):
    if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"[a-z]", password) or not re.search(r"[0-9]", password) or not re.search(r"[@$!%*?&]", password):
        return False
    return True

def validate_email(email):
    return re.match(r"[^@\s]+@[^@\s]+\.[^@\s]+", email)

def validate_contact(contact):
    return re.match(r"^[0-9]{10}$", contact)

# User functions
def add_user():
    name = input("Enter name: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    city = input("Enter city: ")
    address = input("Enter address: ")

    while True:
        password = input("Enter password: ")
        if validate_password(password):
            break
        print("Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.")

    while True:
        contact = input("Enter contact number: ")
        if validate_contact(contact):
            break
        print("Invalid contact number. Must be 10 digits.")

    while True:
        email = input("Enter email: ")
        if validate_email(email):
            break
        print("Invalid email format.")

    while True:
        initial_balance = float(input("Enter initial balance (minimum 2000): "))
        if initial_balance >= 2000:
            break
        print("Initial balance must be at least 2000.")

    account_number = generate_account_number()

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mohi@@ni@@Sharma2307",
        database="banking_system"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, account_number, dob, city, password, balance, contact_number, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                   (name, account_number, dob, city, password, initial_balance, contact, email, address))
    conn.commit()
    conn.close()

    print(f"User added successfully! Account Number: {account_number}")

def show_users():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mohi@@ni@@Sharma2307",
        database="banking_system"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, account_number, dob, city, balance, contact_number, email, address, active FROM users")
    users = cursor.fetchall()
    conn.close()

    for user in users:
        status = "Active" if user[8] else "Inactive"
        print(f"Name: {user[0]}\nAccount Number: {user[1]}\nDOB: {user[2]}\nCity: {user[3]}\nBalance: {user[4]}\nContact: {user[5]}\nEmail: {user[6]}\nAddress: {user[7]}\nStatus: {status}\n{'-' * 40}")

def login():
    account_number = input("Enter account number: ")
    password = input("Enter password: ")

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mohi@@ni@@Sharma2307",
        database="banking_system"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT balance, active FROM users WHERE account_number = %s AND password = %s", (account_number, password))
    user = cursor.fetchone()

    if user:
        if not user[1]:
            print("Account is deactivated. Please contact the bank.")
        else:
            print("Login successful!")
            while True:
                print("\n1. Show Balance")
                print("2. Credit Amount")
                print("3. Debit Amount")
                print("4. Transfer Amount")
                print("5. Change Password")
                print("6. Update Profile")
                print("7. Logout")

                choice = input("Enter your choice: ")

                if choice == "1":
                    print(f"Your balance is: {user[0]}")
                elif choice == "2":
                    amount = float(input("Enter amount to credit: "))
                    cursor.execute("UPDATE users SET balance = balance + %s WHERE account_number = %s", (amount, account_number))
                    cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'credit', %s)", (account_number, amount))
                    conn.commit()
                    print("Amount credited successfully.")
                elif choice == "3":
                    amount = float(input("Enter amount to debit: "))
                    if amount > user[0]:
                        print("Insufficient balance.")
                    else:
                        cursor.execute("UPDATE users SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
                        cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'debit', %s)", (account_number, amount))
                        conn.commit()
                        print("Amount debited successfully.")
                elif choice == "4":
                    target_account = input("Enter target account number: ")
                    amount = float(input("Enter amount to transfer: "))
                    if amount > user[0]:
                        print("Insufficient balance.")
                    else:
                        cursor.execute("UPDATE users SET balance = balance - %s WHERE account_number = %s", (amount, account_number))
                        cursor.execute("UPDATE users SET balance = balance + %s WHERE account_number = %s", (amount, target_account))
                        cursor.execute("INSERT INTO transactions (account_number, type, amount) VALUES (%s, 'transfer', %s)", (account_number, amount))
                        conn.commit()
                        print("Amount transferred successfully.")
                elif choice == "5":
                    new_password = input("Enter new password: ")
                    if validate_password(new_password):
                        cursor.execute("UPDATE users SET password = %s WHERE account_number = %s", (new_password, account_number))
                        conn.commit()
                        print("Password changed successfully.")
                    else:
                        print("Invalid password format.")
                elif choice == "6":
                    city = input("Enter new city: ")
                    address = input("Enter new address: ")
                    contact = input("Enter new contact number: ")
                    email = input("Enter new email: ")

                    if validate_contact(contact) and validate_email(email):
                        cursor.execute("UPDATE users SET city = ?, address = ?, contact_number = ?, email = ? WHERE account_number = ?",
                                       (city, address, contact, email, account_number))
                        conn.commit()
                        print("Profile updated successfully.")
                    else:
                        print("Invalid contact number or email format.")
                elif choice == "7":
                    print("Logged out successfully.")
                    break
                else:
                    print("Invalid choice. Please try again.")
    else:
        print("Invalid account number or password.")

    conn.close()

# Main program
def main():
    initialize_database()
    while True:
        print("\nBANKING SYSTEM")
        print("1. Add User")
        print("2. Show Users")
        print("3. Login")
        print("4. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            add_user()
        elif choice == "2":
            show_users()
        elif choice == "3":
             login()
        elif choice == "4":
            exit()
main()
    