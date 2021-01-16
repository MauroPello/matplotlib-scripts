import inspect
import json
import os
import sys
from sympy import Symbol
import numpy as np
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import Plot3D


def main():
    json_file = None
    while True:
        try:
            json_file = str(input("Enter the json file name: "))
            if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{json_file}.json")):
                break
            else:
                raise ValueError
        except ValueError:
            print("The entered file doesn't exist!")

    # reading input json file
    with open(f"{json_file}.json") as f:
        to_plot = json.load(f)

    # Declaring symbolic variables
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    # min and max for each coordinate
    x_lim = {"min": 0, "max": 0}
    y_lim = {"min": 0, "max": 0}
    z_lim = {"min": 0, "max": 0}
    # extra padding for min and max axes
    extra_padding = 5
    # array of points to plot
    points = []
    # array of planes to plot
    planes = []

    # reading the file and saving data into arrays
    for item in to_plot:
        if item["type"] == "point":
            # adding point to points array
            points.append({"name": item["name"],
                           "x": item["coordinates"]["x"],
                           "y": item["coordinates"]["y"],
                           "z": item["coordinates"]["z"]})

            # calculating min and max for all axes (with the extra_padding)
            x_lim["min"] = min(x_lim["min"], item["coordinates"]["x"] - extra_padding)
            x_lim["max"] = max(x_lim["max"], item["coordinates"]["x"] + extra_padding)
            y_lim["min"] = min(y_lim["min"], item["coordinates"]["y"] - extra_padding)
            y_lim["max"] = max(y_lim["max"], item["coordinates"]["y"] + extra_padding)
            z_lim["min"] = min(z_lim["min"], item["coordinates"]["z"] - extra_padding)
            z_lim["max"] = max(z_lim["max"], item["coordinates"]["z"] + extra_padding)
        elif item["type"] == "plane":
            # function coefficients
            a = item["coefficients"]["a"]
            b = item["coefficients"]["b"]
            c = item["coefficients"]["c"]
            d = item["coefficients"]["d"]

            if a == 0 and b == 0 and c == 0:
                continue

            if a == 0 and b == 0:
                xx, yy = np.meshgrid(range(10), range(10))
                zz = (xx * 0) + ((-d) * 1. / c)
            elif a == 0 and c == 0:
                xx, zz = np.meshgrid(range(10), range(10))
                yy = (xx * 0) + ((-d) * 1. / b)
            elif b == 0 and c == 0:
                yy, zz = np.meshgrid(range(10), range(10))
                xx = (yy * 0) + ((-d) * 1. / a)
            elif a == 0:
                yy, zz = np.meshgrid(range(10), range(10))
                yy *= b
                zz *= c
                xx = yy * a
            elif b == 0:
                xx, zz = np.meshgrid(range(10), range(10))
                xx *= a
                zz *= c
                yy = xx * b
            elif c == 0:
                xx, yy = np.meshgrid(range(10), range(10))
                xx *= a
                yy *= b
                zz = xx * c
            else:
                xx, yy = np.meshgrid(range(10), range(10))
                xx *= a
                yy *= b
                zz = (-a * xx - b * yy - d) * 1. / c

            # calculating min and max for all axes (with the extra_padding)
            x_lim["min"] = min(x_lim["min"], np.min(xx) - extra_padding)
            x_lim["max"] = max(x_lim["max"], np.max(xx) + extra_padding)
            y_lim["min"] = min(y_lim["min"], np.min(yy) - extra_padding)
            y_lim["max"] = max(y_lim["max"], np.max(yy) + extra_padding)
            z_lim["min"] = min(z_lim["min"], np.min(zz) - extra_padding)
            z_lim["max"] = max(z_lim["max"], np.max(zz) + extra_padding)

            # adding plane function to planes
            planes.append({"name": item["name"],
                           "x": xx,
                           "y": yy,
                           "z": zz})
            pass
        else:
            print("The entered json file was wrongly written!")
            exit(1)

    # creating a 3D space where we will plot points and planes
    space = Plot3D(10, 10, x_lim, y_lim, z_lim)

    # plotting planes
    for plane in planes:
        space.add3Dplane(plane["name"], plane["x"], plane["y"], plane["z"])

    # plotting points
    for point in points:
        space.add3Dpoint(point["name"], point["x"], point["y"], point["z"])

    # saving the 3D space to file
    space.save_to_file(json_file, "png")


# starts script only if directly called
if __name__ == "__main__":
    main()

# TODO:
#  set max displayable size for planes,
#  adding other functions (circles and parabolas).
