import sys
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QTextEdit, QVBoxLayout, QHBoxLayout, QCheckBox, QMessageBox)

class ReconatorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reconator 9000 Elite")
        self.setGeometry(100, 100, 900, 700)

        self.target_input = QLineEdit(self)
        self.target_input.setPlaceholderText("Enter domain or IP")

        self.run_button = QPushButton("Run Selected Tools")
        self.run_button.clicked.connect(self.run_tools)

        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)

        self.tools = {
            "whois": "whois {target}",
            "nmap": "nmap -A {target}",
            "dnsrecon": "dnsrecon -d {target}",
            "theHarvester": "theHarvester -d {target} -b all",
            "httpx": "httpx -silent -title -status-code -tech-detect -ip -cname -u {target}",
            "amass": "amass enum -passive -d {target}",
            "nuclei": "nuclei -u {target}",
            "waybackurls": "bash -c 'echo {target} | waybackurls'",
            "whatweb": "whatweb {target}",
            "nikto": "nikto -host {target}",
            "sqlmap": "sqlmap -u {target} --batch"
        }

        self.checkboxes = {}
        checkbox_layout = QVBoxLayout()
        for tool in self.tools:
            cb = QCheckBox(tool)
            self.checkboxes[tool] = cb
            checkbox_layout.addWidget(cb)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Target:"))
        layout.addWidget(self.target_input)
        layout.addLayout(checkbox_layout)
        layout.addWidget(self.run_button)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def run_tools(self):
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Input Error", "Please enter a valid target.")
            return

        for tool, cb in self.checkboxes.items():
            if cb.isChecked():
                cmd = self.tools[tool].format(target=target)
                self.output_text.append(f"\n[--- Running {tool} ---]\n")
                try:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                    self.output_text.append(result.stdout)
                    if result.stderr:
                        self.output_text.append(f"[stderr]\n{result.stderr}")
                except Exception as e:
                    self.output_text.append(f"Error running {tool}: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ReconatorGUI()
    gui.show()
    sys.exit(app.exec_())
