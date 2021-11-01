"""
-----------------
GROUP CHAT CLIENT
-----------------

* Acts as the client for the group chat application.
* This is the backend implementation.

"""


import socket
#import ...
from threading import Thread

from app_gui import *


class GroupChatClient(object):
    """Acts as the client for Group Chat application.
    The port to which the client should request for connection with server, 
        should be given when the class instance is created."""

    def __init__(self, server_port):
        self.client_socket = socket.socket()
        self.server_port = server_port
        self.connected = False

        self.alert_message = ""
        self.alert_signal = AlertSignal()
        self.qt_app = QtWidgets.QApplication(sys.argv)
        self.gui_window = Ui_Window()
        #self.client_threads = {}

    def open_gui_window(self):
        """Opens the GUI window.
        Note: This function is a blocking call."""

        self.gui_window.show()
        sys.exit(self.qt_app.exec_())

    def connect(self, address, client_name):
        """Gets the IP address of the server and the client name and,
        Connects with the server,
        Creates and starts a thread to receive messages from the server.
        This is a non-blocking call.
        Returns 0 if successfull 
        Returns 1 if denied 
        Returns 2 if error"""

        try:
            self.client_socket.connect((address, self.server_port))
            permission = self.client_socket.recv(MAX_MESSAGE_LENGTH).decode()
        except:
            self.client_socket.close()
            self.client_socket = socket.socket()
            return 2

        if permission == DENY_MESSAGE:
            self.client_socket.close()
            self.client_socket = socket.socket()
            return 1

        elif permission == ACCEPT_MESSAGE:
            self.client_socket.send(client_name.encode())
            client_list_message = self.client_socket.recv(MAX_MESSAGE_LENGTH).decode()
            message_type, message_content = client_list_message.split(":")
            if message_type + ":" == CLIENT_LIST_UPDATE_MESSAGE_PREFIX:
                client_list = eval(message_content)
                self.gui_window.update_client_list(client_list)
                self.message_receive_thread = Thread(target = self.start_receiving_messages)
                self.message_receive_thread.start()
                self.connected = True
                return 0
            else:
                self.client_socket.close()
                self.client_socket = socket.socket()
                return 2

        else:
            self.client_socket.close()
            self.client_socket = socket.socket()
            return 2

    def start_receiving_messages(self):
        """Receive the messages from the server and does the needful.
        Note: This function is a blocking call."""

        while 1:
            try: message = self.client_socket.recv(MAX_MESSAGE_LENGTH).decode()
            except: message = ""
            if not(message):
                # Don't do the below todo, as even when the user closes the window, the code comes here!
                # todo: Raise an error message in the GUI window that the server had disconnected unexpectedly.
                self.disconnect()
                break
            #message_type, message_content = message.split(":")
            message_list = message.split(":")
            if len(message_list) == 2:
                message_type, message_content = message_list
            else:
                self.disconnect("Server had sent some junk message...\n\
Its advisable to close the window and reopen the application.\n\
(or just reconnect with the server)")
                break

            if message_type + ":" == CHAT_MESSAGE_PREFIX:
                self.gui_window.show_chat_message(message_content)

            elif message_type + ":" == CLIENT_LIST_UPDATE_MESSAGE_PREFIX:
                client_list = eval(message_content)
                self.gui_window.update_client_list(client_list)

            elif message_type + ":" == SHUTDOWN_MESSAGE_PREFIX:
                self.disconnect("The server had shutted down.\n\
Sorry for the inconvenience. Try chatting later!")
                break

            else:
                self.disconnect("Server had sent some junk message...\n\
Its advisable to close the window and reopen the application.\n\
(or just reconnect with the server)")
                break

    def disconnect(self, message = ""):
        """Disconnects from the server."""

        self.connected = False
        self.client_socket.close()
        self.client_socket = socket.socket()
        if message:
            self.alert_message = message
            self.alert_signal.signal.emit()
            #self.gui_window.alert(message)
        self.gui_window.toggle_gui_active_area()

    def send_chat_message(self, message):
        """Gets the given string chat message and sends it to the server."""

        if self.connected: self.client_socket.send((CHAT_MESSAGE_PREFIX + message).encode())

    def shutdown(self):
        """Shuts down the client.
        Informs the server that this client is shuted down.
        Closes the client socket.
        Terminates the message receiving thread."""

        if self.connected:
            self.client_socket.send((SHUTDOWN_MESSAGE_PREFIX + "ClientTerminated").encode())
            self.client_socket.close()
            self.message_receive_thread.join()
            # As a new socket will be reopenned in the same name, we have to close it second time.
            self.client_socket.close()


#def ...(...):


if __name__ == '__main__':
    client = GroupChatClient(SERVER_LISTENING_PORT)
    client.gui_window.set_client(lambda: client)
    client.open_gui_window()


# END
