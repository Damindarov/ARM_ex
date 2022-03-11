#! /usr/bin/python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import String, Float64
import numpy as np
import socket
from struct import *
import struct
import math
import time
import sys
import binascii
import csv
def talker(q1, q2, q3, q4, q5, q6, q7, q8, q9, q10):
    pub_p = rospy.Publisher('lefttop_point', Float32MultiArray, queue_size=1)
    rospy.init_node('talker', anonymous=False)
    # rate = rospy.Rate(5)

    array = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    left_top = Float32MultiArray(data=array)
    rospy.loginfo(left_top)
    pub_p.publish(left_top)
    # rate.sleep()

desired_force = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
position_force = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def callback_force(data):
    # print(data.data[0])
    desired_force[0] = data.data[0]
    desired_force[1] = data.data[1]
    desired_force[2] = data.data[2]
    desired_force[3] = data.data[3]
    desired_force[4] = data.data[4]

def callback_positioin(data):
    # print(data.data[0])
    position_force[0] = data.data[0]
    position_force[1] = data.data[1]
    position_force[2] = data.data[2]
    position_force[3] = data.data[3]
    position_force[4] = data.data[4]
    # print(data.data[3])
    # rospy.loginfo(rospy.get_caller_id(), data.data)

filename = 'data_point.csv'
fields = ['time','q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10']
rows = []
rows_prime = [] #real value of kuka
# Press the green button in the gutter to run the script.
if __name__ == u'__main__':
    # Create a TCP/IP socket
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 10000)
    # print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock2.bind(server_address)
    # Listen for incoming connections
    sock2.listen(1)
    unpacker = struct.Struct('f f f f f f f f f f')
    rospy.init_node('talker', anonymous=False)
    time_start = time.time()
    rospy.Subscriber("/force_repiter", Float32MultiArray, callback_force)
    rospy.Subscriber("/position_repiter", Float32MultiArray, callback_positioin)
    try:
        while (time_start + 35 > time.time()):
            # print >>sys.stderr, 'waiting for a connection'
            print('waiting for a connection')
            connection, client_address = sock2.accept()

            try:
                # print >>sys.stderr, 'connection from', client_address
                # print('connection from', client_address)
                data = connection.recv(unpacker.size)

                values_force = (desired_force[0], desired_force[1], desired_force[2], desired_force[3], desired_force[4], 0, 0, 0, 0, 0, position_force[0],position_force[1],position_force[2],position_force[3],position_force[4])
                packer_force = struct.Struct('f f f f f f f f f f f f f f f')
                packed_data_force = packer_force.pack(*values_force)
                connection.sendall(packed_data_force)

                # print(struct.unpack("f f f f f f f f f f", data))
                unpacked_data = struct.unpack("f f f f f f f f f f", data)
                # print(unpacked_data[0:5], '\n', unpacked_data[5:])
                # print(data)
                # print >>sys.stderr,  unpacked_data[0]
                # rows.append([time.time(), unpacked_data[0], unpacked_data[1], unpacked_data[2], unpacked_data[3], unpacked_data[4], unpacked_data[5], unpacked_data[6], unpacked_data[7], unpacked_data[8], unpacked_data[9]])
                try:
                    talker(unpacked_data[0], unpacked_data[1], unpacked_data[2], unpacked_data[3], unpacked_data[4], unpacked_data[5], unpacked_data[6], unpacked_data[7], unpacked_data[8], unpacked_data[9])
                except rospy.ROSInterruptException:
                    pass
            finally:
                # Clean up the connection
                connection.close()
        sock2.close()
        # with open(filename + '1', 'w') as csvfile:
        #     # creating a csv writer object
        #     csvwriter = csv.writer(csvfile)
        #     # writing the fields
        #     csvwriter.writerow(fields)
        #     # writing the data rows
        #     csvwriter.writerows(rows)

    except KeyboardInterrupt:
        sock2.close()
        # with open(filename + '1', 'w') as csvfile:
        #     # creating a csv writer object
        #     csvwriter = csv.writer(csvfile)
        #     # writing the fields
        #     csvwriter.writerow(fields)
        #     # writing the data rows
        #     csvwriter.writerows(rows)
