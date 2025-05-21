import argparse
import threading
from sys import exit, argv
from time import sleep
from resource.config import Configuration as config
import walkingnao.walk as walk
import resource.qiapi as qiapi
import walkingnao.autowalk as autowalk
from naoai import naoai
from walkingnao import buttonpresses

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="IP address for the NAO robot. Cannot be a simulated robot as they are not supported")
    parser.add_argument("--port", type=int, default=9559,
                        help="NAO port (Defaults to port 9559)")

    exclude_models = parser.add_mutually_exclusive_group(required=False)
    exclude_models.add_argument("--model", help="Choose an AI model for NAO to use. If it is not set, it defaults to the last used model.")
    exclude_models.add_argument("--gemini", action="store_true", help="Sets model to Gemini. Incompatible with --model flag.")

    parser.add_argument("-s", "--system", action="store_true", help="Set the system prompt to use by the AI")
    parser.add_argument("--auto", "-a", action="store_true", help="Turns on autonomous mode (beta)")
    parser.add_argument("--cli", "-c", action="store_true", help="Use the program as a CLI instead of the GUI")
else:
    raise RuntimeError("Script must be run as main")
    exit(1)

args = parser.parse_args()

if args.cli is False:
    from PySide6 import QtWidgets

    from window import Ui_MainWindow


    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)
            self.api_key.setText(config().geminiApiKeyGUI())
            self.pushButton.clicked.connect(self.connectPushed)
            self.pushButton_2.clicked.connect(self.disconnectPushed)
        def connectPushed(self):
            self.appendLog(f"Connecting to {self.ip_address.text()}:{self.port_num.text()}")
            if self.gemini_button.isChecked() is False and self.ollama_button.isChecked() is False:
                self.appendLog("Please select a model")
                return
                
            if self.gemini_button.isChecked() is True:
                global api_key
                model = "gemini"
                api_key = self.api_key.text()
            if self.gemini_button.isChecked() is True and api_key == "":
                self.appendLog("Enter a Gemini API key to use gemini")
                return
            if self.gemini_button.isChecked() is True and api_key:
                config().geminiSaveKeyGUI(api_key)

            if self.ollama_button.isChecked() is True:           
                modelInput = self.lineEdit.text()
                model = config().modelType(modelInput)
            if self.ollama_button.isChecked() is True and model == "":
                self.appendLog("Please enter a model.")
                return

            if model == 1:
                self.appendLog("No models found, download some models or use Gemini")
                return
            elif 'available' in model:
                self.appendLog("The model was not found. Make sure it is spelled right and if you've also typed its tag.")
                self.appendLog(model)
                return

        def disconnectPushed(self):
            self.appendLog("Disconnecting...")
        def appendLog(self, text):
            self.plainTextEdit.appendPlainText(text)


    app = QtWidgets.QApplication(argv)

    window = MainWindow()
    window.show()
    app.exec()
    exit(0)






# CLI Code

if args.gemini is False:
    model = config().modelType(args.model)
    if model == 1:
        print("No models found, download some models or use Gemini")
        exit(1)
    elif 'available' in model:
        print("The model was not found. Make sure it is spelled right and if you've also typed its tag.")
        print(model)
        exit(1)
    api_key = None
elif args.gemini is True:
    model = "gemini"
    api_key = config().geminiApiKey()

sysprompt = config().systemPrompt(args.system)

# Sets started variable for the button detector
started = threading.Event()
started.clear()
qistart = threading.Event()
qistart.clear()
walkMode = threading.Event()
walkMode.set()

# Defines processes
if args.auto is False:
    buttonDetector = threading.Thread(target=buttonpresses.JoyButton().controllerButtons, args=(args.ip, args.port, model, started, qistart, walkMode, args.auto, api_key))
    naoTranscribeOff = threading.Thread(target=buttonpresses.JoyButton().onAiOff, args=(args.ip, args.port, model, started, qistart, api_key, sysprompt))
    walker = threading.Thread(target=walk.ConnectionDetails.runFromMain, args=(args.ip, args.port, qistart, walkMode))
if args.auto is True:
    autotalk = threading.Thread(target=naoai.ConnectionDetails.runFromMainStart, args=(args.ip, args.port, model, qistart, args.auto, api_key))
    walker = threading.Thread(target=autowalk.ConnectionDetails.runFromMain, args=(args.ip, args.port, qistart))

# Starts Processes
try:
    walker.start()
    if args.auto is False:
        buttonDetector.start()
        naoTranscribeOff.start()
    elif args.auto is True:
        sleep(5)
        autotalk.start()
except KeyboardInterrupt:
    if args.auto is True:
        print("Stopping sonars")
        qiapi.QiService(args.ip, args.port, qistart).stopSonar()
    exit(0)
