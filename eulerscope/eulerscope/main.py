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

# Throttle the while loop to 100 iterations per second.
loop_minimum_seconds = 0.25


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
                print(match.groups())
                a, b, c = match.groups()
                roll, pitch, yaw = math.radians(float(a)), math.radians(float(b)), math.radians(float(c))
                
                
                #####
                ###   UPDATE PLOT
                #####
                
                
                ax.clear()
                # plot_roll(ax, math.radians(roll))
                # plot_pitch(ax, math.radians(pitch))
                # plot_yaw(ax, math.radians(yaw))
                plot_gumball_with_rpy(ax, roll=roll, pitch=pitch, yaw=yaw)

                ax.set_xlim(-1, 1)
                ax.set_ylim(-1, 1)
                ax.set_zlim(-1, 1)

                #####
                ###   UPDATE PLOT
                #####

            # else:
            #     print("No match on line {!r}.".format(line))
            
        # Throttle.        
        required_sleep = next_iteration_earliest_allowed_start - time.time()
        if required_sleep > 0:
            # print("Sleeping for {}s.".format(required_sleep))
            # time.sleep(required_sleep)
            plt.pause(required_sleep)

def main():
    monitor_imu()


if __name__ == "__main__":
    main()
