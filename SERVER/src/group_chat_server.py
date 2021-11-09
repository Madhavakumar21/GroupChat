"""
-----------------
GROUP CHAT SERVER
-----------------

* Acts as the server for the group chat application.
* Console based module.
* Contains the class called 'GroupChatServer' which contains the methods for the required server tasks.
* Also contains a class called 'ClientInterface' to cater the 'GroupChatServer' class.

"""


import socket
#import ...
from threading import Thread

from server_config import *


class GroupChatServer(object):
    """Acts as the server for Group Chat application.
    The port in which the server should listen for clients should be given 
        when instance of the class is created."""

    def __init__(self, server_port):
        self.server_socket = socket.socket()
        self.server_port = server_port
        self.host = socket.gethostname()
        self.server_socket.bind((self.host, self.server_port))

        self.next_client_id_number = 1
        self.live_connections = []      # Will contain tuples like this: (<Client-id-no.>, <ClientInterface>)
        self.client_threads = {}

        print("\n\
------------------\n\
GROUP CHAT: SERVER\n\
------------------\n\
\n\
Server started successfully.\n\
\n\
STATE: Idle\n")

    def start_listening(self):
        """Starts listening for clients.
        Note: This function is a blocking call."""

        print("STATE: Listening...\n")
        self.server_socket.listen(MAX_CLIENTS + 1)
        while 1:
            try: client_connection, client_address = self.server_socket.accept()
            except: break

            self.configure_client(client_connection, client_address)

    def configure_client(self, client_connection, client_address):
        """Gets the client connection and client address,
        Accepts or Denies the client and if accepts,
        Configures the client."""

        print(f"\nRequest received from {client_address}")
        if len(self.live_connections) == MAX_CLIENTS:
            client_connection.send(DENY_MESSAGE.encode())
            client_connection.close()
            print(f"Request denied for {client_address} as max. no. of clients are connected\n")
        else:
            client_interface = ClientInterface(self.next_client_id_number,\
                client_connection, client_address)
            self.live_connections.append((self.next_client_id_number, client_interface))
            client_connection.send(ACCEPT_MESSAGE.encode())

            new_client_thread = Thread(target = self.start_receiving_messages)
            new_client_thread.start()
            self.client_threads[self.next_client_id_number] = new_client_thread
            self.next_client_id_number += 1

            print(f"Request accepted for {client_address}\n")

    def start_receiving_messages(self):
        """Finishes configuring the client and,
        Start waiting for messages from the client.
        Note: This function is a blocking call."""

        client_id_number, client_interface = self.live_connections[-1]
        client_name = client_interface.connection.recv(MAX_MESSAGE_LENGTH).decode()
        client_interface.set_client_name(client_name)
        client_list = self.fetch_client_list()
        client_list_update_message = CLIENT_LIST_UPDATE_MESSAGE_PREFIX + str(client_list)
        self.broadcast(client_list_update_message)

        while 1:
            try: client_message = client_interface.get_client_message_wait()
            except: client_message = ""
            if not(client_message):
                client_address = client_interface.address
                client_id_number = client_interface.id_no
                self.remove_client_entity(client_id_number)
                client_interface.close()
                # The code comes here both when the client get disconnected unexpectedly and the server shutdowns.
                #print(f"\n{client_address} got disconnected unexpectedly!\n")
                break
            #message_type, message_content = client_message.split(":")
            message_list = client_message.split(":")
            if len(message_list) == 2:
                message_type, message_content = message_list

                if message_type + ":" == CHAT_MESSAGE_PREFIX:
                    self.broadcast(message_type + ":" + client_interface.name + "> " + message_content)

                elif message_type + ":" == SHUTDOWN_MESSAGE_PREFIX:
                    client_address = client_interface.address
                    client_id_number = client_interface.id_no
                    self.remove_client_entity(client_id_number)
                    client_interface.close()

                    client_list = self.fetch_client_list()
                    client_list_update_message = CLIENT_LIST_UPDATE_MESSAGE_PREFIX + str(client_list)
                    self.broadcast(client_list_update_message)

                    print(f"\n{client_address} volunteerly got disconnected\n")
                    break

                else:
                    client_address = client_interface.address
                    print(f"\n{client_address} had sent some junk message... Ignored it\n")

            else:
                client_address = client_interface.address
                print(f"\n{client_address} had sent some junk message... Ignored it\n")

    def fetch_client_list(self):
        """Returns the list of client names"""

        client_list = []
        for client_info in self.live_connections: client_list.append(client_info[-1].name)
        return client_list

    def broadcast(self, message):
        """Broadcasts the given string message to all the clients."""

        for client_info in self.live_connections:
            client_connection = client_info[-1].connection
            client_connection.send(message.encode())

    def remove_client_entity(self, client_id_number):
        """Gets the client ID number and, 
        Removes the respective tuple from the 'live_connections' list, if exists."""

        n = 0
        for client_connection in self.live_connections:
            if client_connection[0] == client_id_number:
                self.live_connections.pop(n)
                break
            n += 1

    def shutdown(self):
        """Shuts down the server.
        Informs all the clients that the server is shuted down.
        Closes all the client connections.
        Terminates all the client threads."""

        print("\n\nShutting down...\n")
        self.broadcast(SHUTDOWN_MESSAGE_PREFIX + "ServerTerminated")
        for client_info in self.live_connections: client_info[-1].close()
        for client_thread in self.client_threads.values(): client_thread.join()
        self.server_socket.close()


class ClientInterface(object):
    """Contains all the required methods for communication with the client.
    Instance of this class must be created for each client.
    Client id number, Socket connection and client address 
        must be given at the time of instance creation."""

    def __init__(self, id_number, connection, address):
        self.id_no = id_number
        self.connection = connection
        self.address = address
        self.closed = False

    def set_client_name(self, name):
        """Creates a binding for client name"""

        self.name = name

    def get_client_message_wait(self):
        """Waits for message from the client and,
        Returns the message.
        Note: This function is a blocking call."""

        try: return self.connection.recv(MAX_MESSAGE_LENGTH).decode()
        except: return ""

    def close(self):
        """Closes the client connection."""

        if not(self.closed):
            self.connection.close()
            self.closed = True


#def ...(...):


if __name__ == '__main__':
    server = GroupChatServer(SERVER_LISTENING_PORT)
    server_main_thread = Thread(target = server.start_listening)
    server_main_thread.start()
    try:
        while 1: input("Press Ctrl-C to stop the server\n")
    except (KeyboardInterrupt, SystemExit):
        server.shutdown()
        server_main_thread.join()
        #server.shutdown()
    except:
        server.shutdown()
        server_main_thread.join()


# END
