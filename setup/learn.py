import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

# Hardcoded member list
members = ["aleks","bill","mark","max","natan","stoo","syrena","thomas","toby"]
get = "/Users/codeclubuser/setup/learn-get.sh"
put = "/Users/codeclubuser/setup/learn-put.sh"

# GUI setup
root = tk.Tk()
root.title("Code Club Git Helper")
root.geometry("300x200")

# Member dropdown
tk.Label(root, text="Select your name:").pack(pady=5)
member_var = tk.StringVar()
member_dropdown = ttk.Combobox(root, textvariable=member_var, values=members, state="readonly")
member_dropdown.pack()

# Action buttons
def refresh_repo():
    member = member_var.get()
    if member:
        subprocess.run(["/bin/bash", f"{get}", member])
        messagebox.showinfo("Done", f"Repo refreshed for {member}")
    else:
        messagebox.showwarning("Missing", "Please select your name")

def push_changes():
    member = member_var.get()
    if member:
        subprocess.run(["/bin/bash", f"{put}", member])
        messagebox.showinfo("Done", f"Changes pushed for {member}")
    else:
        messagebox.showwarning("Missing", "Please select your name")

tk.Button(root, text="Refresh Repo", command=refresh_repo).pack(pady=10)
tk.Button(root, text="Push Changes", command=push_changes).pack()

root.mainloop()

