from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTextEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QWidget, QApplication
import subprocess
import os
import sys

class ReconatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Reconator 9000")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        # Executable path
        self.exe_label = QLabel("Executable Path:")
        self.exe_input = QLineEdit()
        self.exe_browse = QPushButton("Browse")
        self.exe_browse.clicked.connect(self.browse_exe)

        exe_layout = QHBoxLayout()
        exe_layout.addWidget(self.exe_label)
        exe_layout.addWidget(self.exe_input)
        exe_layout.addWidget(self.exe_browse)
        layout.addLayout(exe_layout)

        # Input file path
        self.file_label = QLabel("Input File:")
        self.file_input = QLineEdit()
        self.file_browse = QPushButton("Browse")
        self.file_browse.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.file_browse)
        layout.addLayout(file_layout)

        # Output folder path
        self.folder_label = QLabel("Output Folder:")
        self.folder_input = QLineEdit()
        self.folder_browse = QPushButton("Browse")
        self.folder_browse.clicked.connect(self.browse_folder)

        folder_layout = QHBoxLayout()
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(self.folder_input)
        folder_layout.addWidget(self.folder_browse)
        layout.addLayout(folder_layout)

        # Run button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_executable)
        layout.addWidget(self.run_button)

        # Output log
        self.output_label = QLabel("Log Output:")
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)

        layout.addWidget(self.output_label)
        layout.addWidget(self.output_box)

        # Export button
        self.export_button = QPushButton("Export Log")
        self.export_button.clicked.connect(self.export_log)
        layout.addWidget(self.export_button)

        self.setLayout(layout)

    def browse_exe(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Executable")
        if path:
            self.exe_input.setText(path)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Input File")
        if path:
            self.file_input.setText(path)

    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self.folder_input.setText(path)

    def run_executable(self):
        exe_path = self.exe_input.text()
        file_path = self.file_input.text()
        folder_path = self.folder_input.text()

        if not os.path.isfile(exe_path):
            self.output_box.append("[Error] Executable path is invalid!")
            return

        if not os.path.isfile(file_path):
            self.output_box.append("[Error] Input file path is invalid!")
            return

        if not os.path.isdir(folder_path):
            self.output_box.append("[Error] Output folder path is invalid!")
            return

        try:
            command = [exe_path, file_path, folder_path]
            result = subprocess.run(command, capture_output=True, text=True)
            self.output_box.append(f"[Output]\n{result.stdout}")
            if result.stderr:
                self.output_box.append(f"[Error]\n{result.stderr}")
        except Exception as e:
            self.output_box.append(f"[Exception]\n{str(e)}")

    def export_log(self):
        log_content = self.output_box.toPlainText().strip()
        if not log_content:
            QMessageBox.information(self, "Export Log", "No log content to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log Output As", filter="Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(log_content)
                QMessageBox.information(self, "Export Log", f"Log saved to: {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Log", f"Error saving log: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReconatorApp()
    window.show()
    sys.exit(app.exec_())
