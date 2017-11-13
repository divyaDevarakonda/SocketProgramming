import sctp
import socket
def sctp_client ():
    print("SCTP client")
    sock = sctp.sctpsocket_tcp(socket.AF_INET)
    #sock.connect(('10.10.10.70',int(20003)))
    sock.connect(('127.0.0.1',int(8080)))
    print("Sending message")
    sock.sctp_send(msg='divya sindhuri')
    sock.shutdown(0)
    sock.close()
sctp_client()
