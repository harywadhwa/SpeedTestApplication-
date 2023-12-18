import socket
import threading

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 5555))
    server_socket.listen(5)

    print("Server listening on port 5555...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    if data == 'ping':
        client_socket.sendall('pong'.encode('utf-8'))
        print("data sent to", client_socket)
    client_socket.close()

if __name__ == "__main__":
    start_server()
