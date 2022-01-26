from struct import *
import socket
import struct

class comunicator():
    MODE = 0
    ANGLE = 0
    TORQUE = 0
    CENTER = 0
    STIFF = 0
    DUMP = 0
    POSMIN = 0
    POSMAX = 0
    def __new__(cls):
        print("new")
        return super(comunicator, cls).__new__(cls)
    def __init__(self):
        self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF = 0,0,0,0,0
        self.DUMP, self.POSMIN, self.POSMAX = 0,0,0
        self.PWM_L, self.PWM_R = [0] * 12,[0] * 12
        self.POS_MIN_L,self.POS_MIN_R = [0] * 12,[0] * 12
        self.POS_MAX_L,self.POS_MAX_R = [0] * 12,[0] * 12
        self.enable_L,self.enable_R  = [0] * 12,[0] * 12

        self.L_ShoulderF, self.L_ShoulderS, self.L_ElbowR, self.L_Elbow,\
        self.L_WristR, self.L_WristS, self.L_WristF, self.L_F_Index, \
        self.L_F_Little, self.L_F_Middle, self.L_F_Ring, self.L_F_Thumb, self.L_F_ThumbF = 0,1,2,3,4,5,6,7,8,9,10,11,12

        self.R_ShoulderF, self.R_ShoulderS, self.L_ElbowR, self.R_Elbow,\
        self.R_WristR, self.R_WristS, self.R_WristF, self.R_F_Index, \
        self.R_F_Little, self.R_F_Middle, self.R_F_Ring, self.R_F_Thumb, self.R_F_ThumbF = 0,1,2,3,4,5,6,7,8,9,10,11,12

        # L_ShoulderF, L_ShoulderS, L_ElbowR,L_Elbow, L_WristR, L_WristS,L.WristF, L_F_Index, L_F_Little, L_F_Middle, L_F_Ring, L_F_Thumb,
        # R_ShoulderF, R_ShoulderS, R_ElbowR,R_Elbow R_WristR, R_WristS,R.WristF, R_F_Index, R_F_Little, R_F_Middle, R_F_Ring, R_F_Thumb,
        self.scaleL = [-0.085,0.08789063,0.08789063,-0.02,0.085,0.08789063,-0.08789063,-0.085,0.085,0.085,-0.085,1,-0.085]
        self.scaleR = [0.085, 0.08789063,0.08789063, 0.02,0.085,0.08789063, 0.08789063,-0.085,0.085,0.085,-0.085,1, 0.085]
        self.offsetL = [0,-2150,-2088,0,0,-2630,-2230,-2029,-3320,-1934,-2478,0,-490]
        self.offsetR = [0,-2142,-2018,0,0,-2040,-2160,-2692,-1616,-1169, 2130,0, 2155]

    def send(self, data, port=10003, addr='192.169.2.15'):
        """send(data[, port[, addr]]) - multicasts a UDP datagram."""
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)  # Change TTL (=20) to suit
        # Send the data
        s.sendto(data, (addr, port))

    def recv(self, port=10003, addr="192.169.2.15", buf_size=310):
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

    def open_socket(self,UDP_IP, UDP_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        return sock

    def send_pack(self,sock):
        pa = pack(
            'bbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhh',
            1, MODE,0, TORQUE, CENTER, STIFF, 0, 1000,5 ,  # плечо левая
            2, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(0 / 0.087 - 2088), int(11 / 0.087 - 2088),  # кисть
            3, MODE,-100, TORQUE, CENTER, STIFF, 0, 2600, 2500,  # локоть
            4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(490 + 60 / 0.085), int(490 + 20 / 0.085),  # большой
            5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(2029 + 60 / 0.085), int(2029 + 70 / 0.085),  # указательный
            6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(1934 + 0 / -0.085), int(1934 + 60 / -0.085),  # средний
            7, MODE, 456, 3000, CENTER, STIFF, 0, int(3800), int(3900),
            # int((2478 + 60/0.085)),int(2478 + 10/0.085),#безымянный
            8, MODE, 0, 3000, CENTER, STIFF, 0, 3074, 3074,  # мизинец

            1, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # правая
            2, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            3, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            7, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            8, MODE, 0, TORQUE, CENTER, STIFF, 36, 1616 + 550, 1616 + 700)
        self.send(pa)
        data, addr = sock.recvfrom(310)
