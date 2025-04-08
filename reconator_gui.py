import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QLineEdit, QFileDialog, QMessageBox,
    QTabWidget, QStatusBar, QMainWindow
)
from PyQt5.QtCore import QProcess

class ReconatorMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reconator 9000 Elite 🧠")
        self.setGeometry(100, 100, 1000, 700)
        self.process = None

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout()
        central_widget.setLayout(self.layout)

        # Input layout
        self.input_layout = QHBoxLayout()
        self.label = QLabel("Target Domain/IP:")
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("example.com")
        self.input_layout.addWidget(self.label)
        self.input_layout.addWidget(self.input_field)

        # Tabs for outputs
        self.tabs = QTabWidget()
        self.full_recon_tab = QTextEdit()
        self.full_recon_tab.setReadOnly(True)
        self.tabs.addTab(self.full_recon_tab, "Full Recon")

        # Buttons layout
        self.buttons_layout = QHBoxLayout()
        self.run_button = QPushButton("\ud83d\udd25 Run Full Recon")
        self.run_button.clicked.connect(self.run_recon_script)
        self.clear_button = QPushButton("\ud83e\uddf9 Clear Output")
        self.clear_button.clicked.connect(self.clear_output)
        self.buttons_layout.addWidget(self.run_button)
        self.buttons_layout.addWidget(self.clear_button)

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # Combine layouts
        self.layout.addLayout(self.input_layout)
        self.layout.addLayout(self.buttons_layout)
        self.layout.addWidget(self.tabs)

    def run_recon_script(self):
        target = self.input_field.text().strip()
        if not target:
            QMessageBox.warning(self, "Input Error", "Please enter a target domain or IP.")
            return

        script_path = os.path.join(os.getcwd(), "reconator.sh")
        if not os.path.exists(script_path):
            QMessageBox.critical(self, "Script Missing", "The reconator.sh script was not found.")
            return

        self.full_recon_tab.clear()
        self.status_bar.showMessage(f"Running recon on: {target}...")

        self.process = QProcess(self)
        self.process.setProgram("bash")
        self.process.setArguments([script_path, target])
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        self.process.finished.connect(self.recon_finished)
        self.process.start()

    def handle_output(self):
        output = self.process.readAllStandardOutput().data().decode()
        self.full_recon_tab.append(output)

    def handle_error(self):
        error = self.process.readAllStandardError().data().decode()
        self.full_recon_tab.append(f"\n\u274c ERROR: {error}")

    def recon_finished(self):
        self.status_bar.showMessage("Recon Complete.\u2705")
        self.full_recon_tab.append("\n\u2705 Recon Complete.")

    def clear_output(self):
        self.full_recon_tab.clear()
        self.status_bar.clearMessage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReconatorMain()
    window.show()
    sys.exit(app.exec_())
