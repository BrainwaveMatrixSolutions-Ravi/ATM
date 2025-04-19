import tkinter as tk
from tkinter import messagebox
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="root", database="atmdb")
cursor = conn.cursor()

logged_in_user = None

def login():
    global logged_in_user
    acc_no = acc_entry.get()
    pin = pin_entry.get()

    cursor.execute("SELECT * FROM Users WHERE account_number=%s AND pin=%s", (acc_no, pin))
    user = cursor.fetchone()

    if user:
        logged_in_user = acc_no  
        messagebox.showinfo("Login Successful", "Welcome to the ATM!")
        main_menu()
    else:
        messagebox.showerror("Error", "Invalid Account Number or PIN")


def register():
    acc_no = reg_acc_entry.get()
    name = reg_name_entry.get()
    pin = reg_pin_entry.get()
    initial_deposit = reg_deposit_entry.get()

    if not acc_no.isdigit() or len(acc_no) != 10:
        messagebox.showerror("Error", "Account Number must be a 10-digit number!")
        return

    if len(pin) != 4 or not pin.isdigit():
        messagebox.showerror("Error", "PIN must be a 4-digit number!")
        return

    try:
        initial_deposit = float(initial_deposit)
        if initial_deposit < 0:
            messagebox.showerror("Error", "Initial deposit cannot be negative!")
            return
    except ValueError:
        messagebox.showerror("Error", "Enter a valid deposit amount!")
        return

    
    cursor.execute("SELECT * FROM Users WHERE account_number=%s", (acc_no,))
    if cursor.fetchone():
        messagebox.showerror("Error", "Account Number already exists!")
    else:
        cursor.execute("INSERT INTO Users (account_number, name, pin, balance) VALUES (%s, %s, %s, %s)", 
                       (acc_no, name, pin, initial_deposit))
        conn.commit()
        messagebox.showinfo("Success", "Account Registered Successfully! Please Login.")
        register_window.destroy()


def open_register_window():
    global register_window, reg_acc_entry, reg_name_entry, reg_pin_entry, reg_deposit_entry

    register_window = tk.Toplevel(root)
    register_window.title("Register")

    tk.Label(register_window, text="Account Number (10-digits):").pack()
    reg_acc_entry = tk.Entry(register_window)
    reg_acc_entry.pack()

    tk.Label(register_window, text="Full Name:").pack()
    reg_name_entry = tk.Entry(register_window)
    reg_name_entry.pack()

    tk.Label(register_window, text="Set PIN (4-digits):").pack()
    reg_pin_entry = tk.Entry(register_window, show="*")
    reg_pin_entry.pack()

    tk.Label(register_window, text="Initial Deposit:").pack()
    reg_deposit_entry = tk.Entry(register_window)
    reg_deposit_entry.pack()

    tk.Button(register_window, text="Register", command=register).pack()


def check_balance():
    cursor.execute("SELECT balance FROM Users WHERE account_number=%s", (logged_in_user,))
    balance = cursor.fetchone()[0]
    messagebox.showinfo("Balance", f"Your current balance is ${balance:.2f}")


def deposit():
    try:
        amount = float(amount_entry.get())
        cursor.execute("UPDATE Users SET balance = balance + %s WHERE account_number=%s", (amount, logged_in_user))
        conn.commit()
        cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, 'deposit', %s)", (logged_in_user, amount))
        conn.commit()
        messagebox.showinfo("Success", f"${amount:.2f} deposited successfully")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")


def withdraw():
    try:
        amount = float(amount_entry.get())
        cursor.execute("SELECT balance FROM Users WHERE account_number=%s", (logged_in_user,))
        balance = cursor.fetchone()[0]

        if amount > balance:
            messagebox.showerror("Error", "Insufficient Balance")
        else:
            cursor.execute("UPDATE Users SET balance = balance - %s WHERE account_number=%s", (amount, logged_in_user))
            conn.commit()
            cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, 'withdraw', %s)", (logged_in_user, amount))
            conn.commit()
            messagebox.showinfo("Success", f"${amount:.2f} Withdrawn Successfully")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")


def transfer():
    try:
        recipient_acc = recipient_entry.get()
        amount = float(amount_entry.get())

        cursor.execute("SELECT balance FROM Users WHERE account_number=%s", (logged_in_user,))
        sender_balance = cursor.fetchone()[0]

        cursor.execute("SELECT * FROM Users WHERE account_number=%s", (recipient_acc,))
        recipient_exists = cursor.fetchone()

        if not recipient_exists:
            messagebox.showerror("Error", "Recipient account not found.")
            return

        if amount > sender_balance:
            messagebox.showerror("Error", "Insufficient Balance!")
        else:
            cursor.execute("UPDATE Users SET balance = balance - %s WHERE account_number=%s", (amount, logged_in_user))
            cursor.execute("UPDATE Users SET balance = balance + %s WHERE account_number=%s", (amount, recipient_acc))
            conn.commit()
            cursor.execute("INSERT INTO transactions (account_number, transaction_type, amount) VALUES (%s, 'transfer', %s)", (logged_in_user, amount))
            conn.commit()
            messagebox.showinfo("Success", f"${amount:.2f} Transferred Successfully to {recipient_acc}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")


def main_menu():
    global amount_entry, recipient_entry, pin_entry

    login_frame.destroy()  # Destroy login screen
    menu_frame = tk.Frame(root)
    menu_frame.pack()

    tk.Label(menu_frame, text="ATM Main Menu", font=("Arial", 17, "bold")).pack()

    tk.Button(menu_frame, text="Check Balance", command=check_balance).pack()

    tk.Label(menu_frame, text="Enter Amount:").pack()
    amount_entry = tk.Entry(menu_frame)
    amount_entry.pack()

    tk.Button(menu_frame, text="Deposit", command=deposit).pack()
    tk.Button(menu_frame, text="Withdraw", command=withdraw).pack()

    tk.Label(menu_frame, text="Enter Recipient Account No:").pack()
    recipient_entry = tk.Entry(menu_frame)
    recipient_entry.pack()

    tk.Button(menu_frame, text="Transfer Money", command=transfer).pack()

root = tk.Tk()
root.title("ATM Interface")

login_frame = tk.Frame(root)
login_frame.pack()

tk.Label(login_frame, text="Enter Account Number:").pack()
acc_entry = tk.Entry(login_frame)
acc_entry.pack()

tk.Label(login_frame, text="Enter PIN:").pack()
pin_entry = tk.Entry(login_frame, show="*")
pin_entry.pack()

tk.Button(login_frame, text="Login", command=login).pack()
tk.Button(login_frame, text="Register", command=open_register_window).pack()  

root.mainloop()