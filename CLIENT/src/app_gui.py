"""
-------
APP GUI
-------

* Handles GUI with PyQt5.
* GUI done for the client-side of the Group Chat application.
* The 'Ui_Window' class requires an instance of 'GroupChatClient' for doing the client operations, 
    which must be provided through the 'set_client' method.

"""


from PyQt5 import QtCore, QtWidgets, uic
import sys
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal, QObject

from client_config import *


class AlertSignal(QObject):
    """A custom signal for raising warnings and info in the GUI thread from the client core."""

    signal = pyqtSignal()


class Ui_Window(QtWidgets.QWidget):
    """This class requires an instance of 'GroupChatClient' for doing the client operations, 
    Which must be provided through the 'set_client' method."""

    def __init__(self):
        super().__init__()

        uic.loadUi("GroupChatClientWindow.ui", self)

        title = "Group Chat" + " V" + VERSION
        self.setWindowTitle(QtCore.QCoreApplication.translate("Window", title))
        self.client_list.setDisabled(True)
        #self.chat_console.setDisabled(True)
        self.chat_console.setReadOnly(True)

        self.connect_button.clicked.connect(self.connect)
        self.send_button.clicked.connect(self.send)
        self.message_entry.returnPressed.connect(self.send)
        self.chat_console.textChanged.connect(self.auto_scroll)
        #self.chat_console.verticalScrollBar().setSliderPosition(0)

    def set_client(self, get_client_function):
        """Binds the given client obtaining function as 'self.get_client_instance' and also,
        Connects the alert signal to the right slot and sets the correct active area."""

        self.get_client_instance = get_client_function
        self.get_client_instance().alert_signal.signal.connect(self.alert_from_client_core)
        self.set_gui_active_area()

    def alert_from_client_core(self):
        """Calls the alert method by giving the right message 
        Through accessing a binding in the client core"""

        self.alert(self.get_client_instance().alert_message)

    def alert(self, message):
        """Gets the given string message and shows it up in a modal 'QDialog' window.
        Note: This function is a blocking call."""

        dialog_window = QDialog()
        dialog_window.setWindowTitle("Alert")
        dialog_window.setWindowModality(QtCore.Qt.ApplicationModal)
        alert_message = QLabel("\n" + message + "\n", dialog_window)
        ok_button = QPushButton("OK", dialog_window)
        ok_button.clicked.connect(dialog_window.close)
        alert_message.setFont(QFont("Arial", 10))
        alert_layout = QVBoxLayout()
        alert_layout.addWidget(alert_message)
        alert_layout.addWidget(ok_button)
        dialog_window.setLayout(alert_layout)
        dialog_window.exec_()

    def set_gui_active_area(self):
        """Based on the connection status, it sets the active area, 
        Either of connecting area and chatting area."""

        condition = not(self.get_client_instance().connected)
        self.message_entry.setDisabled(condition)
        self.send_button.setDisabled(condition)
        self.address_entry.setDisabled(not(condition))
        self.client_name_entry.setDisabled(not(condition))
        self.connect_button.setDisabled(not(condition))
        if condition: self.client_list.clear()

    def connect(self):
        """Calls the required functions from the client-side class to connect with the server."""

        server_address = self.address_entry.text()
        client_name = self.client_name_entry.text()

        if not(server_address): self.alert("Provide the IP address of the server.")
        elif not(client_name): self.alert("Provide your name to show it in the chat.")
        elif len(client_name) > MAX_CLIENT_NAME_LENGTH:
            self.alert("Your name is too lengthy!\nProvide your nickname or something.")
        else:
            status = self.get_client_instance().connect(server_address, client_name)
            if status == 0:
                self.set_gui_active_area()
            elif status == 1:
                self.alert("Server denied your request as it is busy.\nTry again later!")
            else:
                self.alert("Something went wrong when connecting with the server.\nTry again or try later.")

    def update_client_list(self, client_list):
        """Gets the new client list and updates it in the client_list widget"""

        self.client_list.clear()
        self.client_list.addItems(client_list)

    def send(self):
        """Fetches the message from the chat entry and checks for validity.
        Sends it to the server if valid and, 
        Raises an alert if invalid."""

        message = self.message_entry.text()
        if len(message) > MAX_CHAT_CONTENT:
            self.alert("Your message is too lengthy!\n\
Break it into separate messages and then send them one by one.")
        else:
            message = message.replace(":", "{colon}")
            self.get_client_instance().send_chat_message(message)
            self.message_entry.clear()

    def show_chat_message(self, message):
        """Gets the given string chat message and appends it to the chat console."""

        self.chat_console.append('\n' + message)
        #QtCore.QCoreApplication.instance().processEvents()
        #self.chat_console.repaint()
        #QtWidgets.QApplication.processEvents()
        #self.chat_console.verticalScrollBar().setValue(self.chat_console.verticalScrollBar().maximum())

    def auto_scroll(self):
        """Scrolls the chat console to the bottom."""

        self.chat_console.verticalScrollBar().setValue(self.chat_console.verticalScrollBar().maximum())

    def closeEvent(self, event):

        self.get_client_instance().shutdown()
        event.accept()


#def ...(...):


# Handling high resolution displays
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


if __name__ == "__main__":
    print("\n\
NOT MEANT TO BE RUN\n\
\n\
This is just the module for GUI.\n\
Run 'group_chat_client.py' to start the client-side application.\n\
")


# END
