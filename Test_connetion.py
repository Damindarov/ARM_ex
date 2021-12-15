import socket
import struct
# Client
while(True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('10.100.20.22', 10000)
    # server_address = ('', 10000)
    sock.connect(server_address)
    values = (0, 0, 0, 0)
    packer = struct.Struct('f f f f')
    packed_data = packer.pack(*values)
    try:
        sock.sendall(packed_data)
        data1 = sock.recv(1024)
        print(packer.unpack(data1)
              )
    finally:
        sock.close()