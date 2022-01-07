# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# UDP multicast examples, Hugo Vincent, 2005-05-14.
import socket
import struct

a1, a2, a3, a4 = 0.08, 0, 0.39, 0.32

def send(data, port=10003, addr='192.169.2.15'):
    """send(data[, port[, addr]]) - multicasts a UDP datagram."""
    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Make the socket multicast-aware, and set TTL.
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)  # Change TTL (=20) to suit
    # Send the data
    s.sendto(data, (addr, port))


def recv(port=10003, addr="192.169.2.15", buf_size=310):
    """recv([port[, addr[,buf_size]]]) - waits for a datagram and returns the data."""

    # Create the socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set some options to make it multicast-friendly
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    except AttributeError:
        pass  # Some systems don't support SO_REUSEPORT
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)

    # Bind to the port
    s.bind(('', port))

    # Set some more multicast options
    intf = socket.gethostbyname(socket.gethostname())
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_IF, socket.inet_aton(intf))
    s.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton(intf))

    # Receive the data, then unregister multicast receive membership, then close the port
    data, sender_addr = s.recvfrom(buf_size)
    s.setsockopt(socket.SOL_IP, socket.IP_DROP_MEMBERSHIP, socket.inet_aton(addr) + socket.inet_aton('0.0.0.0'))
    s.close()
    return data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # UDP_IP = "192.169.2.1"
    # UDP_PORT = 10003
    # MODE = 0
    # ANGLE = -700
    # TORQUE = 0
    # CENTER = 0
    # STIFF = 0
    # DUMP = 0
    # POSMIN = 0
    # POSMAX = 0
    while (True):
        # # all this values in angels
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind((UDP_IP, UDP_PORT))
        # frame = []
        # pa = pack(
        #     'bbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhh',
        #     1, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, 3200, 3100,  # плечо левая
        #     2, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(0 / 0.087 - 2088), int(11 / 0.087 - 2088),  # кисть
        #     3, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # локоть
        #     4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(490 + 60 / 0.085), int(490 + 20 / 0.085),  # большой
        #     5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(2029 + 60 / 0.085), int(2029 + 70 / 0.085),  # указательный
        #     6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(1934 + 0 / -0.085), int(1934 + 60 / -0.085),  # средний
        #     7, MODE, 456, 3000, CENTER, STIFF, 0, int(3000), int(3000),
        #     # int((2478 + 60/0.085)),int(2478 + 10/0.085),#безымянный()
        #     8, MODE, ANGLE, 3000, CENTER, STIFF, 0, 3000, 3200,  # мизинец()
        #
        #     1, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # правая
        #     2, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
        #     3, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
        #     4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
        #     5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
        #     6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
        #     7, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
        #     8, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, 1616 + 550, 1616 + 700)
        # send(pa)
        # data, addr = sock.recvfrom(310)
        #
        # L_ShoulderF = struct.unpack('h', data[2:4])[0]*0.085#incorrect?
        # L_Shoulder_S = (struct.unpack('h', data[270:272])[0] - 2150)*0.08789063 #correct
        # L_ElbowR = (struct.unpack('h', data[268:270])[0] - 2088)*0.08789063 #correct
        # L_Elbow = struct.unpack('h', data[34:36])[0]*-0.02 #correct
        # L_WristR = (0 - struct.unpack('h', data[18:20])[0])*0.085 #correct
        # L_WristS = ((0 - struct.unpack('h', data[264:266])[0]) - 2630)*0.08789063 #incorrect?
        # L_WristF = ((0 - struct.unpack('h', data[264:266])[0]) - 2230)*0.08789063
        # #this block for fingers
        #
        # L_Index = (-2029 + struct.unpack('h', data[66:68])[0])*-0.085 #correct
        # L_Little = (-3615 + struct.unpack('h', data[114:116])[0])*-0.085 #correct
        # L_Middle = -(1944 - struct.unpack('h', data[82:84])[0])*0.085 #correct
        # L_Ring = -(2458 - struct.unpack('h', data[98:100])[0])*0.085 #correct
        # L_Thumb = -(490 - struct.unpack('h', data[50:52])[0])*0.085
        #
        # q1, q2, q3, q4, q5, q6, q7 = math.radians(L_ShoulderF), math.radians(L_Shoulder_S), math.radians(L_ElbowR),math.radians(L_Elbow), math.radians(L_Elbow), math.radians(L_WristR), math.radians(L_WristS), math.radians(L_WristF)
        # sock.close()
        #
        #

        print('Exoskeleton_data got')
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('192.168.0.116', 10000)
        sock.connect(server_address)

        # values = (q3, q1, q4, q5)
        values = (10, 15, 20, 25)

        packer = struct.Struct('f f f f')
        packed_data = packer.pack(*values)
        try:
            sock.sendall(packed_data)
        finally:
            sock.close()