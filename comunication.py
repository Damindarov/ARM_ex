class comunication():
    def __init__(self):
        self.PWM = [0] * 16
        self.POS_MIN = [0] * 16
        self.POS_MAX = [0] * 16
        self.enable = [0] * 16
        self.scale = [-0.085, 0.08789063, 0.08789063, 0.02, -0.065, -0.08789063, -0.085, -0.085, 0.085, 0.085, 0.085,
                      -0.085, 0.08789063, 0.08789063, 0.02, 0.065, 0.08789063, -0.085, -0.085, 0.085, 0.085, 0.085]
        self.offset = [0, -2150, -2088, 0, 1100, 2630, -2029, -3615, -1944, -2458, -490]
        self.index = [2,270,268,34,18,264,66,114,82,98,50]
        self.val_ang = [0]*16
    # L_Shoulder = struct.unpack('h', data[2:4])[0] * -0.085  # incorrect?
    # L_Shoulder_S = (struct.unpack('h', data[270:272])[0] - 2150) * 0.08789063  # correct
    # L_ElbowR_R = (struct.unpack('h', data[268:270])[0] - 2088) * 0.08789063  # correct
    # L_Elbow = struct.unpack('h', data[34:36])[0] * 0.02  # correct
    # L_WristR = (+1100 + struct.unpack('h', data[18:20])[0]) * 0.065  # correct
    # L_WristS = ((0 + struct.unpack('h', data[264:266])[0]) + 2630) * -0.08789063  # incorrect?
    # # this block for fingers
    # L_Index = (-2029 + struct.unpack('h', data[66:68])[0]) * -0.085  # correct
    # L_Little = (-3615 + struct.unpack('h', data[114:116])[0]) * -0.085  # correct
    # L_Middle = (-1944 + struct.unpack('h', data[82:84])[0]) * 0.085  # correct
    # L_Ring = (-2458 + struct.unpack('h', data[98:100])[0]) * 0.085  # correct
    # L_Thumb = (-490 + struct.unpack('h', data[50:52])[0]) * 0.085
    def set(self, i, PWM_, P_MIN, P_MAX, enable_, debug):
        self.PWM[i] = PWM_
        self.POS_MIN[i] = P_MIN / self.scale[i] - self.offset[i]
        self.POS_MAX[i] = P_MAX / self.scale[i] - self.offset[i]
        self.enable[i] = enable_
        if debug:
            print('PWM', self.POS_MIN[i], 'POS_MIN', self.POS_MIN[i], 'POS_MAX', self.POS_MIN[i], 'enable', enable_)

    def get(self):
        pass

    def setL_Shoulder(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(0, PWM_, P_MIN, P_MAX, enable_, debug)

    def setL_Wrist(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(1, PWM_, P_MIN, P_MAX, enable_, debug)

    def setL_Elbow(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(2, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Thumb(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(3, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Index(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(4, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Middle(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(5, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Ring(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(6, PWM_, P_MIN, P_MAX, enable_, debug)

    def setLF_Little(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(7, PWM_, P_MIN, P_MAX, enable_, debug)

    def setR_Shoulder(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(8, PWM_, P_MIN, P_MAX, enable_, debug)

    def setR_Wrist(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(9, PWM_, P_MIN, P_MAX, enable_, debug)

    def setR_Elbow(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(10, PWM_, P_MIN, P_MAX, enable_, debug)

    def setRF_Thumb(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(11, PWM_, P_MIN, P_MAX, enable_, debug)

    def setRF_Index(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(12, PWM_, P_MIN, P_MAX, enable_, debug)

    def setRF_Middle(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(13, PWM_, P_MIN, P_MAX, enable_, debug)

    def setRF_Ring(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(14, PWM_, P_MIN, P_MAX, enable_, debug)

    def setRF_Little(self, PWM_=0, P_MIN=0, P_MAX=0, enable_=0, debug=False):
        self.set(15, PWM_, P_MIN, P_MAX, enable_, debug)
