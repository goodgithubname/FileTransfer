import os
import shutil
import socket

# Define directory paths
transfer_dir = 'transfer'
uploaded_dir = 'uploaded'

# Server address
server_address = ('localhost', 12345)

# List all files in the transfer directory
for filename in os.listdir(transfer_dir):
    filepath = os.path.join(transfer_dir, filename)
    
    # Get file size
    filesize = os.path.getsize(filepath)
    print('File size: {filesize} bytes')

    # Creating a TCP/IP socket
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    sock.connect(server_address)

    try:
        # Send file name and size
        sock.sendall(filename.encode() + b'\n' + str(filesize).encode() + b'\n')
        with open(filepath, 'rb') as f:
            # Send file content
            while True:
                data = f.read(1024)
                if not data:
                    break
                sock.sendall(data)

    finally:
        sock.close()

    shutil.move(filepath, os.path.join(uploaded_dir, filename))
