import inspect
import json
import os
import sys
from sympy import Symbol
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import Plot3D


def main():
    # reading input json file
    with open('input.json') as f:
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
            points.append({"x": item["coordinates"]["x"],
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
            # declaring plane function
            f = lambda x, y, z: a*x + b*y + c*z + d
            # adding plane function to planes
            planes.append(f)
            pass
        else:
            print("The entered json file was wrongly written!")
            exit(1)

    # creating a 3D space where we will plot points and planes
    space = Plot3D(4, 4, x_lim, y_lim, z_lim)
    # plotting points
    for point in points:
        space.add3Dpoint(point["x"], point["y"], point["z"])
    # plotting planes
    for plane in planes:
        space.add3Dplane()
    # saving the 3D space to file
    space.save_to_file("output", "png")


# starts script only if directly called
if __name__ == "__main__":
    main()
