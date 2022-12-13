import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math as m

def cart2sph(x,y,z):
    XsqPlusYsq = x**2 + y**2
    r = m.sqrt(XsqPlusYsq + z**2)               # r
    elev = m.atan2(z,m.sqrt(XsqPlusYsq))     # theta
    az = m.atan2(y,x)                           # phi
    return r, elev, az

def cart2sphA(pts):
    return np.array([cart2sph(x,y,z) for x,y,z in pts])

def appendSpherical(xyz):
    np.hstack((xyz, cart2sphA(xyz)))
    
# Sphere

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
a,b,c = cart2sph(1,1,1)
r = a #radius
u, v = np.mgrid[0:2 *np.pi:30j,0:np.pi:20j]
# np.mgrid[b:2 *np.pi:30j,c:np.pi:20j]
# np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
# D = 19.1
# P = 7.9
# H = 9.3

D = r*(np.cos(u) * np.sin(v))+10
P = r*(np.sin(u) * np.sin(v))+10
H = r*(np.cos(v))+10
ax.plot_surface(D, P, H, cmap=plt.cm.YlGnBu_r)
# Single Points
ax.scatter(4,4,4)
plt.show()