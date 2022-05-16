import numpy as np
from matplotlib import pyplot as plt

data = np.array([
    [0, 0.000],
    [2, 0.001],
    [4, 0.002],
    [8, 0.007],
    [12, 0.057],
    [16, 0.277],
    [20, 1.551],
    [24, 6.173],
    [0, 0.000],
    [2, 0.000],
    [4, 0.000],
    [8, 0.000],
    [12, 0.002],
    [16, 0.015],
    [20, 0.036],
    [24, 0.288],
    [0, 0.000],
    [2, 0.000],
    [4, 0.000],
    [8, 0.000],
    [12, 0.000],
    [16, 0.001],
    [20, 0.005],
    [24, 0.028]
])
xCoods=[]
yCoods=[]
for i in data:
    xCoods.append(i[0])
    yCoods.append(i[1])
plt.title("Plot of Time Taken vs Puzzle Depth")
plt.plot(xCoods[0:8], yCoods[0:8], color="r", label="UFC")
plt.plot(xCoods[8:16], yCoods[8:16], color="g", label="A* with Misplaced Tiles")
plt.plot(xCoods[16:24], yCoods[16:24], color="b", label="A* with Manhattan Distance")
plt.xlabel("X = Puzzle Depth Size")
plt.ylabel("Y = Time Taken (Seconds)")
plt.legend()
plt.show()

data2 = np.array([
    [0, 1],
    [2, 7],
    [4, 33],
    [8, 311],
    [12, 2328],
    [16, 13710],
    [20, 54666],
    [24, 135274],
    [0, 1],
    [2, 3],
    [4, 5],
    [8, 19],
    [12, 126],
    [16, 608],
    [20, 2170],
    [24, 15320],
    [0, 1],
    [2, 3],
    [4, 5],
    [8, 13],
    [12, 25],
    [16, 71],
    [20, 311],
    [24, 1611]
])
xCoods=[]
yCoods=[]
for i in data2:
    xCoods.append(i[0])
    yCoods.append(i[1])
plt.title("Plot of Nodes Explored vs Puzzle Depth")
plt.plot(xCoods[0:8], yCoods[0:8], color="r", label="UFC")
plt.plot(xCoods[8:16], yCoods[8:16], color="g", label="A* with Misplaced Tiles")
plt.plot(xCoods[16:24], yCoods[16:24], color="b", label="A* with Manhattan Distance")
plt.xlabel("X = Puzzle Depth Size")
plt.ylabel("Y = No. of Nodes Explored")
plt.legend()
plt.show()