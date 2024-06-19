import os

version_file = 'C:\\Users\\rtkmo\\Documents\\3D-polymer-solubility-calculator\\polimer_solibity_calculator\\version.py'

if os.path.isfile(version_file):
    print("Version file exists.")
else:
    print("Version file does not exist.")
