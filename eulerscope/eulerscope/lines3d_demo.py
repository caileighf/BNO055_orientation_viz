import math

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt


"""
x = cos(yaw) * cos(pitch)
y = sin(yaw) * cos(pitch)
z = sin(pitch)

"""


def plot_roll(ax, roll_angle):
    color = "blue"

    # These may need to be flipped around to get it to match your inputs.
    x = [0, np.cos(roll_angle)]
    y = [0, 0]
    z = [0, np.sin(roll_angle)]
    ax.plot(x, y, z, label='pitch', color=color)

    # These should be fine since they just draw a circle, but if you change which axis is zero above, 
    # change it here too.
    angle = np.linspace(0, 2 * np.pi, 100)
    x = np.sin(angle)
    y = angle * 0
    z = np.cos(angle)
    ax.plot(x, y, z, color=color)


def plot_pitch(ax, pitch_angle, yaw_angle):
    color = "green"
        
    # These may need to be flipped around to get it to match your inputs.
    x = [0, 0]
    y = [0, np.cos(pitch_angle)]
    z = [0, np.sin(pitch_angle)]
    ax.plot(x, y, z, label='pitch', color=color)

    # These should be fine since they just draw a circle, but if you change which axis is zero above, 
    # change it here too.
    angle = np.linspace(0, 2 * np.pi, 100)
    x = angle * 0
    y = np.cos(angle)
    z = np.sin(angle)
    ax.plot(x, y, z, color=color)


def plot_yaw(ax, yaw_angle):
    color = "red"
    
    # These may need to be flipped around to get it to match your inputs.
    x = [0, np.sin(yaw_angle)]
    y = [0, np.cos(yaw_angle)]
    z = [0, 0]
    ax.plot(x, y, z, label='yaw', color=color)
    
    # These should be fine since they just draw a circle, but if you change which axis is zero above, 
    # change it here too.
    angle = np.linspace(0, 2 * np.pi, 100)
    x = np.sin(angle)
    y = np.cos(angle)
    z = angle * 0
    ax.plot(x, y, z, color=color)



if __name__ == "__main__":
    # demonstrate / test capabilities

    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    plot_yaw(ax, math.radians(45))
    plt.show()
    
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, z, label='parametric curve')
    ax.legend()
    
    plt.show()
