import math
import random
import time

import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


from eulerscope.gumball import plot_gumball_with_rpy


def plot_gumball_with_rpy_degrees(ax, roll, pitch, yaw):
    plot_gumball_with_rpy(ax, math.radians(roll), math.radians(pitch), math.radians(yaw))

def plot(choice, ax, increment, roll, pitch, yaw):
    if choice == "D":
        roll += increment
    elif choice == "A":
        roll -= increment
    elif choice == "W":
        pitch += increment
    elif choice == "S": 
        pitch -= increment
    elif choice == "E":
        yaw += increment
    elif choice == "Q":
        yaw -= increment
    elif choice == "CLEAR" or choice == "C":
        ax.clear()
    elif choice == "RESET" or choice == "R":
        roll = pitch = yaw = 0
        ax.clear()
    elif choice == "EXIT":
        exit()

    return(roll, pitch, yaw)

def main():
    roll = pitch = yaw = 0

    increment = 4  # degrees

    plt.ion()
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    plt.draw()
        
    i = 0
    while True:
        i += 1
        if i % 1 == 100:
            ax.clear()
        
        print(f"Roll = {roll}, Pitch = {pitch}, Yaw = {yaw}")
        plot_gumball_with_rpy_degrees(ax, roll, pitch, yaw)
        choice = input('Roll: N or H; Pitch: T or C; Yaw: R or G (or CLEAR or RESET) >> ')

        choice = choice.upper()
        if len(choice) > 1:
            for c in choice:
                roll, pitch, yaw = plot(c, ax, increment, roll, pitch, yaw)

                print(f"Roll = {roll}, Pitch = {pitch}, Yaw = {yaw}")
                plot_gumball_with_rpy_degrees(ax, roll, pitch, yaw)

                plt.pause(0.4)
        else:
            roll, pitch, yaw = plot(choice, ax, increment, roll, pitch, yaw)
        
        plt.pause(0.00001)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('\n\tExiting...\n')
        exit()