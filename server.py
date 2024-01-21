import socket
import time
import threading
import sys

HOST = 'localhost'  # Server IP address
PORT = 1234        # Server port number
BUFFER_SIZE = 8192  # 8 KB
FORMAT = "utf-8"

def calculate_speed(start_time, end_time, data_size):
    duration = end_time - start_time
    #to avoid division by zero
    if duration == 0:
        return 0.0
    
    speed = data_size / duration  # Bytes per second
    speed = speed/125000
    return speed

def download(client_socket):
    sum = 0.0
    for i in range(0,10):
        download_speed = send_data(client_socket)
        print('Data sent successfully.')
        print('download speed is : ',download_speed,' Mbps')
        sum += download_speed

    print("average download speed is : ",sum/10)
    # client_socket.close() #closed the client connection

def send_data(client_socket):

    data = b'X' * 10 * 1024 * 1024  # 10 MB
    client_socket.sendall(data)

    download_speed = b''
    
    while True:
        chunk = client_socket.recv(BUFFER_SIZE)
        download_speed += chunk
        if b'\n' in chunk:
            break

    return float(download_speed.decode().strip())

def upload(client_socket, client_address):
    while True :
        start_time = time.time()
        data_size = 0
        expected_data_size = 10 * 1024 * 1024  # 10 MB

        while data_size < expected_data_size:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            data_size += len(data)

        end_time = time.time()

        # if data_size == 0:
        #     print("connection with ",client_address," is closed")
        #     # client_socket.close()
        #     break

        upload_speed = calculate_speed(start_time, end_time, data_size)
        upload_speed_str = str(upload_speed) + '\n'
        print('Upload speed:', upload_speed, 'Mbps')
        client_socket.send(upload_speed_str.encode(FORMAT))

def start_server(client_socket, client_address):
    try:
        download(client_socket)
        upload(client_socket, client_address)
    finally:
        client_socket.close()

    
    

def listen():

    # create a server socket
    try:
        server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except socket.error as err:
        print("socket creation failed with error %s" %(err))
        sys.exit(1)
    
    # bind the socket with server and port number
    try:
        server_socket.bind((HOST,PORT))
    except socket.error as err:
        print("socket binding failed with error %s" %(err))
        sys.exit(1)

    while True:
        print('Server listening on {}:{}'.format(HOST, PORT))

        # listen for connection
        try:
            server_socket.listen(3)
        except socket.error as err:
            print("socket listening failed with error %s" %(err))
            sys.exit(1)
        
        # accept the connection
        try:    
            client_socket, client_address = server_socket.accept()
        except socket.error as err:
            print("socket accepting failed with error %s" %(err))
            sys.exit(1)
        
        print("connected to ",client_address)
        thread = threading.Thread(target=start_server, args=(client_socket, client_address))
        thread.start()


if __name__ == '__main__':
    listen()