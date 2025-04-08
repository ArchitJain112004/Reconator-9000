import sys
import os
import subprocess
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QFileDialog, QMessageBox)
from PyQt5.QtGui import QFont
from datetime import datetime


class ReconatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Reconator 9000 - Elite GUI")
        self.setGeometry(100, 100, 900, 700)

        title = QLabel("Reconator 9000")
        title.setFont(QFont('Courier', 20, QFont.Bold))

        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target domain (e.g., example.com)")

        self.output_text = QTextEdit()
        self.output_text.setFont(QFont("Courier", 10))

        run_button = QPushButton("Run Reconator 9000")
        run_button.clicked.connect(self.run_reconator)

        clear_button = QPushButton("Clear Output")
        clear_button.clicked.connect(self.clear_output)

        save_button = QPushButton("Save Output")
        save_button.clicked.connect(self.save_output)

        hbox = QHBoxLayout()
        hbox.addWidget(run_button)
        hbox.addWidget(clear_button)
        hbox.addWidget(save_button)

        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(self.target_input)
        layout.addLayout(hbox)
        layout.addWidget(self.output_text)

        self.setLayout(layout)

    def run_reconator(self):
        target = self.target_input.text().strip()
        if not target:
            QMessageBox.warning(self, "Input Error", "Please enter a valid domain.")
            return

        # Save bash script if not already saved
        script_name = "reconator9000.sh"
        if not os.path.exists(script_name):
            with open(script_name, "w") as script:
                script.write(self.get_bash_script())
            os.chmod(script_name, 0o755)

        self.output_text.append(f"[+] Running Reconator on {target}...\n")
        try:
            result = subprocess.run(["bash", script_name, target], capture_output=True, text=True)
            self.output_text.append(result.stdout)
            if result.stderr:
                self.output_text.append(f"\n[!] Errors:\n{result.stderr}")
        except Exception as e:
            self.output_text.append(f"[!] Error: {str(e)}")

    def clear_output(self):
        self.output_text.clear()

    def save_output(self):
        output = self.output_text.toPlainText()
        if not output.strip():
            return
        filename, _ = QFileDialog.getSaveFileName(self, "Save Output", "reconator_output.txt")
        if filename:
            with open(filename, "w") as file:
                file.write(output)

    def get_bash_script(self):
        return """<insert full elite bash script from previous message here>"""


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReconatorApp()
    window.show()
    sys.exit(app.exec_())
