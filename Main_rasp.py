#! /usr/bin/env python3
import socket
import struct
from struct import *
import time
import math
import numpy as np
import csv

from sympy import false, true
import rospy
from iiwa_msgs.msg import *
from std_msgs.msg import Float32MultiArray, Int16MultiArray
from threading import Thread

a1, a2, a3, a4 = 0.08, 0, 0.39, 0.32
force_iiwa2 = [0, 0, 0, 0, 0, 0, 0]
force_iiwa = [0, 0, 0, 0, 0, 0, 0]
pos_iiwa2 = [0, 0, 0, 0, 0, 0, 0]
pos_iiwa = [0, 0, 0, 0, 0, 0, 0]
writing = True


def callback_force_iiwa2(data):
    force_iiwa2[0] = data.torque.a1
    force_iiwa2[1] = data.torque.a2
    force_iiwa2[2] = data.torque.a3
    force_iiwa2[3] = data.torque.a4
    force_iiwa2[4] = data.torque.a5
    force_iiwa2[5] = data.torque.a6
    force_iiwa2[6] = data.torque.a7


def callback_force_iiwa(data):
    force_iiwa[0] = data.torque.a1
    force_iiwa[1] = data.torque.a2
    force_iiwa[2] = data.torque.a3
    force_iiwa[3] = data.torque.a4
    force_iiwa[4] = data.torque.a5
    force_iiwa[5] = data.torque.a6
    force_iiwa[6] = data.torque.a7


def callback_pos_iiwa2(data):
    pos_iiwa2[0] = data.position.a1
    pos_iiwa2[1] = data.position.a2
    pos_iiwa2[2] = data.position.a3
    pos_iiwa2[3] = data.position.a4
    pos_iiwa2[4] = data.position.a5
    pos_iiwa2[5] = data.position.a6
    pos_iiwa2[6] = data.position.a7


def callback_pos_iiwa(data):
    pos_iiwa[0] = data.position.a1
    pos_iiwa[1] = data.position.a2
    pos_iiwa[2] = data.position.a3
    pos_iiwa[3] = data.position.a4
    pos_iiwa[4] = data.position.a5
    pos_iiwa[5] = data.position.a6
    pos_iiwa[6] = data.position.a7


