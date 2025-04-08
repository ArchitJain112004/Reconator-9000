import sys
import os
import shutil
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QListWidget, QHBoxLayout,
    QMessageBox, QTextEdit, QTabWidget
)

class ReconatorGUI(QWidget):
    def _init_(self):
        super()._init_()
        self.setWindowTitle("Reconator 9000")
        self.setGeometry(100, 100, 700, 550)

        self.tabs = QTabWidget()
        self.recon_tab = QWidget()
        self.tools_info_tab = QWidget()
        self.about_tab = QWidget()

        self.tabs.addTab(self.recon_tab, "Recon")
        self.tabs.addTab(self.tools_info_tab, "Tools Info")
        self.tabs.addTab(self.about_tab, "About Us")

        self.init_recon_tab()
        self.init_tools_info_tab()
        self.init_about_tab()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.check_installed_tools()

    def init_recon_tab(self):
        layout = QVBoxLayout()

        self.domain_label = QLabel("Target Domain/IP:")
        self.domain_input = QLineEdit()

        self.outdir_label = QLabel("Output Folder:")
        self.outdir_input = QLineEdit()
        self.outdir_browse = QPushButton("Browse")
        self.outdir_browse.clicked.connect(self.browse_folder)

        outdir_layout = QHBoxLayout()
        outdir_layout.addWidget(self.outdir_input)
        outdir_layout.addWidget(self.outdir_browse)

        self.tools_label = QLabel("Select Tools:")
        self.tools_list = QListWidget()
        self.tools_list.setSelectionMode(QListWidget.MultiSelection)
        tools = ["subfinder", "nmap", "whatweb", "dirb", "traceroute", "waf", "copylog"]
        self.tools_list.addItems(tools)

        self.run_button = QPushButton("Run Selected Tools")
        self.run_button.clicked.connect(self.run_tools)

        self.status_label = QLabel("Status:")
        self.status_output = QTextEdit()
        self.status_output.setReadOnly(True)

        layout.addWidget(self.domain_label)
        layout.addWidget(self.domain_input)
        layout.addWidget(self.outdir_label)
        layout.addLayout(outdir_layout)
        layout.addWidget(self.tools_label)
        layout.addWidget(self.tools_list)
        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)
        layout.addWidget(self.status_output)

        self.recon_tab.setLayout(layout)

    def init_tools_info_tab(self):
        layout = QVBoxLayout()
        info = QTextEdit()
        info.setReadOnly(True)
        info.setText(
            """
🛠 Tool: subfinder
🔹 Desc: Subdomain discovery tool
🔗 Read More: https://github.com/projectdiscovery/subfinder

🛠 Tool: nmap
🔹 Desc: Network scanning and enumeration
🔗 Read More: https://nmap.org/book/inst-windows.html

🛠 Tool: whatweb
🔹 Desc: Identify technologies used by websites
🔗 Read More: https://github.com/urbanadventurer/WhatWeb

🛠 Tool: gobuster (dirb)
🔹 Desc: Directory brute-forcing tool
🔗 Read More: https://github.com/OJ/gobuster

🛠 Tool: traceroute
🔹 Desc: Trace route to host
🔗 Read More: https://man7.org/linux/man-pages/man8/traceroute.8.html

🛠 Tool: wafw00f
🔹 Desc: Detect web application firewalls
🔗 Read More: https://github.com/EnableSecurity/wafw00f
"""
        )
        layout.addWidget(info)
        self.tools_info_tab.setLayout(layout)

    def init_about_tab(self):
        layout = QVBoxLayout()
        about = QTextEdit()
        about.setReadOnly(True)
        about.setText(
            """
📦 Reconator 9000

Created by: Archit
Version: 1.0

Description:
Reconator is a powerful tool that streamlines web reconnaissance by allowing users to select and run popular recon tools from a single interface.

Disclaimer:
For educational and authorized security testing purposes only.
Use responsibly.

Coming Soon:
- Live result view
- Export to PDF/HTML
- Plugin support
"""
        )
        layout.addWidget(about)
        self.about_tab.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.outdir_input.setText(folder)

    def log_status(self, text):
        self.status_output.append(text)

    def check_installed_tools(self):
        tools = {
            "subfinder": "subfinder",
            "nmap": "nmap",
            "whatweb": "whatweb",
            "dirb": "gobuster",
            "traceroute": "traceroute",
            "waf": "wafw00f"
        }
        self.status_output.append("[*] Checking installed tools...\n")
        for display_name, command in tools.items():
            path = shutil.which(command)
            if path:
                self.status_output.append(f"✅ {display_name} is installed at {path}")
            else:
                self.status_output.append(f"❌ {display_name} is NOT installed")
        self.status_output.append("\n")

    def run_tools(self):
        target = self.domain_input.text()
        outdir = self.outdir_input.text()
        selected_items = self.tools_list.selectedItems()
        tools = [item.text() for item in selected_items]

        if not target or not outdir:
            QMessageBox.critical(self, "Error", "Please fill in all required fields.")
            return

        os.makedirs(outdir, exist_ok=True)

        tool_mapping = {
            "subfinder": "subfinder",
            "nmap": "nmap",
            "whatweb": "whatweb",
            "dirb": "gobuster",
            "traceroute": "traceroute",
            "waf": "wafw00f"
        }

        for tool in tools:
            if tool == "copylog":
                copied_dir = os.path.join("copied_logs")
                os.makedirs(copied_dir, exist_ok=True)
                copied = 0
                for file in os.listdir(outdir):
                    if file.endswith(".txt"):
                        src = os.path.join(outdir, file)
                        dst = os.path.join(copied_dir, file)
                        subprocess.run(["cp", src, dst])
                        copied += 1
                msg = f"[+] Copied {copied} log files to: {copied_dir}"
                self.log_status(msg)
                QMessageBox.information(self, "Copied", msg)
                continue

            tool_command = tool_mapping.get(tool, tool)
            cmd = ["bash", "reconator.sh", target, outdir, tool_command]
            try:
                self.log_status(f"[*] Running: {tool}")
                result = subprocess.run(cmd, capture_output=True, text=True)
                self.log_status(f"[+] Finished: {tool}\n{result.stdout}")
                if result.stderr:
                    self.log_status(f"[!] Error ({tool}):\n{result.stderr}")
            except Exception as e:
                self.log_status(f"[!] Failed to run {tool}: {e}")

if _name_ == "_main_":
    app = QApplication(sys.argv)
    window = ReconatorGUI()
    window.show()
    sys.exit(app.exec_())
