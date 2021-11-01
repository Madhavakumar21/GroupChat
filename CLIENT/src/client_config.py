"""
-------------
CLIENT CONFIG
-------------

* Contains all the default configurations and details for the Group Chat client-side application.

"""


#import ...
#from ... import ...


#class ...(...):


#def ...(...):

# Client Core Configurations
VERSION                             = "1.0.3"
MAX_MESSAGE_LENGTH                  = 1024
MAX_CHAT_CONTENT                    = 900
MAX_CLIENT_NAME_LENGTH              = 24
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
This is just the module for client configurations.\n\
Run 'group_chat_client.py' to start the client-side application.\n\
")


# END
