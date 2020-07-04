import re
import sys
import time
from datetime import datetime

import stdin_buffer_handler

import math

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from eulerscope.lines3d_demo import plot_roll, plot_pitch, plot_yaw
from eulerscope.gumball import plot_gumball_with_rpy, plot_gumball_with_rpy_with_old

#                  example: "$EULV,x,45.8750,y,-27.1250,z,-165.0000"
euler_pattern = re.compile("^\$EULV,x,([0-9.-]+),y,([0-9.-]+),z,([0-9.-]+)$")

def monitor_imu():
    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.draw()

    roll = []
    pitch = []
    yaw = []

    history = 2

    while True:
        # Throttle.
        next_iteration_earliest_allowed_start = time.time() + loop_minimum_seconds

        ### 
        ## READ FROM STDIN
        ###
        
        line = sys.stdin.readline().strip()
        if line:
            match = euler_pattern.match(line)
            if match:
                print('[{}]: {}'.format(datetime.now(), match.groups()))
                a, b, c = match.groups()
                try:
                    r, p, y = math.radians(float(a)), math.radians(float(b)), math.radians(float(c))
                except ValueError:
                    # bad parse move on
                    continue

                if len(roll) >= history:
                    while len(roll) > history:
                        roll.pop(0)
                        pitch.pop(0)
                        yaw.pop(0)

                roll.append(r)
                pitch.append(p)
                yaw.append(y)

                if len(roll) <= 1:
                    continue
                #####
                ###   UPDATE PLOT
                #####
                
                ax.clear()
                plot_gumball_with_rpy_with_old(ax, roll=roll, pitch=pitch, yaw=yaw)

                ax.set_xlim(-1, 1)
                ax.set_ylim(-1, 1)
                ax.set_zlim(-1, 1)

                #####
                ###   UPDATE PLOT
                #####
        plt.pause(0.00000000001)

def main():
    monitor_imu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
