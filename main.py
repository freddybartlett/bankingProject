import tkinter as tk
import sqlite3

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banking application")
        self.geometry("1280x720")

app = App()
app.mainloop()