# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# UDP multicast examples, Hugo Vincent, 2005-05-14.
import socket
import struct
from struct import *
import time
import math
import numpy as np
import csv

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
    UDP_IP = "192.169.2.1"
    UDP_PORT = 10003
    MODE = 0
    ANGLE = -700
    TORQUE = 0
    CENTER = 0
    STIFF = 0
    DUMP = 0
    POSMIN = 0
    POSMAX = 0
    Us = 0
    Val_mins = 0
    Val_maxs = 0
    enable = 0

    Us1 = 0
    Val_mins1 = 0
    Val_maxs1 = 0
    enable1 = 0

    Us_Elbow = 0
    Val_mins_ELbow = 0
    Val_maxs_ELbow = 0
    enable_Elbow = 0

    Us_Shoulder = 0
    Val_mins_Shoulder = 0
    Val_maxs_Shoulder = 0
    enable_Shoulder = 0

    skiper = 0
    time_init = time.time()

    deltaR_val = -4520
    deltaL_val = -6720
    delta_R_Shoulder_val = -1600
    while (True):
        # all this values in angels
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        frame = []
        pa = pack(
            'bbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhh',
            1, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # плечо левая
            2, MODE, int(Us), TORQUE, CENTER, STIFF, enable, int(Val_maxs), int(Val_maxs),  # кисть
            3, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # локоть
            4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(490 + 60 / 0.085), int(490 + 20 / 0.085),  # большой
            5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(2029 + 60 / 0.085), int(2029 + 70 / 0.085),  # указательный
            6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(1934 + 0 / -0.085), int(1934 + 60 / -0.085),  # средний
            7, MODE, 456, 3000, CENTER, STIFF, 0, int(3000), int(3000),
            # int((2478 + 60/0.085)),int(2478 + 10/0.085),#безымянный()
            8, MODE, ANGLE, 3000, CENTER, STIFF, 0, 3000, 3200,  # мизинец()

            1, MODE, int(Us_Shoulder), TORQUE, CENTER, STIFF, enable_Shoulder, int(Val_maxs_Shoulder),
            int(Val_mins_Shoulder),  # правая
            2, MODE, int(Us1), TORQUE, CENTER, STIFF, enable1, int(Val_maxs1), int(Val_mins1),
            3, MODE, int(Us_Elbow), TORQUE, CENTER, STIFF, enable_Elbow, int(Val_maxs_ELbow), int(Val_mins_ELbow),
            4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            7, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            8, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, 1616 + 550, 1616 + 700)
        send(pa)
        data, addr = sock.recvfrom(310)
        sock.close()

        L_ShoulderF = struct.unpack('h', data[2:4])[0] * 0.085  # incorrect?
        L_Shoulder_S = (struct.unpack('h', data[270:272])[0] - 2150) * 0.08789063  # correct
        L_ElbowR = (struct.unpack('h', data[268:270])[0] - 2088) * 0.08789063  # correct
        L_Elbow = struct.unpack('h', data[34:36])[0] * -0.02  # correct
        L_WristR = (deltaL_val - struct.unpack('h', data[18:20])[0]) * 0.085  # correct
        L_WristS = ((0 - struct.unpack('h', data[264:266])[0]) + 2630) * -0.08789063  # incorrect?
        L_WristF = ((2088 - struct.unpack('h', data[266:268])[0])) * 0.08789063
        # block for fingers
        L_Index = (-2029 + struct.unpack('h', data[66:68])[0]) * -0.085  # correct
        L_Little = (-3615 + struct.unpack('h', data[114:116])[0]) * -0.085  # correct
        L_Middle = -(1944 - struct.unpack('h', data[82:84])[0]) * 0.085  # correct
        L_Ring = -(2458 - struct.unpack('h', data[98:100])[0]) * 0.085  # correct
        L_Thumb = -(490 - struct.unpack('h', data[50:52])[0]) * 0.085

        R_ShoulderF = (-delta_R_Shoulder_val + struct.unpack('h', data[130:132])[0]) * 0.085
        R_Shoulder_S = (struct.unpack('h', data[284:286])[0] - 2150) * 0.08789063  # correct
        R_ElbowR = (struct.unpack('h', data[278:280])[0] - 2018) * 0.08789063  # correct
        R_Elbow = struct.unpack('h', data[162:164])[0] * -0.02  # correct
        R_WristR = (deltaR_val - struct.unpack('h', data[146:148])[0]) * 0.085  # correct
        R_WristS = ((0 - struct.unpack('h', data[282:284])[0]) + 2040) * 0.08789063  # incorrect?
        R_WristF = ((0 - struct.unpack('h', data[280:282])[0]) + 2160) * 0.08789063

        q1, q2, q3, q4, q5, q6, q7 = math.radians(L_ShoulderF), math.radians(L_Shoulder_S), math.radians(
            L_ElbowR), math.radians(L_Elbow), math.radians(L_WristR), math.radians(L_WristS), math.radians(L_WristF)
        q8, q9, q10, q11, q12, q13, q14 = math.radians(R_ShoulderF), math.radians(R_Shoulder_S), math.radians(R_ElbowR), \
                                          math.radians(R_Elbow), math.radians(R_WristR), math.radians(
            R_WristS), math.radians(R_WristF)
        # delta_W = (q12 - q5)
        # Kp_s = 150
        # Val_mins = -R_WristR / 0.085
        # Val_maxs = -(R_WristR / 0.085 + np.sign(delta_W) * 10)
        # if q12 > q5:
        #     Us = -Kp_s * delta_W * np.sign(delta_W)
        # else:
        #     Us = Kp_s * delta_W * np.sign(delta_W)

        # print('left ',round(q1,2), round(q2,2), round(q3,2), round(q4,2), round(q5,2), round(q6,2), round(q7,2),
        #       'righ ',round(q8,2), round(q9,2), round(q10,2), round(q11,2), round(q12,2), round(q13,2), round(q14,2))
        # print(q12)

        # q7 = q7 + 6.57
        # print(q3, q1, q4, q5, q7)
        # print('Exoskeleton_data got')
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_address = ('10.100.20.119', 10000)
        # sock.connect(server_address)
        #
        # values = (q3, q1, q4, q5, q7)
        # # values = (10, 15, 20, 25)
        # packer = struct.Struct('f f f f f')
        # packed_data = packer.pack(*values)
        # try:
        #     sock.sendall(packed_data)
        #     data = sock.recv(20)
        #     # time.sleep(0.5)
        #     print(struct.unpack("f f f f", data))
        # finally:
        #     sock.close()

        # enable = 3
        # Val_maxs = -100
        # Us = 200

        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        addr = ('192.168.10.176', 10000)
        values = (q3, q1 - 0.25, q4, q5, q7 - 0.8, q10, q8, q11, q12, q14)

        # print(round(q3,2), round(q1-0.25,2), round(q4,2), round(q5,2), round(q7-0.8,2), round(q10,2), round(q8,2), round(q11,2), round(q12,2), round(q14,2))

        packer = struct.Struct('f f f f f f f f f f')
        packed_data = packer.pack(*values)
        udp_socket.sendto(packed_data, addr)

        data1 = udp_socket.recvfrom(80)
        data_unpacked = struct.unpack("f f f f f f f f f f f f f f f f f f f f", data1[0])
        udp_socket.close()

        enable1 = 30
        Val_maxs = -6800
        Val_mins = -6800

        # #модуль на левую руку
        # if abs(round(struct.unpack('h', data[18:20])[0],2)-Val_maxs)<80:
        #     enable = 30
        # else:
        #     enable = 30
        # Us = -np.sign(round(struct.unpack('h', data[18:20])[0],2)-Val_maxs)*150

        # #модуль на правую руку
        # if abs(round(struct.unpack('h', data[146:148])[0],2) -Val_maxs1)<40:
        #     enable1 = 30
        # else:
        #     enable1 = 30
        # Us1 = -np.sign(round(struct.unpack('h', data[146:148])[0],2) -Val_maxs1)*150

        # delta_angles = round(q12,2) - round(data_unpacked[13]/0.8,2)
        # print(round(q12,2),round(data_unpacked[13]/0.8,2), round(data_unpacked[18]),delta_angles)

        # #!!!!!!!!!!!!!! #модуль на правую руку рабочий на смещение относительно угла
        # # Val_maxs1test = -(np.rad2deg(data_unpacked[13]/0.8)/0.085 - deltaR_val)
        # # Val_mins1 = -round(data_unpacked[13]/0.8,2)/0.085 + deltaR_val-1000
        # Val_maxs1 = -5000
        # Val_mins1 = -5000

        # delta_angles = struct.unpack('h', data[146:148])[0] - Val_maxs1

        # if abs(delta_angles)<40:
        #     enable1 = 30
        # else:
        #     enable1 = 36
        # Us1 = -delta_angles*0.3
        # print(round(Us1,2), round(q12,2), struct.unpack('h', data[146:148])[0], round(Val_maxs1,2),R_WristR, delta_angles)

        # #на сучай некоректности расчета
        # if struct.unpack('h', data[146:148])[0] < -7800 or struct.unpack('h', data[146:148])[0] > -3500:
        #     enable1 = 30
        # #!!!!!!!!!!!!! #модуль на правую руку рабочий на смещение относительно угла
        # # print(round(delta_angles,2), Us1, Us1_prime, Val_mins1, force_kuka1)

        # ------------------------------------------------------------------------------------------------------------------------------

        # #модуль на правую руку рабочий на смещение относительно угла
        # Val_maxs1test = -(np.rad2deg(data_unpacked[13]/0.8)/0.085 - deltaR_val)
        # # Val_mins1 = -round(data_unpacked[13]/0.8,2)/0.085 + deltaR_val-1000
        # force_kuka1 = round(data_unpacked[18])
        # delta_angles = struct.unpack('h', data[146:148])[0] - Val_maxs1
        # Val_maxs1 = Val_maxs1test
        # Val_mins1 = Val_maxs1test
        # Val_maxs1 = Val_maxs1 + np.sign(Val_maxs1)*(np.sign(force_kuka1)*50)
        # Val_mins1 = Val_mins1 + np.sign(Val_mins1)*(np.sign(force_kuka1)*50)
        # # print(round(q12,2), struct.unpack('h', data[146:148])[0], round(Val_maxs1,2),R_WristR, delta_angles, Val_maxs1test)

        # if abs(delta_angles)<40:
        #     enable1 = 30
        # else:
        #     enable1 = 30
        # Us1 = -delta_angles*0.0
        # Us1_prime = Us1
        # Us1 = Us1 - np.sign(force_kuka1)*abs(force_kuka1)*20
        # #на сучай некоректности расчета
        # if struct.unpack('h', data[146:148])[0] < -6100 or struct.unpack('h', data[146:148])[0] > -3000:
        #     enable1 = 30
        # #модуль на правую руку рабочий на смещение относительно угла
        # print(Us1, round(Val_maxs1test,2), round(struct.unpack('h', data[146:148])[0],2), Val_mins1, force_kuka1)
        # if abs(Us1) > 300:
        #     Us1 = 70
        #     enable1 = 30

        force_elbow = data_unpacked[17]
        Val_maxs_ELbow = np.rad2deg(data_unpacked[12] / 0.8 + 3.14 / 2 + 3.14 / 4) / -0.02
        Val_mins_ELbow = np.rad2deg(data_unpacked[12] / 0.8 + 3.14 / 2 + 3.14 / 4) / -0.02
        Val_maxs_ELbow = Val_maxs_ELbow + np.sign(Val_mins_ELbow) * (np.sign(force_elbow) * 50)
        Val_mins_ELbow = Val_mins_ELbow + np.sign(Val_mins_ELbow) * (np.sign(force_elbow) * 50)

        delta_angles_elbow = struct.unpack('h', data[162:164])[0] - Val_maxs_ELbow
        if data_unpacked[12] < -1.699999999999:
            delta_angles_elbow = 0
        if abs(delta_angles_elbow) < 70:
            enable_Elbow = 30
        else:
            enable_Elbow = 30
        Us_Elbow_prime = -delta_angles_elbow * 0.0
        Us_Elbow = Us_Elbow_prime - np.sign(force_elbow) * abs(force_elbow) * 10
        # print(round(R_Elbow,2), struct.unpack('h', data[162:164])[0], int(Us_Elbow), delta_angles_elbow)
        print('delta = ', int(delta_angles_elbow), 'Val_max = ', int(Val_maxs_ELbow), 'Us_Elbow = ', int(Us_Elbow),
              round(np.rad2deg(data_unpacked[12] / 0.8 + 3.14 / 2 + 3.14 / 4), 2) / -0.02,
              int(struct.unpack('h', data[162:164])[0]), data_unpacked[17])
        # на сучай некоректности расчета
        # if struct.unpack('h', data[162:164])[0] < -3500 or struct.unpack('h', data[146:148])[0] > -30:
        #     enable_Elbow = 30
        # !!!!!!!!!!!!! #модуль на правую руку рабочий на смещение относительно угла
        # print(round(delta_angles,2), Us1, Us1_prime, Val_mins1, force_kuka1)
        # print(round(R_Elbow,2), struct.unpack('h', data[162:164])[0])

        # !!!!!!!!!!!!!! #модуль на правую руку рабочий на смещение относительно угла
        # Val_maxs1test = -(np.rad2deg(data_unpacked[13]/0.8)/0.085 - deltaR_val)
        # Val_mins1 = -round(data_unpacked[13]/0.8,2)/0.085 + deltaR_val-1000

        # force_Shoulder = data_unpacked[16]
        # Val_maxs_Shoulder = (-np.rad2deg(data_unpacked[11]/0.8 -3.14/4))/0.085 + delta_R_Shoulder_val
        # Val_mins_Shoulder = (-np.rad2deg(data_unpacked[11]/0.8 -3.14/4))/0.085 + delta_R_Shoulder_val
        # Val_maxs_Shoulder = Val_maxs_Shoulder + np.sign(Val_maxs_Shoulder)*(np.sign(force_Shoulder)*30)
        # Val_mins_Shoulder = Val_mins_Shoulder + np.sign(Val_mins_Shoulder)*(np.sign(force_Shoulder)*30)

        # # Val_maxs_Shoulder = -3100
        # # Val_mins_Shoulder = -3100

        # delta_angles_Shoulder = struct.unpack('h', data[130:132])[0] - Val_maxs_Shoulder

        # if abs(delta_angles_Shoulder)<10:
        #     enable_Shoulder = 30
        # else:
        #     enable_Shoulder = 30
        # Us_Shoulder_Prime = -delta_angles_Shoulder*0.0
        # Us_Shoulder = Us_Shoulder_Prime - np.sign(force_Shoulder)*abs(force_Shoulder)*5
        # # print(round(Us_Shoulder,2), struct.unpack('h', data[146:148])[0], round(Val_maxs1,2),R_WristR, delta_angles_Shoulder)

        # #на сучай некоректности расчета
        # # if struct.unpack('h', data[130:132])[0] < -3600 or struct.unpack('h', data[130:132])[0] > -900:
        # #     enable_Shoulder = 30
        # #!!!!!!!!!!!!! #модуль на правую руку рабочий на смещение относительно угла
        # print(int(Us_Shoulder), round(R_ShoulderF,2), int(Val_mins_Shoulder), struct.unpack('h', data[130:132])[0], data_unpacked[16], -np.rad2deg(data_unpacked[11]/0.8 -3.14/4))

        # print('L_WristR=',round(L_WristR,2),'q5=',round(q5,2), 'struct=', round(struct.unpack('h', data[18:20])[0],2), 'unpack=')
        # print(data_unpacked)

        # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # addr = ('10.100.20.119', 145)
        # values = (L_Index)
        # # print(round(q5,2), round(11,2), L_Index)
        # packer = struct.Struct('f')
        # packed_data = packer.pack(values)
        # udp_socket.sendto(packed_data, addr)
        # udp_socket.close()

        # time.sleep(0.01)
        # # print('left ',q3, q1, q4, q5, q7, 'right ', q10, q8, q11, q12, q14)
        # # print('Exoskeleton_data got')
        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_address = ('10.100.20.119', 10000)
        # sock.connect(server_address)

        # values = (q3, q1, q4, q5, q7,   q10, q8, q11, q12, q14)
        # # #if skiper % 2000 == 0:

        # with open('for_speed.csv', 'a', newline='') as f:
        #     writer = csv.writer(f)
        #     row = [time.time(), q3, q1, q4, q5, q7, q10, q8, q11, q12, q14]
        #     writer.writerow(row)
        # f.close()

        # # values = (10, 15, 20, 25)
        # packer = struct.Struct('f f f f f f f f f f')
        # packed_data = packer.pack(*values)
        # try:
        #     sock.sendall(packed_data)
        #     # data = sock.recv(59)
        #     # time.sleep(0.5)
        #     # print(struct.unpack("f f f f f f f f f f f f f f f", data))
        #     # recieved_data = struct.unpack("f f f f f f f f f f f f f f f", data)
        #     # delta_W = recieved_data[13] - q5 - recieved_data[3]

        #     # Kp_s = 180
        #     # Val_mins = L_WristR / 0.085
        #     # Val_maxs = (L_WristR / 0.085 + np.sign(delta_W) * 10)
        #     # if True or (abs(recieved_data[3]*15) > 1.5):
        #     #     enable = 0
        #     # else:
        #     #     enable = 0
        #     # if q12 > q5:
        #     #     Us = -Kp_s * delta_W * np.sign(delta_W)
        #     # else:
        #     #     Us = Kp_s * delta_W * np.sign(delta_W)
        #     # print(round(recieved_data[13] - q5,2), round(delta_W,2), round(recieved_data[3],2))
        # finally:
        #     sock.close()