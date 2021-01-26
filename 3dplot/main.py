import inspect
import json
import os
import sys
from sympy import *
import numpy as np

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import Plot3D


def get_coefficient(equation, variable):
    # gets the mul for the variable
    mul = [arg for arg in equation.args if arg.is_Mul and arg.free_symbols == {variable}]

    # if the variable exists in the equation but it's not a mul, the coefficient is 1
    if equation.free_symbols.issuperset({variable}) and len(mul) == 0:
        return 1.

    # if the variable doesn't exist at all then its coefficient is 0
    if not equation.free_symbols.issuperset({variable}):
        return 0.

    # if the variable exists, get his coefficient from the mul
    return float([arg for arg in mul[0].args if arg.is_Number][0])


def main():

    # available 3D objects
    obj_types = ("point", "plane")

    # Declaring symbolic variables
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

    # extra padding for min and max axes
    extra_padding = 5

    # min and max for each coordinate
    x_lim = {"min": 0, "max": 0}
    y_lim = {"min": 0, "max": 0}
    z_lim = {"min": 0, "max": 0}

    # array of points to plot
    points = []

    # array of planes to plot
    planes = []

    # list of 3D objects to plot
    to_plot = []

    output_filename = "output"

    while True:
        # asking the user if he wants to enter more 3D objects
        try:
            choice = str(input("Do you want to use json files(y/n)? ")).upper()
            if choice == "Y" or choice == "YES":
                while True:
                    try:
                        json_file = str(input("Enter the json file name: "))
                        if os.path.isfile(
                                os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{json_file}.json")):
                            output_filename = json_file
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print("The entered file doesn't exist!")

                # reading input json file
                with open(f"{json_file}.json") as f:
                    to_plot = json.load(f)
                break
            elif choice == "N" or choice == "NO":
                while True:
                    # asking the user if he wants to enter more 3D objects
                    try:
                        if len(to_plot) > 0:
                            choice = str(input("Do you want to stop(y/n)? ")).upper()
                            if choice == "Y" or choice == "YES":
                                break
                            elif choice == "N" or choice == "NO":
                                pass
                            else:
                                raise ValueError
                    except ValueError:
                        print("The entered choice could not be understood!")

                    # asking which type of 3D object the user wants to plot
                    try:
                        obj_type = str(input("Enter the type of object to plot: ")).lower()

                        if obj_type not in obj_types:
                            raise ValueError
                    except ValueError:
                        print(f"The desired object is not available. \nObjects available are: {', '.join(obj_types)}.")
                        continue

                    # entering the correct equation for the right type of 3D object
                    try:
                        equation = str(input("Enter the object equation: ")).replace(" ", "")

                        if obj_type == obj_types[0]:  # point
                            if ord('A') <= ord(equation[0]) <= ord('Z'):  # a point has a unique letter (A -> Z)
                                name = equation[0]
                                if name in [item["name"] for item in to_plot if item["type"] == "point"]:
                                    raise ValueError
                                equation = equation.replace(equation[0], "")
                            else:
                                raise ValueError
                            if equation[0] == "(" and equation[
                                len(equation) - 1] == ")":  # removing brackets (not needed)
                                equation = equation.replace("(", "")
                                equation = equation.replace(")", "")
                            else:
                                raise ValueError

                            # getting the 3 coordinates
                            equation = equation.split(",")
                            if len(equation) != 3:
                                raise ValueError

                            # adding the point to the list of 3D objects to plot
                            to_plot.append({"name": name, "type": obj_types[0], "coordinates": {"x": float(equation[0]),
                                                                                                "y": float(equation[1]),
                                                                                                "z": float(
                                                                                                    equation[2])}})
                        elif obj_type == obj_types[1]:  # plane
                            if 'x^' in equation or 'y^' in equation or 'z^' in equation:  # the variables for a plane have no pow
                                raise ValueError

                            # translating the entered equation
                            equation = sympify(equation)

                            # check if the only variables entered are x, y and/or z
                            if not equation.free_symbols.issubset({x, y, z}) and not equation.is_scalar:
                                raise ValueError

                            # auto assigning a letter (a -> z)
                            name = chr(97 + len([item["name"] for item in to_plot if item["type"] == "plane"]))

                            # getting the right coefficient for every value
                            a = get_coefficient(equation, x)
                            b = get_coefficient(equation, y)
                            c = get_coefficient(equation, z)

                            # getting the right value for the constant d
                            d = [arg for arg in equation.args if not arg.is_Mul and not arg.is_Symbol]
                            if len(d) == 0:
                                d = 0.
                            else:
                                d = float(d[0])

                            # adding the plane to the list of 3D objects to plot
                            to_plot.append({"name": name, "type": obj_types[1], "coefficients": {"a": a,
                                                                                                 "b": b,
                                                                                                 "c": c,
                                                                                                 "d": d}})
                    except ValueError:
                        print("The object equation was written wrong!")
                break
            else:
                raise ValueError
        except ValueError:
            print("The entered choice could not be understood!")

    # reading the file and saving data into arrays
    for item in to_plot:
        if item["type"] == obj_types[0]:
            # adding point to points array
            points.append({"name": item["name"],
                           "x": item["coordinates"]["x"],
                           "y": item["coordinates"]["y"],
                           "z": item["coordinates"]["z"]})

            # calculating min and max for all axes (with the extra_padding)
            x_lim["min"] = round(min(x_lim["min"], item["coordinates"]["x"] - extra_padding))
            x_lim["max"] = round(max(x_lim["max"], item["coordinates"]["x"] + extra_padding))
            y_lim["min"] = round(min(y_lim["min"], item["coordinates"]["y"] - extra_padding))
            y_lim["max"] = round(max(y_lim["max"], item["coordinates"]["y"] + extra_padding))
            z_lim["min"] = round(min(z_lim["min"], item["coordinates"]["z"] - extra_padding))
            z_lim["max"] = round(max(z_lim["max"], item["coordinates"]["z"] + extra_padding))
        elif item["type"] == obj_types[1]:
            # function coefficients
            a = item["coefficients"]["a"]
            b = item["coefficients"]["b"]
            c = item["coefficients"]["c"]
            d = item["coefficients"]["d"]

            if a == 0 and b == 0 and c == 0:
                continue

            fill_values = np.arange(0, 10, 1.)

            if a == 0 and b == 0:
                xx, yy = np.meshgrid(fill_values, fill_values)
                zz = (xx * 0) + ((-d) * 1. / c)
            elif a == 0 and c == 0:
                xx, zz = np.meshgrid(fill_values, fill_values)
                yy = (xx * 0) + ((-d) * 1. / b)
            elif b == 0 and c == 0:
                yy, zz = np.meshgrid(fill_values, fill_values)
                xx = (yy * 0) + ((-d) * 1. / a)
            elif a == 0:
                yy, zz = np.meshgrid(fill_values, fill_values)
                yy *= b
                zz *= c
                xx = yy * a
            elif b == 0:
                xx, zz = np.meshgrid(fill_values, fill_values)
                xx *= a
                zz *= c
                yy = xx * b
            elif c == 0:
                xx, yy = np.meshgrid(fill_values, fill_values)
                xx *= a
                yy *= b
                zz = xx * c
            else:
                xx, yy = np.meshgrid(fill_values, fill_values)
                xx *= a
                yy *= b
                zz = (-a * xx - b * yy - d) * 1. / c

            # calculating min and max for all axes (with the extra_padding)
            x_lim["min"] = round(min(x_lim["min"], np.min(xx) - extra_padding))
            x_lim["max"] = round(max(x_lim["max"], np.max(xx) + extra_padding))
            y_lim["min"] = round(min(y_lim["min"], np.min(yy) - extra_padding))
            y_lim["max"] = round(max(y_lim["max"], np.max(yy) + extra_padding))
            z_lim["min"] = round(min(z_lim["min"], np.min(zz) - extra_padding))
            z_lim["max"] = round(max(z_lim["max"], np.max(zz) + extra_padding))

            # adding plane function to planes
            planes.append({"name": item["name"],
                           "x": xx,
                           "y": yy,
                           "z": zz})

    # creating a 3D space where we will plot points and planes
    space = Plot3D(10, 10, x_lim, y_lim, z_lim)

    # plotting planes
    for plane in planes:
        space.add3Dplane(plane["name"], plane["x"], plane["y"], plane["z"])

    # plotting points
    for point in points:
        space.add3Dpoint(point["name"], point["x"], point["y"], point["z"])

    # saving the 3D space to file
    space.save_to_file(output_filename, "png")


# starts script only if directly called
if __name__ == "__main__":
    main()

# TODO:
#  set max displayable size for planes,
#  adding other functions (circles and parabolas).
