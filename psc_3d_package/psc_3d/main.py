import numpy as np
import matplotlib.pyplot as plt
import math as m
import json
from pathlib import Path
import itertools

colors = itertools.cycle(["r", "b", "g", "y", "c", "m", "k"])

DATA_FILE = Path('data.json')


def distance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


def load_data():
    return json.loads(DATA_FILE.read_text())


def main():
    plt.rcParams["figure.figsize"] = [10, 8]
    plt.rcParams["figure.autolayout"] = True

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    data = load_data()

    for poly in data['polymer']:
        if not poly['enabled']:
            continue
        R = poly['r']
        u, v = np.mgrid[0:2 * np.pi:100j, 0:np.pi:50j]
        D = R * np.cos(u) * np.sin(v) + poly['d']
        P = R * np.sin(u) * np.sin(v) + poly['p']
        H = R * np.cos(v) + poly['h']
        ax.plot_surface(D, P, H, color='gray', alpha=0.4)
        print(f"For polymer {poly['name']}:")
        centerSphere = (poly['d'], poly['p'], poly['h'])
        for sol in data['solvent']:
            if not sol['enabled']:
                continue

            pointOfSol = (sol['d'], sol['p'], sol['h'])
            dist = distance(centerSphere, pointOfSol)
            x = dist / R

            if dist == R:
                status = "exactly on the surface"
            elif dist < R:
                status = "inside the sphere"
            else:
                status = "outside the sphere"

            print(f"  The RED for solvent {sol['name']} is: {x:.2f} ({status})")
    for sol in data['solvent']:
        if not sol['enabled']:
            continue
        ax.scatter(sol['d'], sol['p'], sol['h'], c=next(colors), label=sol['name'])
    ax.set_xlabel('D-axis')
    ax.set_ylabel('P-axis')
    ax.set_zlabel('H-axis')
    ax.legend()
    ax.view_init(elev=20, azim=30)  # Adjust the viewing angle for better visualization
    plt.savefig('test.png')
    plt.show()



if __name__ == '__main__':
    main()

