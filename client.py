import speedtest
import socket
import time

def get_ping():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    start_time = time.time()
    client_socket.sendall('ping'.encode('utf-8'))
    client_socket.recv(1024)
    end_time = time.time()
    client_socket.close()
    ping_time = end_time - start_time
    return ping_time

def get_speed():
    st = speedtest.Speedtest()
    st.get_best_server()  # Automatically selects the best server
    download_speed = st.download() / 1_000_000  # Convert to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert to Mbps
    return download_speed, upload_speed 


def main():
    ping_time = get_ping()
    download_speed, upload_speed = get_speed()

    print(f"Ping Time: {ping_time:.2f} seconds")
    print(f"Download Speed: {download_speed:.2f} Mbps")
    print(f"Upload Speed: {upload_speed:.2f} Mbps")

if __name__ == "__main__":
    main()
