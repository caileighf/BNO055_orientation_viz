import re
import sys
import time

import math

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

from eulerscope.lines3d_demo import plot_roll, plot_pitch, plot_yaw
from eulerscope.gumball import plot_gumball_with_rpy

import stdin_buffer_handler

#                  example: "$EULV,x_yaw,0.0000,y_pitch,-25.3750,z_roll,-30.8750"
euler_pattern = re.compile("^\$EULV,x_yaw,([0-9.-]+),y_pitch,([0-9.-]+),z_roll,([0-9.-]+)$")


def monitor_imu():
    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.draw()

    while True:
        ### 
        ## READ FROM STDIN
        ###
        
        line = sys.stdin.readline().strip()
        if line:
            match = euler_pattern.match(line)
            if match:
                print(match.groups())
                a, b, c = match.groups()
                try:
                    roll, pitch, yaw = math.radians(float(a)), math.radians(float(b)), math.radians(float(c))
                except ValueError:
                    # bad parse move on
                    continue

                #####
                ###   UPDATE PLOT
                #####

                ax.clear()
                plot_gumball_with_rpy(ax, roll=roll, pitch=pitch, yaw=yaw)

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
    main()
