import socket
import time
HOST = 'localhost'  # Server IP address
PORT = 1234       # Server port number
BUFFER_SIZE = 8192
FORMAT = "utf-8"

def calculate_speed(start_time, end_time, data_size):
    duration = end_time - start_time
    speed = data_size / duration  # Bytes per second
    speed = speed / 125000  # Convert to Mbps
    return speed

def download(client_socket):
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

        if data_size == 0:
            # print("connection with ",client_address," is closed")
            client_socket.close()
            break

        download_speed = calculate_speed(start_time, end_time, data_size)
        download_speed_str = str(download_speed) + '\n'
        print('Download speed:', download_speed, 'Mbps')
        client_socket.send(download_speed_str.encode(FORMAT))

def upload(client_socket):
    sum = 0.0
    for i in range(0,10):
        upload_speed = send_data(client_socket)
        print('Data sent successfully.')
        print('upload speed is : ',upload_speed,' Mbps')
        sum += upload_speed

    print("average upload speed is : ",sum/10)

def send_data(client_socket):

    data = b'X' * 10 * 1024 * 1024  # 10 MB
    client_socket.sendall(data)

    upload_speed = b''
    
    while True:
        chunk = client_socket.recv(BUFFER_SIZE)
        upload_speed += chunk
        if b'\n' in chunk:
            break

    return float(upload_speed.decode().strip())

if __name__ == '__main__':
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    # upload(client_socket)
    download(client_socket)

    client_socket.close()    