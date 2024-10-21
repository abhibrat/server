from concurrent.futures import ThreadPoolExecutor
from socket import *
import time, threading

MAX_THREADS = 2

def handle_connection(socket, addr):
    print(f"Starting to handle connection {addr[0]}:{addr[1]}")
    data = socket.recv(1024)
    data = data.decode()
    data = data.splitlines()
    remote_url = data[0].split(" ")[1]
    
    if remote_url[0] !='/':
        raise Exception("Bad Request: Remote Url couldn't be parsed")
    
    remote_url = remote_url[1:]
    
    try: 
        if remote_url:
            print("Remote Url: ",remote_url)
            data = connect(remote_url)
            message = "HTTP/1.1 200 OK\r\n\r\n" + data + "\r\n"
            socket.send(message.encode())
    except Exception as e:
        print("Error occured while sending response to client")
        print(f"Error: {e}")

    # time.sleep(5)
    # message = "HTTP/1.1 200 OK\r\n\r\n Hi there!\r\n"
    # socket.send(message.encode('utf-8'))
    finally:
        socket.close()
    
    print(f"Completed handling connection {addr[0]}:{addr[1]}")

def connect(url):
    url_parts =  url.split('/',1)
    host = url.split('/',1)[0]
    path=""
    if len(url_parts)>1:
        path = url.split('/',1)[1]
    try:
        proxy_socket = socket(AF_INET, SOCK_STREAM)
        proxy_socket.connect((host,80))
    except Exception as e:
        print("Error occured while connecting to remote server")
        print(f"Error: {e}")
        proxy_socket.close()
        
    try:
        # request = "GET /{path} HTTP/1.0\r\nHost: {host}\r\nConnection: close\r\n\r\n".format(host=host, path=path)    
        request = "GET / HTTP/1.0\r\nHost: {}\r\nConnection: close\r\n\r\n".format(host)    

        print(request)
        proxy_socket.send(request.encode())
        response = proxy_socket.recv(4096)

        while True:
            data = proxy_socket.recv(4096)
            if not data:
                proxy_socket.close()
                break
            response+=data
    except Exception as e:
        print("Error occured while receiving data from remote server")
        print(f"Error {e}")        
    finally:
        proxy_socket.close()
    response = response.decode()       
    headers, body = response.split("\r\n\r\n", 1)    
    print(body[0:100])
    return body          

def start_server():
    print("Creating socket for server to listen on")
    main_socket = socket(AF_INET, SOCK_STREAM) # TCP socket ipv4
    main_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
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

