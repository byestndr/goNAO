from sys import argv
import threading
from PySide6 import QtWidgets

from ui.window import Ui_MainWindow
from resource.config import Configuration as config
import walkingnao.walk as walk
import resource.qiapi as qiapi
import walkingnao.autowalk as autowalk
from naoai import naoai
from walkingnao import buttonpresses


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = ""
        self.apikey = ""
        self.sysprompt = ""
        self.stop = threading.Event()
        self.stop.clear()
        self.api_key.setText(config().geminiApiKeyGUI())
        self.sys_prompt.setText(config().systemPromptGui())
        self.pushButton.clicked.connect(self.connectPushed)
        self.pushButton_2.clicked.connect(self.disconnectPushed)
    def connectPushed(self):
        """ 
        Connects to the robot when the connect button is pushed.
        Also runs the configure method to get and set values.
        """
        ip, port = self.ip_address.text(), self.port_num.text()
        if not ip or not port:
            self.appendLog("Enter the robot's IP address and port")
            return
        self.appendLog(f"Connecting to {self.ip_address.text()}:{self.port_num.text()}")
        if self.config() == 1:
            return

        started = threading.Event()
        started.clear()
        qistart = threading.Event()
        qistart.clear()
        walkMode = threading.Event()
        walkMode.set()
        self.stop.clear()

        if self.checkBox.isChecked() is False:
            buttonDetector = threading.Thread(
                target=buttonpresses.JoyButton().controllerButtons,
                args=(ip, port, self.model, started, qistart, walkMode, self.checkBox.isChecked(), self.apikey, self.stop))
            naoTranscribeOff = threading.Thread(
                target=buttonpresses.JoyButton().onAiOff,
                args=(ip, port, self.model, started, qistart, self.apikey, self.sysprompt, self.stop))
            walker = threading.Thread(
                target=walk.ConnectionDetails.runFromMain,
                args=(ip, port, qistart, walkMode, self.stop))
        elif self.checkBox.isChecked() is True:
            autotalk = threading.Thread(
                target=naoai.ConnectionDetails.runFromMainStart,
                args=(ip, port, self.model, qistart, self.checkBox.isChecked(), self.apikey, self.stop))
            walker = threading.Thread(
                target=autowalk.ConnectionDetails.runFromMain,
                args=(ip, port, qistart, self.stop))
        self.appendLog("Starting walker...")
        walker.start()
        if args.auto is False:
            self.appendLog("Starting button detector...")
            buttonDetector.start()
            self.appendLog("Starting AI off listener...")
            naoTranscribeOff.start()
        elif args.auto is True:
            sleep(5)
            self.appendLog("Starting autotalk...")
            autotalk.start()

    def disconnectPushed(self):
        self.appendLog("Disconnecting...")
        self.stop.set()

    def config(self):
        """ Set variable values and return one if a value is not found """
        if self.gemini_button.isChecked() is False and self.ollama_button.isChecked() is False:
            self.appendLog("Please select between Ollama or Gemini")
            return 1

        if self.gemini_button.isChecked() is True:
            self.model = "gemini"
            self.apikey = self.api_key.text()

        if self.gemini_button.isChecked() is True and self.apikey == "":
            self.appendLog("Enter a Gemini API key to use gemini")
            return 1

        if self.gemini_button.isChecked() is True and self.apikey:
            config().geminiSaveKeyGUI(self.apikey)
        if self.ollama_button.isChecked() is True:           
            modelInput = self.lineEdit.text()
            self.model = config().modelType(modelInput)
        if self.ollama_button.isChecked() is True and self.model == "":
            self.appendLog("Please enter an ollama model to use.")
            return 1

        if self.model == 1:
            self.appendLog("No models found, download some models or use Gemini")
            return 1
        elif 'available' in self.model:
            self.appendLog("The model was not found. Make sure it is spelled right and if you've also typed its tag.")
            self.appendLog(self.model)
            return 1
        if self.ollama_button.isChecked() is True and self.model:
            config().modelSaveGUI(modelInput)

        if self.sys_prompt.text() == "":
            self.appendLog("Please enter a system prompt.")
            return 1

        self.sysprompt = self.sys_prompt.text()
        config().sysSaveKeyGUI(self.sysprompt)

    def appendLog(self, text):
        """ Append the window's log with the text parameter """
        self.plainTextEdit.appendPlainText(text)

def run():
    """ Method for starting the window """
    app = QtWidgets.QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec()
    exit(0)
