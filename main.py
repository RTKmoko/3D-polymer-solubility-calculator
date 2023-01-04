import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import math as m
import json
from pathlib import Path
import itertools

colors = itertools.cycle(["r", "b", "g"])

DATA_FILE = Path('data.json')



def distance(point1, point2):
  x1, y1, z1 = point1
  x2, y2, z2 = point2
  return m.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def load_data():
    return json.loads(DATA_FILE.read_text())


def main():
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    u, v = np.mgrid[0:2 * np.pi:1000j, 0:np.pi:1000j]
    # np.mgrid[b:2 *np.pi:30j,c:np.pi:20j]
    # np.mgrid[0:2 * np.pi:30j, 0:np.pi:20j]

    data = load_data()

    for poly in data['polymer']:
        if not poly['enabled']:
            continue
        # Sphere
        ax.set_aspect('equal')
        #TODO a bug after this line that makes the program start not from the normal viewing point
        R = poly['r']
        D = R*(np.cos(u) * np.sin(v))+(poly['d'])
        P = R*(np.sin(u) * np.sin(v))+(poly['p'])
        H = R*(np.cos(v))+(poly['h'])
        ax.plot_surface(D, P, H, cmap='gray', alpha=0.4)
        print(f"for polymere {poly['name']}")
        for sol in data['solvent']:
            if not sol['enabled']:
                continue
            centerSphere = (poly['d'], poly['p'], poly['h'])
            pointOfSol = (sol['d'], sol['p'], sol['h'])
            if R == distance(centerSphere, pointOfSol):
                x = distance(centerSphere, pointOfSol)/R
                print(f"the RED for solvent {sol['name']} is : {x}")
            elif R > distance(centerSphere, pointOfSol):
                x = distance(centerSphere, pointOfSol)/R
                print(f"the RED for solvent {sol['name']} is : {x} (R is smaller than distance)")
            else:
                x = distance(centerSphere, pointOfSol)/R
                print(f"the RED is for solvent {sol['name']} : {x} (R is bigger than distance)")


    for sol in data['solvent']:
        if not sol['enabled']:
            continue
        # Single point
        ax.scatter(sol['d'], sol['p'], sol['h'],c=next(colors))
    plt.show()



if __name__ == '__main__':
    main()
