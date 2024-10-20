from socket import *
import time, threading

def handle_connection(sock):
    sock.recv(1024)
    time.sleep(10)
    message = "HTTP/1.1 200 OK\r\n\r\n Hi there!\r\n"
    sock.send(message.encode('utf-8'))
    sock.close()

def start_server():
    print("Creating socket for server to listen on")
    main_socket = socket(AF_INET, SOCK_STREAM) # TCP socket ipv4
    
    server_port = 1234
    main_socket.bind(('',server_port))
    main_socket.listen(5)
    print(f"Server started and listening on localhost:{server_port}")
    
    i = 0
    while True:
        i= i+1
        socket_for_client, addr = main_socket.accept()
        print(i," Client address is ", addr[0],":", addr[1])
        thread = threading.Thread(target=handle_connection, args=(socket_for_client,))
        thread.start()

if __name__ == "__main__":
    start_server()        

