import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import datetime

# Tool Descriptions
tool_info = {
    "whois": "Performs a WHOIS lookup to gather domain ownership and registration info.",
    "nmap": "Performs port scanning and OS detection on the target.",
    "dnsrecon": "Performs DNS enumeration to find subdomains and records.",
    "theHarvester": "Gathers emails, subdomains, and more from public sources."
}

def run_tool(tool, target):
    if not target:
        messagebox.showwarning("Input Error", "Please enter a target domain or IP.")
        return
    try:
        command = []
        if tool == "whois":
            command = ["whois", target]
        elif tool == "nmap":
            command = ["nmap", "-A", target]
        elif tool == "dnsrecon":
            command = ["dnsrecon", "-d", target]
        elif tool == "theHarvester":
            command = ["theHarvester", "-d", target, "-b", "all"]

        result = subprocess.run(command, capture_output=True, text=True)
        output_text.insert(tk.END, f"\n[--- {tool.upper()} OUTPUT ---]\n")
        output_text.insert(tk.END, result.stdout + "\n")

        # Save to file with timestamp
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"reconator_output_{tool}_{now}.txt", "w") as f:
            f.write(result.stdout)

    except FileNotFoundError:
        output_text.insert(tk.END, f"\nError: {tool} not found on this system.\n")

def show_tool_info(tool):
    messagebox.showinfo(f"About {tool}", tool_info.get(tool, "No info available."))

def run_all():
    for tool in tool_info:
        run_tool(tool, entry.get())

def clear_output():
    output_text.delete('1.0', tk.END)

# GUI Setup
root = tk.Tk()
root.title("Reconator 9000")
root.geometry("800x600")

frame = tk.Frame(root)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter Target Domain/IP:")
label.grid(row=0, column=0, padx=5)

entry = tk.Entry(frame, width=40)
entry.grid(row=0, column=1, padx=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for i, tool in enumerate(tool_info):
    tk.Button(button_frame, text=f"Run {tool}", width=15, command=lambda t=tool: run_tool(t, entry.get())).grid(row=0, column=i)
    tk.Button(button_frame, text=f"Info {tool}", width=15, command=lambda t=tool: show_tool_info(t)).grid(row=1, column=i)

tk.Button(root, text="Run All Tools", command=run_all, bg='green', fg='white').pack(pady=5)
tk.Button(root, text="Clear Output", command=clear_output).pack(pady=5)

output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25)
output_text.pack(padx=10, pady=10)

root.mainloop()
