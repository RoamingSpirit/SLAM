import socket

def main():
    con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    # Bind socket to local host and port
    try:
        con.bind(("", 9000))
    except socket.error as msg:
        print "Error"
        return
        
    # Start listening on socket
    con.listen(1)
    print "Wait for client.."
    
    # Connect to the client
    try:
        connection, addr = con.accept()
        print "Connected with " + addr[0] + ":" + str(addr[1])
        connection.send(chr(2))
        con.close()
    except socket.error, e:
        print "Socket closed."
	return 0

if __name__ == '__main__':
	main()

