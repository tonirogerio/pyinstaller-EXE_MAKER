import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, QVBoxLayout, QWidget
from PyQt6.QtCore import QProcess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.process = None

    def initUI(self):
        self.setWindowTitle("PyInstaller GUI")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Widgets
        self.labelMain = QLabel("Main Python File:")
        self.layout.addWidget(self.labelMain)

        self.lineEditMain = QLineEdit()
        self.layout.addWidget(self.lineEditMain)

        self.btnBrowseMain = QPushButton("Browse")
        self.btnBrowseMain.clicked.connect(self.select_main_file)
        self.layout.addWidget(self.btnBrowseMain)

        self.labelIcon = QLabel("Icon File (.ico):")
        self.layout.addWidget(self.labelIcon)

        self.lineEditIcon = QLineEdit()
        self.layout.addWidget(self.lineEditIcon)

        self.btnBrowseIcon = QPushButton("Browse")
        self.btnBrowseIcon.clicked.connect(self.select_icon_file)
        self.layout.addWidget(self.btnBrowseIcon)

        self.btnCreateExe = QPushButton("CREATE EXE")
        self.btnCreateExe.clicked.connect(self.create_exe)
        self.layout.addWidget(self.btnCreateExe)

        self.textEditOutput = QTextEdit()
        self.textEditOutput.setReadOnly(True)
        self.layout.addWidget(self.textEditOutput)

    def select_main_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Main Python File", "", "Python Files (*.py)")
        if filename:
            self.lineEditMain.setText(filename)

    def select_icon_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Icon File", "", "Icon Files (*.ico)")
        if filename:
            self.lineEditIcon.setText(filename)

    def create_exe(self):
        main_file = self.lineEditMain.text()
        icon_file = self.lineEditIcon.text()

        if not main_file or not icon_file:
            self.textEditOutput.append("Error: Main file and icon file must be selected.")
            return

        self.textEditOutput.append("Starting PyInstaller...")

        # Verifica se o arquivo principal .py existe
        if not os.path.isfile(main_file):
            self.textEditOutput.append(f"Error: Main file '{main_file}' not found.")
            return

        # Verifica se o arquivo de ícone .ico existe
        if not os.path.isfile(icon_file):
            self.textEditOutput.append(f"Error: Icon file '{icon_file}' not found.")
            return

        # Caminho para a pasta de saída
        output_folder = os.path.dirname(main_file)

        # Comando para PyInstaller
        command = ['pyinstaller', '--onefile', '--windowed', f'--icon={icon_file}', main_file]

        # Inicia o processo PyInstaller
        self.process = QProcess(self)
        self.process.setWorkingDirectory(output_folder)
        self.process.start('pyinstaller', command[1:])

        # Conecta sinais de saída
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        output = data.data().decode()
        self.textEditOutput.append(output)
        self.textEditOutput.ensureCursorVisible()

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        output = data.data().decode()
        self.textEditOutput.append(output)
        self.textEditOutput.ensureCursorVisible()

    def process_finished(self):
        self.textEditOutput.append("PyInstaller process finished.")
        self.process = None

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
