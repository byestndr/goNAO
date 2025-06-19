# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListView, QListWidget,
    QListWidgetItem, QMainWindow, QMenuBar, QPlainTextEdit,
    QPushButton, QRadioButton, QSizePolicy, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(921, 687)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.widget_8 = QWidget(self.centralwidget)
        self.widget_8.setObjectName(u"widget_8")
        self.verticalLayout_5 = QVBoxLayout(self.widget_8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.plainTextEdit = QPlainTextEdit(self.widget_8)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout_5.addWidget(self.plainTextEdit)

        self.clearButton = QPushButton(self.widget_8)
        self.clearButton.setObjectName(u"clearButton")

        self.verticalLayout_5.addWidget(self.clearButton)


        self.horizontalLayout_3.addWidget(self.widget_8)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.horizontalLayout_7 = QHBoxLayout(self.tab)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.widget_3 = QWidget(self.tab)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.groupBox_2 = QGroupBox(self.widget_3)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget = QWidget(self.groupBox_2)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.ip_address = QLineEdit(self.widget)
        self.ip_address.setObjectName(u"ip_address")

        self.horizontalLayout.addWidget(self.ip_address)


        self.verticalLayout_3.addWidget(self.widget)

        self.widget_2 = QWidget(self.groupBox_2)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(355, 0))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.port_num = QLineEdit(self.widget_2)
        self.port_num.setObjectName(u"port_num")

        self.horizontalLayout_2.addWidget(self.port_num)


        self.verticalLayout_3.addWidget(self.widget_2)

        self.widget_6 = QWidget(self.groupBox_2)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_10 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.checkBox = QCheckBox(self.widget_6)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_10.addWidget(self.checkBox)

        self.pushButton_2 = QPushButton(self.widget_6)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setEnabled(False)

        self.horizontalLayout_10.addWidget(self.pushButton_2)

        self.pushButton = QPushButton(self.widget_6)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_10.addWidget(self.pushButton)


        self.verticalLayout_3.addWidget(self.widget_6)


        self.verticalLayout_2.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.widget_3)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_4 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_4 = QGroupBox(self.groupBox)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout = QVBoxLayout(self.groupBox_4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gemini_button = QRadioButton(self.groupBox_4)
        self.gemini_button.setObjectName(u"gemini_button")
        self.gemini_button.setEnabled(True)

        self.verticalLayout.addWidget(self.gemini_button)

        self.ollama_button = QRadioButton(self.groupBox_4)
        self.ollama_button.setObjectName(u"ollama_button")

        self.verticalLayout.addWidget(self.ollama_button)


        self.horizontalLayout_4.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.groupBox)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget_5 = QWidget(self.groupBox_5)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.sys_prompt = QLineEdit(self.widget_5)
        self.sys_prompt.setObjectName(u"sys_prompt")

        self.horizontalLayout_6.addWidget(self.sys_prompt)


        self.verticalLayout_4.addWidget(self.widget_5)

        self.widget_4 = QWidget(self.groupBox_5)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_3 = QLabel(self.widget_4)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.api_key = QLineEdit(self.widget_4)
        self.api_key.setObjectName(u"api_key")
        self.api_key.setEchoMode(QLineEdit.EchoMode.NoEcho)

        self.horizontalLayout_5.addWidget(self.api_key)


        self.verticalLayout_4.addWidget(self.widget_4)

        self.widget_7 = QWidget(self.groupBox_5)
        self.widget_7.setObjectName(u"widget_7")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_5 = QLabel(self.widget_7)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_9.addWidget(self.label_5)

        self.lineEdit = QLineEdit(self.widget_7)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout_9.addWidget(self.lineEdit)


        self.verticalLayout_4.addWidget(self.widget_7)


        self.horizontalLayout_4.addWidget(self.groupBox_5)


        self.verticalLayout_2.addWidget(self.groupBox)


        self.horizontalLayout_7.addWidget(self.widget_3)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_6 = QVBoxLayout(self.tab_2)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.groupBox_6 = QGroupBox(self.tab_2)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.commandList = QListView(self.groupBox_6)
        self.commandList.setObjectName(u"commandList")

        self.verticalLayout_8.addWidget(self.commandList)


        self.verticalLayout_6.addWidget(self.groupBox_6)

        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.behaviorList = QListWidget(self.groupBox_3)
        self.behaviorList.setObjectName(u"behaviorList")

        self.verticalLayout_7.addWidget(self.behaviorList)

        self.behaviorRefresh = QPushButton(self.groupBox_3)
        self.behaviorRefresh.setObjectName(u"behaviorRefresh")

        self.verticalLayout_7.addWidget(self.behaviorRefresh)


        self.verticalLayout_6.addWidget(self.groupBox_3)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_3.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 921, 30))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked["bool"].connect(self.pushButton_2.setDisabled)
        self.pushButton.clicked["bool"].connect(self.pushButton.setEnabled)
        self.pushButton_2.clicked["bool"].connect(self.pushButton.setDisabled)
        self.pushButton_2.clicked["bool"].connect(self.pushButton_2.setEnabled)
        self.gemini_button.clicked["bool"].connect(self.widget_7.setDisabled)
        self.ollama_button.clicked["bool"].connect(self.widget_7.setEnabled)
        self.clearButton.clicked.connect(self.plainTextEdit.clear)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"IP address:", None))
        self.ip_address.setText("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Port:", None))
        self.port_num.setText(QCoreApplication.translate("MainWindow", u"9559", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"Auto Mode", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"Disconnect", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Connect", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"AI", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Model", None))
        self.gemini_button.setText(QCoreApplication.translate("MainWindow", u"Gemini", None))
        self.ollama_button.setText(QCoreApplication.translate("MainWindow", u"Ollama", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Settings", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"System Prompt", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Gemini API key", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Model", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Configure", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Command Remapping", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Behavior Remapping", None))
#if QT_CONFIG(tooltip)
        self.behaviorRefresh.setToolTip(QCoreApplication.translate("MainWindow", u"Pulls behaviors from your NAO robot to map buttons to", None))
#endif // QT_CONFIG(tooltip)
        self.behaviorRefresh.setText(QCoreApplication.translate("MainWindow", u"Refresh behaviors", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Controller", None))
    # retranslateUi

