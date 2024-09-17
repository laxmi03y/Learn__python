import datetime

import mysql.connector
import pandas as pd
import pdfkit
from tabulate import tabulate


class Transaction_Type:
    pass


class ATM:
    def __init__(self):
        # Initialize database connection and cursor
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="atmmanagment"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as e:
            print(f"Error: {e}")
            raise

        self.current_user = None  # Keep track of the currently logged-in user

    def signup_user(self, First_name, Last_name, User_name, Password, Initial_Amount):
        try:
            query = '''INSERT INTO Users 
                       (First_name, Last_name, User_name, Password, Initial_Amount, Current_Balance) 
                       VALUES (%s, %s, %s, %s, %s, %s)'''
            self.cursor.execute(query, (First_name, Last_name, User_name, Password, Initial_Amount))
            self.conn.commit()
            print("Signup Successful")
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def login(self, User_name, Password):
        try:
            query = "SELECT Password, Current_Balance,id FROM Users WHERE User_name = %s"
            self.cursor.execute(query, (User_name,))
            result = self.cursor.fetchone()

            if result and result[0] == Password:
                self.current_user = User_name
                self.balance = result[1]
                self.user_id = result[2]
                print("Login successful!")
            else:
                print("Invalid username or password.")
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def display_balance(self):
        if self.current_user:
            print(f"Your current balance is {self.balance}")
        else:
            print("You need to login first.")

    def deposit_amt(self, amt):
        if amt > 0:
            print("inside deposit_amt")
            self.balance += amt
            self.update_balance_in_db(self.balance, amt, "Deposit")
            print(f"Deposited {amt} into your account.")
        else:
            print("Invalid amount")

    def withdraw_amt(self, amt):
        if amt > 0:
            if amt <= self.balance:
                self.balance -= amt
                self.update_balance_in_db(self.balance, amt, "Withdraw")
                print(f"Withdrew {amt} from your account.")
            else:
                print("Insufficient funds.")
        else:
            print("Invalid amount")

    def update_balance_in_db(self, curr_balance, amt, transaction_type):
        try:
            print("inside update_balance_in_db ")
            query = "UPDATE Users SET Current_Balance = %s WHERE id = %s"
            self.cursor.execute(query, (curr_balance, self.user_id))

            self.record_transaction(transaction_type, amt)

            self.conn.commit()

        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def record_transaction(self, transaction_type, amt):
        try:
            print("inside record_transaction ")
            query = '''INSERT INTO Transaction 
                       (User_ID, Transaction_Type, Amount,Transaction_Date) 
                       VALUES (%s, %s, %s, %s)'''
            self.cursor.execute(query, (self.user_id, transaction_type, amt, datetime.datetime.now()))
            self.conn.commit()
        except mysql.connector.Error as e:
            print(f"Error: {e}")

    def show_transaction(self, user_id):
        try:
            query = """
            SELECT Transaction_ID, Transaction_Type, Amount, Transaction_Date
            FROM transaction
            WHERE User_ID = %s
            ORDER BY Transaction_Date DESC;
            """
            self.cursor.execute(query, (user_id,))
            transaction = self.cursor.fetchall()
            df = pd.DataFrame(transaction, columns=['ID', 'Type', 'Amount', 'Date & Time'])

            # Format Date & Time column
            df['Date & Time'] = df['Date & Time'].dt.strftime('%Y-%m-%d %H:%M:%S')


            # Save DataFrame to CSV
            csv_filename = f"transactions_for_{self.user_id}.csv"
            df.to_csv(csv_filename, index=False)

            # Print the DataFrame using tabulate
            print(tabulate(df, headers='keys', tablefmt='pretty', showindex=False))
            # print(transaction)
            print("Show transactions")
        except mysql.connector.Error as e:
            print(f"Error: {e}")
    def main_menu(self):
        while True:
            print("\nATM Menu")
            print("1. Login")
            print("2. Signup")
            print("3. Quit")

            choice = input("Select an option (1-3): ")

            if choice == '1':
                User_name = input("Enter User_name: ")
                Password = input("Enter Password: ")
                self.login(User_name, Password)
                if self.current_user:
                    self.user_menu()
            elif choice == '2':
                First_name = input("Enter First_name: ")
                Last_name = input("Enter Last_name: ")
                User_name = input("Enter User_name: ")
                Password = input("Enter Password: ")
                try:
                    Initial_Amount = float(input("Enter Initial Amount: "))
                    self.signup_user(First_name, Last_name, User_name, Password, Initial_Amount)
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            elif choice == '3':
                print("Thank you for using the ATM.")
                break
            else:
                print("Invalid option. Please select a valid option.")

    def user_menu(self):
        while True:
            print("\nUser Menu")
            print("1. Display Balance")
            print("2. Deposit Amount")
            print("3. Withdraw Amount")
            print("4. show transaction")

            print("5. Logout")

            choice = input("Select an option (1-5): ")

            if choice == '1':
                self.display_balance()
            elif choice == '2':
                try:
                    amt = float(input("Enter amount to deposit: "))

                    self.deposit_amt(amt)
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            elif choice == '3':
                try:
                    amt = float(input("Enter amount to withdraw: "))
                    self.withdraw_amt(amt)
                except ValueError:
                    print("Invalid amount. Please enter a numeric value.")
            elif choice == '4':
                self.show_transaction(self.user_id)

            elif choice == '5 ':
                self.current_user = None
                print("Logged out successfully.")
                break
            else:
                print("Invalid option. Please select a valid option.")


if __name__ == "__main__":
    atm = ATM()
    atm.main_menu()
