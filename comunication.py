from struct import *
import socket
import struct
class comunication():
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
        return super(comunication, cls).__new__(cls)
    def __init__(self):
        self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF = 0,0,0,0,0
        self.DUMP, self.POSMIN, self.POSMAX = 0,0,0
        self.PWM = [0] * 16
        self.POS_MIN = [0] * 16
        self.POS_MAX = [0] * 16
        self.enable = [0] * 16
        self.scale = [-0.085, 0.08789063, 0.08789063, 0.02, -0.065, -0.08789063,-0.08789063, -0.085, -0.085, 0.085, 0.085, 0.085,
                      -0.085, 0.08789063, 0.08789063, 0.02, -0.065, -0.08789063,-0.08789063, -0.085, -0.085, 0.085, 0.085, 0.085]
        self.offset = [0, -2150, -2088, 0, 1100, 2630, 2230,-2029, -3615, -1944, -2458, -490]
        self.index = [2,270,268,34,18,264,266,66,114,82,98,50]
        self.val_ang = [0]*16
        self.data = 0
        self.addr = 0

    def send(self,data, port=10003, addr='192.169.2.15'):
        """send(data[, port[, addr]]) - multicasts a UDP datagram."""
        # Create the socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)  # Change TTL (=20) to suit
        # Send the data
        s.sendto(data, (addr, port))

    def recv(self,port=10003, addr="192.169.2.15", buf_size=310):
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

    def set(self, i, PWM_, P_MIN, P_MAX, enable_, debug):
        self.PWM[i] = PWM_
        self.POS_MIN[i] = P_MIN / self.scale[i] - self.offset[i]
        self.POS_MAX[i] = P_MAX / self.scale[i] - self.offset[i]
        self.enable[i] = enable_
        if debug:
            print('PWM', self.PWM[i], 'POS_MIN', self.POS_MIN[i], 'POS_MAX', self.POS_MIN[i], 'enable', enable_)

    def get(self,i):
        pwm = self.PWM[i]
        p_min = self.POS_MIN[i]
        p_max = self.POS_MAX[i]
        enable = self.enable[i]
        ang = self.val_ang[i]
        return pwm,p_min,p_max,enable,ang

    def getL_Shoulder(self):
        return self.get(0)

    def getL_Shoulder_S(self):
        return self.get(1)

    def getL_ElbowR_R(self):
        return self.get(2)

    def getL_Elbow(self):
        return self.get(3)

    def getL_WristR(self):
        return self.get(4)

    def getL_WristS(self):
        return self.get(5)

    def getL_WristF(self):
        return self.get(6)

    def getL_Index(self):
        return self.get(7)

    def getL_Little(self):
        return self.get(8)

    def getL_Middle(self):
        return self.get(9)

    def getL_Ring(self):
        return self.get(10)

    def getL_Thumb(self):
        return self.get(11)

    def setL_Shoulder(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(0, PWM_, P_MIN, P_MAX, enable_, debug)

    def setL_Wrist(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(4, PWM_, P_MIN, P_MAX, enable_, debug)

    def setL_Elbow(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(3, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Thumb(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(11, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Index(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(7, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Middle(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(9, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Ring(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(10, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Little(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(8, PWM_, P_MIN, P_MAX, enable_, debug)

    def send_(self,socket):
        pa = pack(
            'bbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhh',
            1, self.MODE, self.PWM[0], self.TORQUE, self.CENTER, self.STIFF, self.enable[0], int(self.POS_MIN[0]), int(self.POS_MAX[0]),  # плечо левая
            2, self.MODE, self.PWM[3], self.TORQUE, self.CENTER, self.STIFF, self.enable[3], int(self.POS_MIN[3]), int(self.POS_MAX[3]),  # кисть
            3, self.MODE, self.PWM[4], self.TORQUE, self.CENTER, self.STIFF, self.enable[4], int(self.POS_MIN[4]), int(self.POS_MAX[4]),  # локоть
            4, self.MODE, self.PWM[7], self.TORQUE, self.CENTER, self.STIFF, self.enable[7], int(self.POS_MIN[7]), int(self.POS_MAX[7]),  # большой
            5, self.MODE, self.PWM[8], self.TORQUE, self.CENTER, self.STIFF, self.enable[8], int(self.POS_MIN[8]), int(self.POS_MAX[8]),  # указательный
            6, self.MODE, self.PWM[9], self.TORQUE, self.CENTER, self.STIFF, self.enable[9], int(self.POS_MIN[9]), int(self.POS_MAX[9]),  # средний
            7, self.MODE, self.PWM[10],self.TORQUE, self.CENTER, self.STIFF, self.enable[10],int(self.POS_MIN[10]),int(self.POS_MAX[10]), # безымянный
            8, self.MODE, 400,self.TORQUE, self.CENTER, self.STIFF, 36,int(self.POS_MIN[11]),int(self.POS_MAX[11]),  # мизинец

            1, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,  # правая
            2, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,
            3, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,
            4, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,
            5, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,
            6, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,
            7, self.MODE, self.ANGLE, self.TORQUE, self.CENTER, self.STIFF, 0, self.POSMIN, self.POSMAX,
            8, self.MODE, 0, self.TORQUE, self.CENTER, self.STIFF, 36, 1616 + 550, 1616 + 700)
        self.send(pa)
        self.data, self.addr = socket.recvfrom(310)
        self.val_ang[0] = struct.unpack('h', self.data[2:4])[0]*-0.085#incorrect?
        self.val_ang[1] = (struct.unpack('h', self.data[270:272])[0] - 2150)*0.08789063 #correct
        self.val_ang[2] = (struct.unpack('h', self.data[268:270])[0] - 2088)*0.08789063 #correct
        self.val_ang[3] = struct.unpack('h', self.data[34:36])[0]*0.02 #correct
        self.val_ang[4] = (-1100 - struct.unpack('h', self.data[18:20])[0])*0.065 #correct
        self.val_ang[5] = ((0 - struct.unpack('h', self.data[264:266])[0]) - 2630)*0.08789063 #incorrect?
        #this block for fingers
        self.val_ang[6] = (-2029 + struct.unpack('h', self.data[66:68])[0])*-0.085 #correct
        self.val_ang[7] = (-3615 + struct.unpack('h', self.data[114:116])[0])*-0.085 #correct
        self.val_ang[8] = -(1944 - struct.unpack('h', self.data[82:84])[0])*0.085 #correct
        self.val_ang[9] = -(2458 - struct.unpack('h', self.data[98:100])[0])*0.085 #correct
        self.val_ang[10] = -(490 - struct.unpack('h', self.data[50:52])[0])*0.085

        return self.data, self.addr
    #
    # def setR_Shoulder(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(8, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setR_Wrist(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(9, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setR_Elbow(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(10, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setRF_Thumb(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(11, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setRF_Index(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(12, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setRF_Middle(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(13, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setRF_Ring(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(14, PWM_, P_MIN, P_MAX, enable_, debug)
    #
    # def setRF_Little(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
    #     self.set(15, PWM_, P_MIN, P_MAX, enable_, debug)
