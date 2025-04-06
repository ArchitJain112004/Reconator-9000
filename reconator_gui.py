#!/usr/bin/env python3
# Author: Archit
import tkinter as tk
from tkinter import messagebox
import subprocess

def run_recon():
    target = entry.get()
    if not target:
        messagebox.showwarning("Input Error", "Please enter a target domain.")
        return
    result = subprocess.run(['bash', 'reconator.sh', target], capture_output=True, text=True)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result.stdout + result.stderr)

root = tk.Tk()
root.title("Reconator GUI")

tk.Label(root, text="Target Domain:").pack()
entry = tk.Entry(root, width=40)
entry.pack()

tk.Button(root, text="Run Recon", command=run_recon).pack(pady=10)
output_text = tk.Text(root, height=25, width=100)
output_text.pack()

root.mainloop()
