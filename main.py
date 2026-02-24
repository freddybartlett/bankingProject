import tkinter as tk
import sqlite3
import time
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

    def getUserBalance(self,username):
        self.cursor.execute("SELECT balance FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        return f"£{result[0]:.2f}"


class Account:
    def __init__(self,username,balance):
        self.username = username
        self.balance = balance

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

        currentBalance = self.db.getUserBalance(self.auth.currentUser)
        self.greetingLabel = tk.Label(self,text=f"Hello, {self.auth.currentUser}, your balance is {currentBalance}",font=("Arial",20))
        self.greetingLabel.place(x="0",y="40")


app = App()
app.mainloop()


