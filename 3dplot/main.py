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


def get_json():
    while True:
        try:
            json_file = str(input("Enter the json file name: "))
            if os.path.isfile(
                    os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{json_file}.json")):
                return json_file
            else:
                raise ValueError
        except ValueError:
            print("The entered file doesn't exist!")


def main():
    # common variables

    # available 3D objects
    obj_types = ("point", "plane")

    # Declaring symbolic variables
    x = Symbol('x')
    y = Symbol('y')
    z = Symbol('z')

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


    #CLI menu
    while True:
        # asking the user if he wants to enter more 3D objects
        try:
            choice = str(input("Do you want to use json files(y/n)? ")).upper()
            if choice == "Y" or choice == "YES":
                output_filename = get_json()

                # reading input json file
                with open(f"{output_filename}.json") as f:
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
        elif item["type"] == obj_types[1]:
            # function coefficients
            a = item["coefficients"]["a"]
            b = item["coefficients"]["b"]
            c = item["coefficients"]["c"]
            d = item["coefficients"]["d"]

            if a == 0 and b == 0 and c == 0:
                continue

            fill_values = np.linspace(0, 10, 10)

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
                xx = yy * a
            elif b == 0:
                xx, zz = np.meshgrid(fill_values, fill_values)
                yy = xx * b
            elif c == 0:
                xx, yy = np.meshgrid(fill_values, fill_values)
                zz = xx * c
            else:
                xx, yy = np.meshgrid(fill_values, fill_values)
                zz = (-a * xx - b * yy - d) * 1. / c

            # saving first calculation of planes
            planes.append({"name": item["name"],
                           "x": xx,
                           "y": yy,
                           "z": zz})

    # calculating all mins and maxes
    if len(points) > 0:
        x_lim["min"] = round(min(x_lim["min"], np.min([point["x"] for point in points])))
        x_lim["max"] = round(max(x_lim["max"], np.max([point["x"] for point in points])))
        y_lim["min"] = round(min(y_lim["min"], np.min([point["y"] for point in points])))
        y_lim["max"] = round(max(y_lim["max"], np.max([point["y"] for point in points])))
        z_lim["min"] = round(min(z_lim["min"], np.min([point["z"] for point in points])))
        z_lim["max"] = round(max(z_lim["max"], np.max([point["z"] for point in points])))

    if len(planes) > 0:
        x_lim["min"] = round(min(x_lim["min"], np.min([np.min(plane["x"]) for plane in planes])))
        x_lim["max"] = round(max(x_lim["max"], np.max([np.max(plane["x"]) for plane in planes])))
        y_lim["min"] = round(min(y_lim["min"], np.min([np.min(plane["y"]) for plane in planes])))
        y_lim["max"] = round(max(y_lim["max"], np.max([np.max(plane["y"]) for plane in planes])))
        z_lim["min"] = round(min(z_lim["min"], np.min([np.min(plane["z"]) for plane in planes])))
        z_lim["max"] = round(max(z_lim["max"], np.max([np.max(plane["z"]) for plane in planes])))

    refined_planes = []

    # recalculating planes to fit the Axes
    for item in to_plot:
        if item["type"] == obj_types[1]:
            # function coefficients
            a = item["coefficients"]["a"]
            b = item["coefficients"]["b"]
            c = item["coefficients"]["c"]
            d = item["coefficients"]["d"]

            if a == 0 and b == 0 and c == 0:
                continue

            if a == 0 and b == 0:
                xx, yy = np.meshgrid(np.linspace(x_lim["min"], x_lim["max"], 10), np.linspace(y_lim["min"], y_lim["max"], 10))
                zz = (xx * 0) + ((-d) * 1. / c)
            elif a == 0 and c == 0:
                xx, zz = np.meshgrid(np.linspace(x_lim["min"], x_lim["max"], 10), np.linspace(z_lim["min"], z_lim["max"], 10))
                yy = (xx * 0) + ((-d) * 1. / b)
            elif b == 0 and c == 0:
                yy, zz = np.meshgrid(np.linspace(y_lim["min"], y_lim["max"], 10), np.linspace(z_lim["min"], z_lim["max"], 10))
                xx = (yy * 0) + ((-d) * 1. / a)
            elif a == 0:
                yy, zz = np.meshgrid(np.linspace(y_lim["min"], y_lim["max"], 10), np.linspace(z_lim["min"], z_lim["max"], 10))
                xx = yy * a
            elif b == 0:
                xx, zz = np.meshgrid(np.linspace(x_lim["min"], x_lim["max"], 10), np.linspace(z_lim["min"], z_lim["max"], 10))
                yy = xx * b
            elif c == 0:
                xx, yy = np.meshgrid(np.linspace(x_lim["min"], x_lim["max"], 10), np.linspace(y_lim["min"], y_lim["max"], 10))
                zz = xx * c
            else:
                xx, yy = np.meshgrid(np.linspace(x_lim["min"], x_lim["max"], 10), np.linspace(y_lim["min"], y_lim["max"], 10))
                zz = (-a * xx - b * yy - d) * 1. / c

            # saving the refined planes
            refined_planes.append({"name": item["name"],
                           "x": xx,
                           "y": yy,
                           "z": zz})

    # creating a 3D space where we will plot points and planes
    space = Plot3D(10, 10, x_lim, y_lim, z_lim)

    # plotting planes
    for plane in refined_planes:
        space.add3Dplane(plane["name"], plane["x"], plane["y"], plane["z"])

    # plotting points
    for point in points:
        space.add3Dpoint(point["name"], point["x"], point["y"], point["z"])

    # enabling the legend
    space.show_legend()

    # saving the 3D space to file
    space.save_to_file(output_filename, "png")


# starts script only if directly called
if __name__ == "__main__":
    main()

# TODO:
#  adding other functions (circles and parabolas).
