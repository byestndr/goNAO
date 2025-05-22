from sys import argv
from PySide6 import QtWidgets

from ui.window import Ui_MainWindow
from resource.config import Configuration as config


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.api_key.setText(config().geminiApiKeyGUI())
        self.sys_prompt.setText(config().systemPromptGui())
        self.pushButton.clicked.connect(self.connectPushed)
        self.pushButton_2.clicked.connect(self.disconnectPushed)
    def connectPushed(self):
        self.appendLog(f"Connecting to {self.ip_address.text()}:{self.port_num.text()}")
        if self.config() == 1:
            return


    def disconnectPushed(self):
        self.appendLog("Disconnecting...")
    
    def config(self):
        if self.gemini_button.isChecked() is False and self.ollama_button.isChecked() is False:
            self.appendLog("Please select a model")
            return 1

        if self.gemini_button.isChecked() is True:
            global api_key
            model = "gemini"
            api_key = self.api_key.text()

        if self.gemini_button.isChecked() is True and api_key == "":
            self.appendLog("Enter a Gemini API key to use gemini")
            return 1

        if self.gemini_button.isChecked() is True and api_key:
            config().geminiSaveKeyGUI(api_key)
        if self.ollama_button.isChecked() is True:           
            modelInput = self.lineEdit.text()
            model = config().modelType(modelInput)
        if self.ollama_button.isChecked() is True and model == "":
            self.appendLog("Please enter a model.")
            return 1

        if model == 1:
            self.appendLog("No models found, download some models or use Gemini")
            return 1
        elif 'available' in model:
            self.appendLog("The model was not found. Make sure it is spelled right and if you've also typed its tag.")
            self.appendLog(model)
            return 1
        if self.ollama_button.isChecked() is True and model:
            config().modelSaveGUI(modelInput)
        
        if self.sys_prompt.text() == "":
            self.appendLog("Please enter a system prompt.")
            return 1
        
        sysprompt = self.sys_prompt.text()
        config().sysSaveKeyGUI(sysprompt)

    def appendLog(self, text):
        self.plainTextEdit.appendPlainText(text)

def run():
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
    exit(0)
