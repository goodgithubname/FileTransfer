import os
import shutil
import socket
from dotenv import load_dotenv

# Define directory paths
transfer_dir = 'transfer'
uploaded_dir = 'uploaded'

# Check if directories exist, if not, create them
for directory in [transfer_dir, uploaded_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Load .env
load_dotenv()

# Server address
IP_ADDRESS = os.getenv('IP_ADDRESS')
print(IP_ADDRESS)
server_address = (IP_ADDRESS, 12345)

# List all files in the transfer directory
for filename in os.listdir(transfer_dir):
    filepath = os.path.join(transfer_dir, filename)
    
    # Get file size
    filesize = os.path.getsize(filepath)
    print('File size: ' + str(filesize) + ' bytes')

    # Creating a TCP/IP socket
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    sock.connect(server_address)

    try:
        # Send file name and size
        sock.sendall((filename + '\n').encode())
        print(f"Sending file size: {filesize}")
        sock.sendall((str(filesize) + '\n').encode())
        print(filesize)

        # Wait for ACK
        ack = sock.recv(1024)

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
