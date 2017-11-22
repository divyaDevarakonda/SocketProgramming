import sys
import socket
import select

import sctp
from   sctp import *
import threading

HOST = '127.0.0.1'
SOCKET_LIST = []
RECV_BUFFER = 4096
PORT = 9009

def chat_server():
    my_sctp_socket = sctpsocket_tcp(socket.AF_INET)
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_sctp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_sctp_socket.bind((HOST, PORT))
    my_sctp_socket.listen(10)

    # add server socket object to the list of readable connections
    SOCKET_LIST.append(my_sctp_socket)

    print "Chat server started on port " + str(PORT)

    while 1:

        # get the list sockets which are ready to be read through select
        # 4th arg, time_out  = 0 : poll and never block
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)

        for sock in ready_to_read:
            # a new connection request recieved
            if sock == my_sctp_socket:
                sockfd, addr = my_sctp_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr

                broadcast(my_sctp_socket, sockfd, "[%s:%s] entered our chatting room\n" % addr)

            # a message from a client, not a new connection
            else:
                # process data recieved from client,
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        broadcast(my_sctp_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)
                    else:
                        # remove the socket that's broken
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(my_sctp_socket, sock, "Client (%s, %s) is offline\n" % addr)

                # exception
                except:
                    broadcast(my_sctp_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    my_sctp_socket.close()

# broadcast chat messages to all connected clients
def broadcast (my_sctp_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != my_sctp_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)

if __name__ == "__main__":
    sys.exit(chat_server())
