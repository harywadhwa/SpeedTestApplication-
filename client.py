import socket
import time

HOST = 'localhost'  # Server IP address
PORT = 1234       # Server port number
BUFFER_SIZE = 8192

def calculate_speed(start_time, end_time, data_size):
    duration = end_time - start_time
    speed = data_size / duration  # Bytes per second
    speed = speed / 125000  # Convert to Mbps
    return speed



def download(client_socket):
    sum_speed = 0.0

    for i in range(10):
        download_speed = receive_data(client_socket)
        sum_speed += download_speed

    average_speed = sum_speed / 10
    print("Average download speed is:", average_speed, "Mbps")


def upload(client_socket):
    sum = 0.0
    for i in range(0,10):
        upload_speed = send_data(client_socket)
        print('Data sent successfully.')
        print('upload speed is : ',upload_speed,' Mbps')
        sum += upload_speed

    print("average upload speed is : ",sum/10)




def receive_data(client_socket):
    data_size = 0
    expected_data_size = 10 * 1024 * 1024  # 10 MB

    start_time = time.time()

    while data_size < expected_data_size:
        chunk = client_socket.recv(BUFFER_SIZE)
        if not chunk:
            break
        data_size += len(chunk)

    end_time = time.time()

    download_speed = calculate_speed(start_time, end_time, data_size)
    print('Data received successfully.')
    print('Download speed is:', download_speed, 'Mbps')
    return download_speed



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
    
    download(client_socket)
    upload(client_socket)

    client_socket.close()

# import socket
# import time

# HOST = 'localhost'  # Server IP address
# PORT = 1234          # Server port number
# BUFFER_SIZE = 8192

# def receive_data(client_socket):
#     data_size = 0
#     expected_data_size = 10 * 1024 * 1024  # 10 MB

#     start_time = time.time()

#     while data_size < expected_data_size:
#         chunk = client_socket.recv(BUFFER_SIZE)
#         if not chunk:
#             break
#         data_size += len(chunk)

#     end_time = time.time()

#     download_speed = calculate_download_speed(start_time, end_time, data_size)
#     print('Data received successfully.')
#     print('Download speed is:', download_speed, 'Mbps')
#     return download_speed



# if __name__ == '__main__':
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((HOST, PORT))
#     sum_speed = 0.0

#     for i in range(10):
#         download_speed = receive_data(client_socket)
#         sum_speed += download_speed

#     average_speed = sum_speed / 10
#     print("Average download speed is:", average_speed, "Mbps")

#    