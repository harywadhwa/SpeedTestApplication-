# CLient Program to send data from server to client in order to achieve about 100Mbps speed between 2 different systems
import socket
import time

# Server configuration
HOST = 'localhost'  # Server IP address
PORT = 1234       # Server port number
BUFFER_SIZE = 8192

def send_data(client_socket):
    
    # Generate dummy data
    
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
    sum = 0.0
    for i in range(0,10):
        upload_speed = send_data(client_socket)
        print('Data sent successfully.')
        print('upload speed is : ',upload_speed,' Mbps')
        sum += upload_speed

    print("average upload speed is : ",sum/10)
