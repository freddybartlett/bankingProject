import tkinter as tk
import sqlite3
import hashlib as h

class ManageDatabase:
    def __init__(self):
        self.conn = sqlite3.connect("banking.db")
        self.cursor = self.conn.cursor()
        self.createTable()

    def createTable(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                balance REAL DEFAULT 0.00
        )''')

    def hashPassword(self,enteredPassword):
        return h.sha256(enteredPassword.encode()).hexdigest()

    def addUser(self, enteredUsername, enteredPassword):
        hashedPassword = self.hashPassword(enteredPassword)
        self.cursor.execute("INSERT INTO users (username, password) VALUES (?,?)", (enteredUsername, hashedPassword))
        self.conn.commit()

    def getUserData(self,enteredUsername):
        self.cursor.execute("SELECT username,password,balance FROM users WHERE username = ?",(enteredUsername,))
        return self.cursor.fetchone()

    def getUserBalanceString(self,username):
        self.cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return f"£{result[0]:.2f}"

    def getUserBalanceFloat(self,username):
        self.cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return result[0]

    def updateBalance(self,newBalance,username):
        self.cursor.execute("UPDATE users SET balance = ? WHERE username = ?",(newBalance,username))
        self.conn.commit()

class ManageAuth:
    def __init__(self):
        self.db = ManageDatabase()
        self.currentUser = None

    def validateLogin(self, enteredUsername, enteredPassword):
        if enteredUsername == "" and enteredPassword == "":
            return False,"Please enter a username and password"
        elif enteredUsername == "":
            return False,"Please enter a username"
        elif enteredPassword == "":
            return False,"Please enter a password"
        userData = self.db.getUserData(enteredUsername)
        if userData is None:
            return False, "User does not exist"
        dbUser,dbHashedPassword,dbBalance = userData
        enteredhashedPassword = self.db.hashPassword(enteredPassword)
        if enteredhashedPassword == dbHashedPassword:
            self.currentUser = enteredUsername
            return True,""
        else:
            return False,"Invalid username or password"

    def validateAccountCreation(self, enteredUsername, enteredPassword):
        if enteredUsername == "" and enteredPassword == "":
            return False, "Please enter a username and password"
        elif enteredUsername == "":
            return False, "Please enter a username"
        elif enteredPassword == "":
            return False, "Please enter a password"
        else:
            self.db.addUser(enteredUsername,enteredPassword)
            return True,""


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.db = ManageDatabase()
        self.auth = ManageAuth()

        self.title("Banking application")
        self.geometry("700x500")
        self.displayLogin()
        self.resizable(width=False, height=False)

    def clearGUI(self):
        for widget in self.winfo_children():
            widget.destroy()

    def displayLogin(self):
        self.clearGUI()

        self.loginLabel = tk.Label(self, text="Log in to online banking", font=("Arial bold", 30))
        self.loginLabel.place(x="0", y="0")

        self.usernameLabel = tk.Label(self, text="Username:", font=("Arial", 20))
        self.usernameLabel.place(x="0", y="50")
        self.usernameEntry = tk.Entry(self, font=("Arial", 20))
        self.usernameEntry.place(x="150", y="50", height=40, width=304)

        self.passwordLabel = tk.Label(self, text="Password:", font=("Arial", 20))
        self.passwordLabel.place(x="0", y="90")
        self.passwordEntry = tk.Entry(self, font=("Arial", 20), show="*")
        self.passwordEntry.place(x="150", y="90", height=40, width=304)

        self.loginButton = tk.Button(self, text="Login", font=("Arial", 20),command=lambda: self.manageLogin(self.usernameEntry.get(),self.passwordEntry.get()))
        self.loginButton.place(x="227", y="135", height=40, width=80)

        self.createAccountButton = tk.Button(self,text="Create new account", font=("Arial",20),command=self.displayAccountCreation)
        self.createAccountButton.place(x="25",y="400",height=80,width=260)

    def manageError(self, errorMessage,loginPage):
        self.clearGUI()
        if loginPage == True:
            self.displayLogin()
        else:
            self.displayAccountCreation()
        self.errorLabel = tk.Label(self, text=errorMessage, font=("Arial", 20), fg="red")
        self.errorLabel.place(x="0", y="170")

    def manageLogin(self, enteredUsername, enteredPassword):
        validated,errorMessage = self.auth.validateLogin(enteredUsername,enteredPassword)
        if validated == True:
            self.displayDashboard()
        else:
            self.manageError(errorMessage,True)

    def manageAccountCreation(self,enteredUsername,enteredPassword):
        validated,errorMessage = self.auth.validateAccountCreation(enteredUsername,enteredPassword)
        if validated == True:
            self.accountCreationConfirmationLabel = tk.Label(self, text="Account creation successful, redirecting to login page", font=("Arial", 20), fg="green")
            self.accountCreationConfirmationLabel.place(x="0",y="170")
            self.after(3000,self.displayLogin)
        else:
            self.manageError(errorMessage,False)

    def displayAccountCreation(self):
        self.clearGUI()

        self.createAccountLabel = tk.Label(self, text="Create an online banking account", font=("Arial bold", 30))
        self.createAccountLabel.place(x="0", y="0")

        self.usernameLabel = tk.Label(self, text="Username:", font=("Arial", 20))
        self.usernameLabel.place(x="0", y="50")
        self.usernameEntry = tk.Entry(self, font=("Arial", 20))
        self.usernameEntry.place(x="150", y="50", height=40, width=304)

        self.passwordLabel = tk.Label(self, text="Password:", font=("Arial", 20))
        self.passwordLabel.place(x="0", y="90")
        self.passwordEntry = tk.Entry(self, font=("Arial", 20), show="*")
        self.passwordEntry.place(x="150", y="90", height=40, width=304)

        self.accountCreationButton = tk.Button(self, text="Create account", font=("Arial", 20),command=lambda: self.manageAccountCreation(self.usernameEntry.get(),self.passwordEntry.get()))
        self.accountCreationButton.place(x="152", y="135", height=40, width=200)

        self.createAccountButton = tk.Button(self, text="Log in to online banking", font=("Arial", 20),command=self.displayLogin)
        self.createAccountButton.place(x="25", y="400", height=80, width=300)

    def displayDashboard(self):
        self.clearGUI()

        self.titleLabel = tk.Label(self,text="Online banking dashboard",font=("Arial bold", 30))
        self.titleLabel.place(x="0",y="0")

        currentBalance = self.db.getUserBalanceString(self.auth.currentUser)
        self.greetingLabel = tk.Label(self,text=f"Hello, {self.auth.currentUser}, your balance is {currentBalance}",font=("Arial",20))
        self.greetingLabel.place(x="0",y="50")

        self.depositButton = tk.Button(self,text="Deposit money",font=("Arial",20), command=self.displayDeposit)
        self.depositButton.place(x="0",y="100",height=40,width=300)

        self.withdrawButton = tk.Button(self,text="Withdraw money",font=("Arial",20), command=self.displayWithdraw)
        self.withdrawButton.place(x="0",y="150",height=40,width=300)

    def displayDeposit(self):
        self.clearGUI()

        self.depositWindowLabel = tk.Label(self,text="Deposit money",font=("Arial bold",30))
        self.depositWindowLabel.place(x="0",y="0")

        self.depositEntry = tk.Entry(self,font=("Arial", 20))
        self.depositEntry.place(x="10",y="60")

        self.depositButton = tk.Button(self,text="Deposit",font=("Arial",20),command=lambda:self.manageDeposit(self.depositEntry.get()))
        self.depositButton.place(x="13",y="100",height=40,width=300)

        self.returnDashboardButton = tk.Button(self,text="Return to dashboard",font=("Arial",20),command=self.displayDashboard)
        self.returnDashboardButton.place(x="25",y="400",height=80,width=300)


    def displayWithdraw(self):
        self.clearGUI()

        self.withdrawWindowLabel = tk.Label(self, text="Withdraw money", font=("Arial bold", 30))
        self.withdrawWindowLabel.place(x="0", y="0")

        self.withdrawEntry = tk.Entry(self,font=("Arial",20))
        self.withdrawEntry.place(x="10",y="60")

        self.withdrawButton = tk.Button(self,text="Withdraw",font=("Arial",20),command=lambda:self.manageWithdraw(self.withdrawEntry.get()))
        self.withdrawButton.place(x="13",y="100",height=40,width=300)

        self.returnDashboardButton = tk.Button(self, text="Return to dashboard", font=("Arial", 20),command=self.displayDashboard)
        self.returnDashboardButton.place(x="25", y="400", height=80, width=300)

    def manageDeposit(self,deposit):
        try:
            deposit = float(deposit)
            if deposit <= 0:
                self.displayDeposit()
                self.errorLabel = tk.Label(self, text="Please enter a valid amount (greater than 0)", font=("Arial", 20), fg="red")
                self.errorLabel.place(x="0", y="140")
            else:
                amount = self.db.getUserBalanceFloat(self.auth.currentUser)
                amount += deposit
                self.db.updateBalance(amount,self.auth.currentUser)
                self.displayDeposit()
                self.successLabel = tk.Label(self,text=f"Deposit successful, your balance is now £{amount}",font=("Arial",20),fg="green")
                self.successLabel.place(x="0",y="140")
        except ValueError:
            self.displayDeposit()
            self.errorLabel = tk.Label(self,text="Please enter a valid number",font=("Arial", 20), fg="red")
            self.errorLabel.place(x="0",y="140")

    def manageWithdraw(self,withdraw):
        try:
            withdraw = float(withdraw)
            if withdraw <= 0:
                self.displayWithdraw()
                self.errorLabel = tk.Label(self, text="Please enter a valid amount (greater than 0)",font=("Arial", 20), fg="red")
                self.errorLabel.place(x="0", y="140")
            else:
                amount = self.db.getUserBalanceFloat(self.auth.currentUser)
                amount -= withdraw
                if amount < 0:
                    self.displayWithdraw()
                    self.errorLabel = tk.Label(self, text="Cannot withdraw more than the current balance",font=("Arial", 20), fg="red")
                    self.errorLabel.place(x="0", y="140")
                else:
                    self.db.updateBalance(amount, self.auth.currentUser)
                    self.displayWithdraw()
                    self.successLabel = tk.Label(self, text=f"Withdraw successful, your balance is now £{amount}",font=("Arial", 20), fg="green")
                    self.successLabel.place(x="0", y="140")
        except ValueError:
            self.displayWithdraw()
            self.errorLabel = tk.Label(self, text="Please enter a valid number", font=("Arial", 20), fg="red")
            self.errorLabel.place(x="0", y="140")

app = App()
app.mainloop()


