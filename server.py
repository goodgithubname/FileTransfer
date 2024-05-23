import os
import socket
import time

# Define directory paths
uploaded_dir = 'uploaded'

if not os.path.exists(uploaded_dir):
    os.makedirs(uploaded_dir)

#  Create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# function to get outbound ip
def get_outbound_ip():
    # Connect to a remote server on port 80 (http)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't matter if this address is reachable
        sock.connect(('10.255.255.255', 1))
        ip = sock.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        sock.close()
    return ip

# Bind the socket to the address and port
server_address = (get_outbound_ip(), 12345)
print('Starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
print('Waiting for a connection')
sock.listen(1)

while True:
    # wait for connection
    connection, client_address = sock.accept()

    # Check if directory exists, if not, create it
    if not os.path.exists(uploaded_dir):
        os.makedirs(uploaded_dir)

    try:
        # Receive the file name and size
        filename = connection.recv(65536).decode().strip()
        received_filesize = connection.recv(65536).decode().strip()
        print(f"Received filename: {filename}")
        print(f"Received filesize: {received_filesize}")
        filesize = int(received_filesize)
        print(f"Sending file size: {filesize}")

        print('request for {}, {}'.format(filename, filesize))
        
        # Send ACK to client
        connection.sendall(b'ACK')

        data = b''
        print('0/{}'.format(filesize))
        start_time = time.time()
        while len(data) < filesize:
            chunk = connection.recv(65536)
            if not chunk:
                break
            data += chunk
            elapsed_time = time.time() - start_time
            transfer_rate = len(data) / elapsed_time
            remaining_data = filesize - len(data)
            estimated_time = remaining_data / transfer_rate
            print('\r{}/{} bytes received, estimated time remaining: {:.2f} seconds'.format(len(data), filesize, estimated_time), end='')

        # Write the file data to a file
        with open(os.path.join(uploaded_dir, filename), 'wb') as f:
            f.write(data)
        
    finally:
        connection.close()
