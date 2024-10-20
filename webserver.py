from concurrent.futures import ThreadPoolExecutor
from socket import *
import time, threading

MAX_THREADS = 2
def handle_connection(socket, addr):
    print(f"Starting to handle connection {addr[0]}:{addr[1]}")
    socket.recv(1024)
    time.sleep(10)
    message = "HTTP/1.1 200 OK\r\n\r\n Hi there!\r\n"
    socket.send(message.encode('utf-8'))
    socket.close()
    print(f"Completed handling connection {addr[0]}:{addr[1]}")

def start_server():
    print("Creating socket for server to listen on")
    main_socket = socket(AF_INET, SOCK_STREAM) # TCP socket ipv4
    
    server_port = 1234
    main_socket.bind(('',server_port))
    main_socket.listen(10)
    print(f"Server started and listening on localhost:{server_port}")
    
    i = 0
    active_threads = []
    try:
        while True:
            i= i+1
            socket_for_client, addr = main_socket.accept()
            print(i," Client address is ", addr[0],":", addr[1])
            if is_thread_available(active_threads): # Limit no of threads to MAX_THREADS
                thread = threading.Thread(target=handle_connection, args=(socket_for_client,addr))
                active_threads.append(thread)
                thread.start()

        # Same can also be accomplished through threadpoolexecutor
        # with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        #     while True:
        #         i= i+1
        #         socket_for_client, addr = main_socket.accept()
        #         print(i," Client address is ", addr[0],":", addr[1])
        #         executor.submit(handle_connection, socket_for_client, addr)
      
    finally:
        print("Server Stopped")
        main_socket.close()            


def is_thread_available(active_threads):
    while True:
        if len(active_threads)<MAX_THREADS:
            return True
        else:
            time.sleep(50/1000)
            for thread in active_threads:
                if not thread.is_alive():
                    active_threads.remove(thread)

if __name__ == "__main__":
    start_server()        

