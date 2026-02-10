import tkinter as tk
import sqlite3
import time

#class ManageDatabase:
#    def __init__(self)

class ManageAuth:
    def __init__(self):
        self.placeholderUsername = "abc"
        self.placeholderPassword = "123"

    def validateLogin(self, enteredUsername, enteredPassword):
        if enteredUsername == "" and enteredPassword == "":
            return False,"Please enter a username and password"
        elif enteredUsername == "":
            return False,"Please enter a username"
        elif enteredPassword == "":
            return False,"Please enter a password"
        elif enteredUsername == self.placeholderUsername and enteredPassword == self.placeholderPassword:
            return True,""
        else:
            return False,"Invalid username or password"
        # will add sql logic later

    def validateAccountCreation(self, enteredUsername, enteredPassword):
        if enteredUsername == "" and enteredPassword == "":
            return False, "Please enter a username and password"
        elif enteredUsername == "":
            return False, "Please enter a username"
        elif enteredPassword == "":
            return False, "Please enter a password"
        else:
            return True,""


class App(tk.Tk):
    def __init__(self):
        super().__init__()
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
            self.displayLogin()
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


app = App()
app.mainloop()


