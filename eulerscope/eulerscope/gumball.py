import argparse
import math

from collections import namedtuple

import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.proj3d import proj_transform
import numpy as np
import matplotlib.pyplot as plt

angles = np.linspace(0, 2 * np.pi, 30)

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
    z = [   0,   0],
    x = [-0.5, 0.5],
    y = [   0,   0],
    color = "red",
)

green_line = XYZ_Points(
    z = [0, 1],
    x = [0, 0],
    y = [0, 0],
    color = "green",
)

green_arrow = XYZ_Points(
    z = [0, 0.5],
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

from matplotlib.patches import FancyArrowPatch

class Arrow3D(FancyArrowPatch):
    def __init__(self, x, y, z, dx, dy, dz, *args, **kwargs):
        super().__init__((0,0), (0,0), *args, **kwargs)
        self._xyz = (x,y,z)
        self._dxdydz = (dx,dy,dz)

    def draw(self, renderer):
        x1,y1,z1 = self._xyz
        dx,dy,dz = self._dxdydz
        x2,y2,z2 = (x1+dx,y1+dy,z1+dz)

        xs, ys, zs = proj_transform((x1,x2),(y1,y2),(z1,z2), renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        super().draw(renderer)

def _arrow3D(ax, x, y, z, dx, dy, dz, *args, **kwargs):
    '''Add an 3d arrow to an `Axes3D` instance.'''
    arrow = Arrow3D(x, y, z, dx, dy, dz, *args, **kwargs)
    ax.add_artist(arrow)

setattr(Axes3D,'arrow3D',_arrow3D)

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

def plot_gumball_with_rpy(ax, roll, pitch, yaw, alpha=1.0):
    transformed_green_arrow = apply_roll_pitch_yaw([green_arrow], roll=yaw, pitch=pitch, yaw=roll)[0]
    tga = transformed_green_arrow
    ax.arrow3D(tga.x[0], tga.z[0], tga.y[0],
               tga.x[1]-tga.x[0], tga.z[1]-tga.z[0], tga.y[1]-tga.y[0],
               # alpha=0.5,
               mutation_scale=35,
               ec ='black',
               fc='green')
    #
    #   Roll and Yaw need to be swapped!
    #
    transformed_items = apply_roll_pitch_yaw(items, roll=yaw, pitch=pitch, yaw=roll)
    for item in transformed_items:
        ax.plot(item.x, item.z, item.y, color=item.color, alpha=alpha)

def plot_gumball_with_rpy_with_old(ax, roll, pitch, yaw):
    assert len(roll) == len(pitch) == len(yaw)
    alpha_vals = list(np.linspace(0.1, 1.0, len(roll)))

    i = 0
    for j in range(0, len(roll)):
        plot_gumball_with_rpy(ax, roll[j], pitch[j], yaw[j], alpha_vals[i])
        i += 1
        if len(alpha_vals) <= i:
            i = 0


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

