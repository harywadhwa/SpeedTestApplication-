import socket
import threading
import time

HOST = 'localhost'  # Server IP address
PORT = 1234          # Server port number
BUFFER_SIZE = 8192   # 8 KB
FORMAT = "utf-8"

def calculate_speed(start_time, end_time, data_size):
    duration = end_time - start_time
    speed = data_size / duration  # Bytes per second
    speed = speed / 125000  # Convert to Mbps
    return speed

def download(client_socket):
    start_time = time.time()
    data_size = 0
    expected_data_size = 10 * 1024 * 1024  # 10 MB

    simulated_data = b'0' * expected_data_size
    client_socket.sendall(simulated_data)

    end_time = time.time()

    if client_socket.fileno() == -1:
        print("Connection closed")
        return

    download_speed = calculate_speed(start_time, end_time, expected_data_size)
    download_speed_str = str(download_speed) + '\n'
    print('Download speed:', download_speed, 'Mbps')

    try:
        client_socket.send(download_speed_str.encode(FORMAT))
    except ConnectionResetError:
        print("Connection forcibly closed by the remote host")

def upload(client_socket):
    start_time = time.time()
    data_size = 0
    expected_data_size = 10 * 1024 * 1024  # 10 MB

    while data_size < expected_data_size:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        data_size += len(data)

    end_time = time.time()

    if client_socket.fileno() == -1:
        print("Connection closed")
        return

    if data_size == 0:
        print("Connection closed")
        client_socket.close()
        return

    upload_speed = calculate_speed(start_time, end_time, data_size)
    upload_speed_str = str(upload_speed) + '\n'
    print('Upload speed:', upload_speed, 'Mbps')

    try:
        client_socket.send(upload_speed_str.encode(FORMAT))
    except ConnectionResetError:
        print("Connection forcibly closed by the remote host")

def start_server(client_socket, client_address):
    for _ in range(10):
        download(client_socket)
        upload(client_socket)

def listen():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    while True:
        print('Server listening on {}:{}'.format(HOST, PORT))
        server_socket.listen(3)
        client_socket, client_address = server_socket.accept()
        print("Connected to", client_address)
        thread = threading.Thread(target=start_server, args=(client_socket, client_address))
        thread.start()

if __name__ == '__main__':
    listen()





# import socket
# import time
# import threading

# HOST = ''  # Server IP address
# PORT = 1234  # Server port number
# BUFFER_SIZE = 8192  # 8 KB
# FORMAT = "utf-8"

# def calculate_download_speed(start_time, end_time, data_size):
#     duration = end_time - start_time
#     speed = data_size / duration  # Bytes per second
#     speed = speed / 125000  # Convert to Mbps
#     return speed

# def start_server(client_socket, client_address):
#     while True:
#         start_time = time.time()
#         data_size = 0
#         expected_data_size = 10 * 1024 * 1024  # 10 MB

#         # Simulate sending data from server to client (for testing purposes)
#         simulated_data = b'0' * expected_data_size
#         client_socket.sendall(simulated_data)

#         end_time = time.time()

#         upload_speed = calculate_download_speed(start_time, end_time, expected_data_size)
#         upload_speed_str = str(upload_speed) + '\n'
#         print('Download speed:', upload_speed, 'Mbps')
#         client_socket.send(upload_speed_str.encode(FORMAT))

# def listen():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server_socket.bind((HOST, PORT))

#     while True:
#         print('Server listening on {}:{}'.format(HOST, PORT))
#         server_socket.listen(3)
#         client_socket, client_address = server_socket.accept()
#         print("Connected to ", client_address)
#         thread = threading.Thread(target=start_server, args=(client_socket, client_address))
#         thread.start()

# if __name__ == '__main__':
#     listen()



