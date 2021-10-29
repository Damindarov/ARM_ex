import socket
import struct
from struct import *
import numpy as np
import sympy as sym
sym.init_printing()
import math
import csv
import plotly.io as pio
import plotly.graph_objects as go
import time
from matrix import *
a1, a2, a3, a4 = 0.08, 0, 0.39, 0.32

pi = np.pi
pi_sym = sym.pi

filename = 'point_cloud.csv'

def plot_robots(rob_cnfs, traj_x, traj_y, traj_z):

    fig = go.Figure()

    for i, q_params in enumerate(rob_cnfs):
        q1, q2, q3, q4, q5 = q_params


        T01 = np.eye(4)
        T12 = Ry(q1) @ Ty(a1)  # Joint 1 to 2
        T23 = Rx(q2) @ Tz(a2)  # Joint 2 to 3
        T34 = Rz(q3) @ Tz(a3)  # Joint 3 to 4
        T45 = Ry(q4) @ Tz(a4)  # Joint 4 to 5
        T56 = Rz(q5) @ Tz(a4)  # Joint 5 to 6

        T02 = T01 @ T12
        T03 = T01 @ T12 @ T23
        T04 = T01 @ T12 @ T23 @ T34
        T05 = T01 @ T12 @ T23 @ T34 @ T45
        T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56

        x_pos = [T01[0, -1], T02[0, -1], T03[0, -1], T04[0, -1], T05[0, -1], T06[0, -1]]
        y_pos = [T01[1, -1], T02[1, -1], T03[1, -1], T04[1, -1], T05[1, -1], T06[1, -1]]
        z_pos = [T01[2, -1], T02[2, -1], T03[2, -1], T04[2, -1], T05[2, -1], T06[2, -1]]

        # Setting opacity
        if (i != 0 and i != len(rob_cnfs) - 1):
            opc = 0.3
        else:
            opc = 1

        wd = 10  # Width

        fig.add_scatter3d(
            x=np.round(x_pos, 2),
            y=np.round(y_pos, 2),
            z=z_pos,
            line=dict(color='darkblue', width=wd),
            hoverinfo="none",  # hoverinfo="text",
            hovertext=[f"joint {idx}: {q}"
                       for idx, q in
                       enumerate(np.round(np.rad2deg([0, q1, q2, q3, q4, q5]), 0))],
            marker=dict(
                size=wd / 2,
                color=["black", "orange", "yellow", "pink", "blue", "goldenrod", "green", "red"],
            ),
            opacity=opc,
            showlegend=False,
            name=f"conf {i}"
        )

    fig.layout = dict(
        width=1000,
        height=700,
        scene=dict(
            camera=dict(eye={'x': -1.25, 'y': -1.25, 'z': 2}),
            aspectratio={'x': 1.25, 'y': 1.25, 'z': 1},
            # xaxis = dict( nticks=8, range=[np.min(traj_x)-0.5, np.max(traj_x)+0.5] ),
            # yaxis = dict( nticks=8, range=[np.min(traj_y)-0.5, np.max(traj_y)+0.5] ),
            # zaxis = dict( nticks=8, range=[-0.05, np.max(traj_z)+0.4] ),
            xaxis_title='Robot x-axis',
            yaxis_title='Robot y-axis',
            zaxis_title='Robot z-axis'),
        title=f"Robot plot in different configurations",
        colorscale=dict(diverging="thermal")
    )
    pio.show(fig)


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
    offsets_left = np.array([0, 2150, 2088, 0, 0, 2630, 2230, 2029, 3320, 1934, 2478, 0, 490])
    offsets_right = np.array([0, 2142, 2018, 0, 0, 2040, 2160, 2692, 1616, 1169, 2130, 0, 2155])
    scale_left = np.array([0.085, -0.08789063, -0.8789063, 0.02, -0.085, -0.8789063, 0.8789063, 0.085, -0.085,
                           -0.085, 0.085, 1, 0.085])
    scale_right = np.array([-0.085, -0.08789063, -0.08789063, -0.02, -0.085, -0.08789063, -0.08789063, 0.085, -0.085,
                            -0.085, 0.085, 1, -0.085])
    print(len(scale_left), len(scale_right))
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
    #     # int((2478 + 60/0.085)),int(2478 + 10/0.085),#безымянный
    #     8, MODE, ANGLE, 3000, CENTER, STIFF, 0, 3000, 3200,  # мизинец
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

    Kp = 4.8
    Ki = 0

    Kd = 5
    I = 0
    error_p = 0

    fig = go.Figure()

    fields = ['q1', 'q2', 'q3', 'q4', 'q5']
    rows = []
    print(time.time())
    start = time.time()

    while (time.time() - start < 120):
        # all this values in angels
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((UDP_IP, UDP_PORT))
        frame = []
        pa = pack(
            'bbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhhbbhhhhhhh',
            1, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, 3200, 3100,  # плечо левая
            2, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(0 / 0.087 - 2088), int(11 / 0.087 - 2088),  # кисть
            3, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # локоть
            4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(490 + 60 / 0.085), int(490 + 20 / 0.085),  # большой
            5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(2029 + 60 / 0.085), int(2029 + 70 / 0.085),  # указательный
            6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, int(1934 + 0 / -0.085), int(1934 + 60 / -0.085),  # средний
            7, MODE, 456, 3000, CENTER, STIFF, 0, int(3000), int(3000),
            # int((2478 + 60/0.085)),int(2478 + 10/0.085),#безымянный
            8, MODE, ANGLE, 3000, CENTER, STIFF, 0, 3000, 3200,  # мизинец

            1, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,  # правая
            2, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            3, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            4, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            5, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            6, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            7, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, POSMIN, POSMAX,
            8, MODE, ANGLE, TORQUE, CENTER, STIFF, 0, 1616 + 550, 1616 + 700)
        send(pa)
        data, addr = sock.recvfrom(310)

        L_Shoulder = struct.unpack('h', data[2:4])[0]*-0.085#incorrect?
        L_Shoulder_S = (struct.unpack('h', data[270:272])[0] - 2150)*0.08789063 #correct
        L_ElbowR_R = (struct.unpack('h', data[268:270])[0] - 2088)*0.08789063 #correct
        L_Elbow = struct.unpack('h', data[34:36])[0]*-0.02 #correct
        L_WristR = (0 - struct.unpack('h', data[18:20])[0])*0.085 #correct
        L_WristS = ((0 - struct.unpack('h', data[264:266])[0]) - 2630)*0.08789063 #incorrect?
        #this block for fingers
        L_Index = (-2029 + struct.unpack('h', data[66:68])[0])*-0.085 #correct
        L_Little = (-3615 + struct.unpack('h', data[114:116])[0])*-0.085 #correct
        L_Middle = -(1944 - struct.unpack('h', data[82:84])[0])*0.085 #correct
        L_Ring = -(2458 - struct.unpack('h', data[98:100])[0])*0.085 #correct
        L_Thumb = -(490 - struct.unpack('h', data[50:52])[0])*0.085

        q1, q2, q3, q4, q5 = math.radians(L_Shoulder), math.radians(L_Shoulder_S), math.radians(L_ElbowR_R),math.radians(L_Elbow), math.radians(L_WristR)

        T01 = np.eye(4)@Ry(math.pi)
        T12 = Rx(q1) @ Tx(a1)  # Joint 1 to 2
        T23 = Ry(q2) #@ Tz(a2)  # Joint 2 to 3
        T34 = Rz(q3) @ Tz(-a3)  # Joint 3 to 4
        T45 = Rx(q4) @ Tz(-a4)  # Joint 4 to 5

        T56 = Rz(q5) #@ Tz(a4)  # Joint 5 to 6

        T02 = T01 @ T12
        T03 = T01 @ T12 @ T23
        T04 = T01 @ T12 @ T23 @ T34
        T05 = T01 @ T12 @ T23 @ T34 @ T45
        T06 = T01 @ T12 @ T23 @ T34 @ T45 @ T56

        x_pos = [T01[0, -1], T02[0, -1], T03[0, -1], T04[0, -1], T05[0, -1], T06[0, -1]]
        y_pos = [T01[1, -1], T02[1, -1], T03[1, -1], T04[1, -1], T05[1, -1], T06[1, -1]]
        z_pos = [T01[2, -1], T02[2, -1], T03[2, -1], T04[2, -1], T05[2, -1], T06[2, -1]]
        print('x = ', T06[0][3] ,'y = ', T06[1][3], 'z = ', T06[2][3])
        new_row = [q1, q2, q3, q4, q5]
        rows.append(new_row)
        sock.close()
        time.sleep(0.01)
    # writing to csv file
    with open(filename+'1', 'w') as csvfile:
    # creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # writing the fields
        csvwriter.writerow(fields)
        # writing the data rows
        csvwriter.writerows(rows)
