import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.116', 10000)
sock.connect(server_address)

# print(q4)
# values = (q3, q1, q4, q5, q6)
values = (15, 15, 15, 15, 15)

packer = struct.Struct('f f f f f')
packed_data = packer.pack(*values)
# while(True):
    # try:
sock.sendall(packed_data)
        # data1 = sock.recv(1024)
        # print(packer.unpack(data1))
    # finally:
    #     sock.close()