def talker(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, pub_p):
    array = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    left_top = Float32MultiArray(data=array)
    # rospy.loginfo(left_top)
    pub_p.publish(left_top)


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

    deltaR_val = -5682
    deltaL_val = -6720
    delta_R_Shoulder_val = -1650

    rospy.init_node('talker', anonymous=False)
    pub_p = rospy.Publisher('/exoskeleton_data', Float32MultiArray, queue_size=2)
    # rospy.Subscriber("/iiwa2/state/JointTorque", String, callback)
    # /iiwa2/state/JointTorque
    print('1')
    array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    left_top = Float32MultiArray(data=array)
    # rospy.loginfo(left_top)
    pub_p.publish(left_top)
    # rate = rospy.Rate(10000)
    filename = 'data_point_ROS_part.csv'
    fields = ['time', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'Us_Elbow', 'Us_Shoulder']
    rows = []

    time_start = time.time()
    time_change = time.time()
    start_angle = 0.2

    rospy.Subscriber("/iiwa2/state/ExternalJointTorque", JointTorque, callback_force_iiwa2, queue_size=1)
    rospy.Subscriber("/iiwa/state/ExternalJointTorque", JointTorque, callback_force_iiwa)
    rospy.Subscriber("/iiwa2/state/JointPosition", JointPosition, callback_pos_iiwa2, queue_size=1)
    rospy.Subscriber("/iiwa/state/JointPosition", JointPosition, callback_pos_iiwa)
    q14 = 0
    while (time_start + 225 > time.time()):
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

        R_Index = (-2692 + struct.unpack('h', data[194:196])[0]) * -0.085

        q1, q2, q3, q4, q5, q6, q7 = math.radians(L_ShoulderF), math.radians(L_Shoulder_S), math.radians(
            L_ElbowR), math.radians(L_Elbow), math.radians(L_WristR), math.radians(L_WristS), math.radians(L_WristF)
        q8, q9, q10, q11, q12, q13 = math.radians(R_ShoulderF), math.radians(R_Shoulder_S), math.radians(R_ElbowR), \
                                     math.radians(R_Elbow), math.radians(R_WristR), math.radians(
            R_WristS)
        if math.radians(R_WristF + 38) < 1 and math.radians(R_WristF + 38) > 0:
            q14 = math.radians(R_WristF + 58)
        # if time_change+5 < time.time():
        #     time_change = time.time()
        #     start_angle=start_angle*-1
        #     print(time.time())
        # q10 = start_angle

        force_elbow = force_iiwa2[3]
        Val_maxs_ELbow = np.rad2deg(pos_iiwa2[3] / 0.8 + 3.14 / 2 + 3.14 / 4) / -0.02
        Val_mins_ELbow = np.rad2deg(pos_iiwa2[3] / 0.8 + 3.14 / 2 + 3.14 / 4) / -0.02
        Val_maxs_ELbow = Val_maxs_ELbow + np.sign(Val_mins_ELbow) * (np.sign(force_elbow) * 50)
        Val_mins_ELbow = Val_mins_ELbow + np.sign(Val_mins_ELbow) * (np.sign(force_elbow) * 50)

        delta_angles_elbow = struct.unpack('h', data[162:164])[0] - Val_maxs_ELbow
        if pos_iiwa2[3] < -1.7:
            delta_angles_elbow = 0
        Us_Elbow_prime = -delta_angles_elbow * 0.0
        Us_Elbow = Us_Elbow_prime - np.sign(force_elbow) * abs(force_elbow) * 10
        # Us_Elbow = 0

        if abs(Us_Elbow) < 20:
            enable_Elbow = 30
        else:
            enable_Elbow = 30
        # print(round(R_Elbow,2), struct.unpack('h', data[162:164])[0], int(Us_Elbow), delta_angles_elbow)
        # print('delta = ', int(delta_angles_elbow), 'Val_max = ', int(Val_maxs_ELbow), 'Us_Elbow = ', int(Us_Elbow),
        #       round(np.rad2deg(pos_iiwa2[3] / 0.8 + 3.14 / 2 + 3.14 / 4), 2) / -0.02,
        #       int(struct.unpack('h', data[162:164])[0]), force_iiwa2[3])

        force_Shoulder = force_iiwa2[1]
        Val_maxs_Shoulder = (-np.rad2deg(pos_iiwa2[1] / 0.8 - 3.14 / 4)) / 0.085 + delta_R_Shoulder_val
        Val_mins_Shoulder = (-np.rad2deg(pos_iiwa2[1] / 0.8 - 3.14 / 4)) / 0.085 + delta_R_Shoulder_val
        Val_maxs_Shoulder = Val_maxs_Shoulder + np.sign(Val_maxs_Shoulder) * (np.sign(force_Shoulder) * 30)
        Val_mins_Shoulder = Val_mins_Shoulder + np.sign(Val_mins_Shoulder) * (np.sign(force_Shoulder) * 30)

        # Val_maxs_Shoulder = -3100
        # Val_mins_Shoulder = -3100

        delta_angles_Shoulder = struct.unpack('h', data[130:132])[0] - Val_maxs_Shoulder

        Us_Shoulder_Prime = -delta_angles_Shoulder * 0.0
        Us_Shoulder = Us_Shoulder_Prime - np.sign(force_Shoulder) * abs(force_Shoulder) * 20
        if abs(Us_Shoulder) < 20:
            enable_Shoulder = 30
        else:
            enable_Shoulder = 30
        # print(round(Us_Shoulder,2), struct.unpack('h', data[146:148])[0], round(Val_maxs1,2),R_WristR, delta_angles_Shoulder)
        # print(struct.unpack('h', data[146:148])[0])

        Val_maxs1test = -(np.rad2deg(pos_iiwa2[4] / 0.8) / 0.085 - deltaR_val)
        # Val_mins1 = -round(data_unpacked[13]/0.8,2)/0.085 + deltaR_val-1000
        force_kuka1 = round(force_iiwa2[4])
        delta_angles = struct.unpack('h', data[146:148])[0] - Val_maxs1
        Val_maxs1 = Val_maxs1test
        Val_mins1 = Val_maxs1test
        Val_maxs1 = Val_maxs1 + np.sign(Val_maxs1) * (np.sign(force_kuka1) * 50)
        Val_mins1 = Val_mins1 + np.sign(Val_mins1) * (np.sign(force_kuka1) * 50)
        # print(round(q12,2), struct.unpack('h', data[146:148])[0], round(Val_maxs1,2),R_WristR, delta_angles, Val_maxs1test)
        Us1 = -delta_angles * 0.0
        Us1_prime = Us1
        Us1 = Us1 - np.sign(force_kuka1) * abs(force_kuka1) * 20
        if abs(Us1) < 20:
            enable1 = 30
        else:
            enable1 = 30

        if writing:
            rows.append(
                [time.time_ns(), q3, q1 - 0.25, q4, q5, q7 - 0.8, q10, q8, q11, q12, q14, Us_Elbow, Us_Shoulder])

        talker(q3, q1 - 0.25, q4, q5, q7 - 0.8, q10, q8, q11, q12, q14, pub_p)
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.bind(('', 145))
        pa = pack('f', int(R_Index))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Make the socket multicast-aware, and set TTL.
        # print(q14)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 20)  # Change TTL (=20) to suit
        # Send the data
        s.sendto(pa, ('', 145))
        # print(R_Index)
        # # packer = struct.Struct('f f f f f f f f f f')
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)