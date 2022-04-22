from socket import *
import struct
import serial
import time

host = ''
port = 145
addr = (host, port)

udp_socket = socket(AF_INET, SOCK_DGRAM)
udp_socket.bind(addr)
activate = bytearray([0x09, 0x10, 0x03, 0xE8, 0x00, 0x03, 0x06, 0x1, 0x00, 0x00, 0x00, 0x00, 0x00, 0x72, 0xE1])
close = bytearray(
    [0x09, 0x10, 0x03, 0xE8, 0x00, 0x03, 0x06, 0x09, 0x00, 0x00, int(hex(255), 16), 0xFF, 0xFF, 0x42, 0x29])
open = bytearray(
    [0x09, 0x10, 0x03, 0xE8, 0x00, 0x03, 0x06, 0x09, 0x00, 0x00, 0x00, 0xFF, int(hex(255), 16), 0x72, 0x19])
ser = serial.Serial('/dev/ttyUSB0', 115200, stopbits=1)
ser.write(activate)
time_s = time.time()
while time_s + 20.0 > time.time():
    pass
print('Init')
station = True
ser.close()
while True:
    data = udp_socket.recvfrom(1024)
    data_angle = struct.unpack('f',data[0])
    # print(data)
    if abs(data_angle[0]) > 45 and  station:
        ser = serial.Serial('/dev/ttyUSB0', 115200, stopbits=1)
        ser.write(close)
        station = False
        print('closed')
        ser.close()
    if abs(data_angle[0]) < 45 and not station:
        ser = serial.Serial('/dev/ttyUSB0', 115200, stopbits=1)
        ser.write(open)
        station = True
        print('opened')
        ser.close()
udp_socket.close()
