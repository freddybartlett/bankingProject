import tkinter as tk
import sqlite3
import time


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banking application")
        self.geometry("600x500")
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

        self.loginButton = tk.Button(self, text="Login", font=("Arial", 20),command=lambda: self.validateLogin(self.usernameEntry.get(),self.passwordEntry.get()))
        self.loginButton.place(x="227", y="135", height=40, width=80)

    def manageError(self, errorMessage):
        print(errorMessage)
        self.clearGUI()
        self.displayLogin()
        self.errorLabel = tk.Label(self, text=errorMessage, font=("Arial", 20), fg="red")
        self.errorLabel.place(x="0", y="200")

    def validateLogin(self, enteredUsername, enteredPassword):
        placeholderUsername = "abc"
        placeholderPassword = "123"
        if enteredUsername == "" and enteredPassword == "":
            self.manageError("Please enter a username and password")
        elif enteredUsername == "":
            self.manageError("Please enter a username")
        elif enteredPassword == "":
            self.manageError("Please enter a password")
        # will add sql logic later


app = App()
app.mainloop()


