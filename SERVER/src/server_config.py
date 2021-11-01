"""
-------------
SERVER CONFIG
-------------

* Contains all the default configurations and details for the Group Chat server-side application.

"""


#import ...
#from ... import ...


#class ...(...):


#def ...(...):

# Server Core Configurations
VERSION                             = "1.0.2"
MAX_CLIENTS                         = 5
MAX_MESSAGE_LENGTH                  = 1024
SERVER_LISTENING_PORT               = 50000

# Message Format
DENY_MESSAGE                        = "RequestDenied"
ACCEPT_MESSAGE                      = "RequestAccepted"
CLIENT_LIST_UPDATE_MESSAGE_PREFIX   = "UpdateClientList:"
CHAT_MESSAGE_PREFIX                 = "Chat:"
SHUTDOWN_MESSAGE_PREFIX             = "ShutDown:"


if __name__ == '__main__':
    print("\n\
NOT MEANT TO BE RUN\n\
\n\
This is just the module for server configurations.\n\
Run 'group_chat_server.py' to start the server-side application.\n\
")


# END
