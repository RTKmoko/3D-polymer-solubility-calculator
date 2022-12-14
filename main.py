import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math as m

SPH_D_PARAMETER = float(input('Enter D of the sphere: '))
SPH_P_PARAMETER = float(input('Enter P of the sphere: '))
SPH_H_PARAMETER = float(input('Enter H of the sphere: '))
SPH_R_PARAMETER = float(input('Enter R of the sphere: '))

S_D_PARAM = float(input('Enter D of the solvent: '))
S_P_PARAM = float(input('Enter P of the solvent: '))
S_H_PARAM = float(input('Enter H of the solvent: '))


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
def sphere(SPH_D_PARAMETER, SPH_P_PARAMETER, SPH_H_PARAMETER, SPH_R_PARAMETER):
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    a,b,c = cart2sph(SPH_R_PARAMETER,1,1)
    r = a #radius
    u, v = np.mgrid[0:2 *np.pi:1000j,0:np.pi:1000j]
    # np.mgrid[b:2 *np.pi:30j,c:np.pi:20j]
    # np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]
    # D = 19.1
    # P = 7.9
    # H = 9.3

    D = r*(np.cos(u) * np.sin(v))+SPH_D_PARAMETER
    P = r*(np.sin(u) * np.sin(v))+SPH_P_PARAMETER
    H = r*(np.cos(v))+SPH_H_PARAMETER
    ax.plot_surface(D, P, H, cmap='gray',alpha=0.3)
    #single point
    def single_point(S_D_PARAM,S_P_PARAM,S_H_PARAM):
        ax.scatter(S_D_PARAM,S_P_PARAM,S_H_PARAM)
    
    
    single_point(S_D_PARAM,S_P_PARAM,S_H_PARAM)
    
    plt.show()
    
sphere(SPH_D_PARAMETER, SPH_P_PARAMETER, SPH_H_PARAMETER, SPH_R_PARAMETER)