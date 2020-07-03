import time
import serial
import io
import math
import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
from itertools import product, combinations
from numpy import sin, cos

def eulerToDegree(euler):
    return ( (euler) / (2 * pi) ) * 360

def create_serial_obj(port, baudrate):
    serial_port = serial.Serial(port=port, 
                                baudrate=baudrate, 
                                parity=serial.PARITY_NONE, 
                                bytesize=serial.EIGHTBITS, 
                                timeout=0.1, 
                                stopbits=serial.STOPBITS_ONE)
    sio = io.TextIOWrapper(io.BufferedRWPair(serial_port, serial_port))
    return(sio)

class Quat(object):
    """docstring for Quat"""
    def __init__(self, params):
        super(Quat, self).__init__()
        self.params = params
        self.w = float(params[2])
        self.x = float(params[4])
        self.y = float(params[6])
        self.z = float(params[8])
        self.yaw = math.atan2(2.0*(self.y*self.z + self.w*self.x), 
                         self.w*self.w - self.x*self.x - self.y*self.y + self.z*self.z)
        self.pitch = math.asin(-2.0*(self.x*self.z - self.w*self.y))
        self.roll = math.atan2(2.0*(self.x*self.y + self.w*self.z), 
                          self.w*self.w + self.x*self.x - self.y*self.y - self.z*self.z)
        print('ROLL:  {}'.format(self.roll))
        print('PITCH: {}'.format(self.pitch))
        print('YAW:   {}'.format(self.yaw))

def main(port):
    plt.ion()

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.scatter([0],[0],[0],color="r",s=100)

    d = [-2, 2]
    for s, e in combinations(np.array(list(product(d,d,d))), 2):
        if np.sum(np.abs(s-e)) == d[1]-d[0]:
            ax.plot3D(*zip(s,e), color="g")

    plt.draw()
    plt.pause(1)

    # sio = create_serial_obj(port=port, baudrate=9600)
    while True:
        # $EULV,x,132.6875,y,-14.3750,z,-141.6875
        # $QUAT,qw,0.3459,qx,0.8594,qy,0.3763,qz,0.0069
        line = input()
        print(line)
        # import ipdb; ipdb.set_trace()
        if ('QUAT' in line):
            line = line.split(',')
            try:
                q = Quat(line)
            except ValueError:
                print('bad string!')
                continue

            ax.clear()
            ax.scatter([0],[0],[0],color="r",s=100)
            theta = np.radians(q.yaw)
            for s, e in combinations(np.array(list(product(d,d,d))), 2):
                if np.sum(np.abs(s-e)) == d[1]-d[0]:
                    s_rotated = [s[0] * cos(theta) - s[1] * sin(theta), 
                                 s[0] * sin(theta) + s[1] * cos(theta),
                                 s[2]]
                    e_rotated = [e[0] * cos(theta) - e[1] * sin(theta), 
                                 e[0] * sin(theta) + e[1] * cos(theta),
                                 e[2]]  
                    ax.plot3D(*zip(s_rotated,e_rotated), color="g")

            plt.pause(0.1)

        elif ('EULV' in line):
            print('EULER')
            print(line)
        else:
            print('Nothing!')
            print(line)

if __name__ == '__main__':
    try:
        main(port=sys.argv[1])
    except KeyboardInterrupt:
        print_line('\n\n\tEnding...\n')