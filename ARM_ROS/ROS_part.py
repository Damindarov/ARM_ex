#! /usr/bin/python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import Float32MultiArray

import numpy as np
import socket
from struct import *
import struct
import math
import time
import sys
import binascii
def talker(x, y, z):
    pub_p = rospy.Publisher('lefttop_point', Float32MultiArray, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    array = [x, y, z]
    left_top = Float32MultiArray(data=array)
    rospy.loginfo(left_top)
    pub_p.publish(left_top)



# Press the green button in the gutter to run the script.
if __name__ == u'__main__':
    # Create a TCP/IP socket
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', 10000)
    print >>sys.stderr, 'starting up on %s port %s' % server_address
    sock2.bind(server_address)
    # Listen for incoming connections
    sock2.listen(1)
    unpacker = struct.Struct('f f f')
    try:
        while(True):
            print >>sys.stderr, 'waiting for a connection'
            connection, client_address = sock2.accept()
            try:
                print >>sys.stderr, 'connection from', client_address
                data = connection.recv(unpacker.size)
                unpacked_data = unpacker.unpack(data)
                print >>sys.stderr,  unpacked_data[0]
                try:
                    talker(unpacked_data[0], unpacked_data[1], unpacked_data[2])
                except rospy.ROSInterruptException:
                    pass                    
            finally:
                # Clean up the connection
                connection.close()
    except KeyboardInterrupt:
        sock2.close()

