import argparse
import math

from collections import namedtuple

import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

angles = np.linspace(0, 2 * np.pi, 100)


"""
z = forward/back
x = left/right
y = up/down
"""

XYZ_Points = namedtuple("XYZ_Points", "x y z color")

red_circle = XYZ_Points(
    z = np.sin(angles),
    x = np.cos(angles),
    y = angles * 0,
    color = "red",
)

green_circle = XYZ_Points(
    z = np.cos(angles),
    x = angles * 0,
    y = np.sin(angles),
    color = "green",
)

blue_circle = XYZ_Points(
    z = angles * 0,
    x = np.sin(angles),
    y = np.cos(angles),
    color = "blue",
)

red_line = XYZ_Points(
    z = [0, 0],
    x = [-0.5, 0.5],
    y = [0, 0],
    color = "red",
)

green_line = XYZ_Points(
    z = [0, 1],
    x = [0, 0],
    y = [0, 0],
    color = "green",
)

blue_line = XYZ_Points(
    z = [0, 0],
    x = [0, 0],
    y = [0, 1],
    color = "blue",
)

# Worked well-ish with matrixes ordered roll, pitch, yaw
def __apply_roll_pitch_yaw(items, roll=0, pitch=0, yaw=0):
    return _apply_roll_pitch_yaw(items, roll=pitch, pitch=yaw, yaw=roll)

def apply_roll_pitch_yaw(items, roll=0, pitch=0, yaw=0):
    return _apply_roll_pitch_yaw(items, roll=pitch, pitch=yaw, yaw=roll)

def _apply_roll_pitch_yaw(items, roll=0, pitch=0, yaw=0):
    roll_matrix = np.array([
        [1,              0,               0],
        [0, math.cos(roll), -math.sin(roll)],
        [0, math.sin(roll),  math.cos(roll)],
    ])

    pitch_matrix = np.array([
        [math.cos(pitch), 0, -math.sin(pitch)],
        [              0, 1,                0],
        [math.sin(pitch), 0,  math.cos(pitch)],
    ])
    
    yaw_matrix = np.array([
        [math.cos(yaw), -math.sin(yaw), 0],
        [math.sin(yaw),  math.cos(yaw), 0],
        [            0,              0, 1],

    ])

    result = []
    for item in items:
        assert len(item.x) == len(item.y) == len(item.z)
        xs, ys, zs = [], [], []

        for x, y, z in zip(item.x, item.y, item.z):
            vector = np.array((x, y, z))
            vector = np.matmul(vector, yaw_matrix)
            vector = np.matmul(vector, pitch_matrix)
            vector = np.matmul(vector, roll_matrix)

            xs.append(vector[0])
            ys.append(vector[1])
            zs.append(vector[2])

        result.append(XYZ_Points(x=xs, y=ys, z=zs, color=item.color))
    return result


items = [red_circle, green_circle, blue_circle,
         red_line, green_line, blue_line] 


def plot_gumball(ax):
    for item in items:
        ax.plot(item.x, item.z, item.y, color=item.color)


def plot_gumball_with_rpy(ax, roll, pitch, yaw):
    transformed_items = apply_roll_pitch_yaw(items, roll=roll, pitch=pitch, yaw=yaw)
    for item in transformed_items:
        ax.plot(item.x, item.z, item.y, color=item.color)


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--roll", type=float, required=True)      # actually does pitch
    argparser.add_argument("--pitch", type=float, required=True)     # actually does yaw
    argparser.add_argument("--yaw", type=float, required=True)       # actually does roll
    args=argparser.parse_args()

    pitch = args.roll
    yaw = args.pitch
    roll = args.yaw

    # Demonstrate the function.

    # demonstrate / test capabilities

    mpl.rcParams['legend.fontsize'] = 10

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # plot_gumball(ax)

    plot_gumball_with_rpy(
        ax, 
        roll=math.radians(roll), 
        pitch=math.radians(pitch), 
        yaw=math.radians(yaw),
    )
    plt.show()

