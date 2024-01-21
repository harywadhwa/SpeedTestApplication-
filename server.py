import socket
import time
import threading
HOST = 'localhost'  # Server IP address
PORT = 1234        # Server port number
BUFFER_SIZE = 8192  # 8 KB
FORMAT = "utf-8"

def calculate_speed(start_time, end_time, data_size):
    duration = end_time - start_time
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

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((HOST,PORT))

    while True:
        print('Server listening on {}:{}'.format(HOST, PORT))
        server_socket.listen(3)
        client_socket, client_address = server_socket.accept()
        print("connected to ",client_address)
        thread = threading.Thread(target=start_server, args=(client_socket, client_address))
        thread.start()


if __name__ == '__main__':
    listen()
    


