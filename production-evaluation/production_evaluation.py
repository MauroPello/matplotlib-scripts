import sys
import os
import inspect
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import OnlyColumnsTable, MultipleLinesGraph
from numpy import append, zeros, array, arange
from scipy.optimize import fsolve


def function(x, *data):
    coefficients, constants = data
    y = zeros(len(coefficients))
    for i in range(len(coefficients)):
        y[i] = coefficients[i] * x[1] + constants[i] - x[0]
    return y


def main():
    costs = {
        "coefficient": 0,
        "constant": 0
    }

    while True:
        try:
            if (tmp := float(input("Enter the production costs for an item: "))) < 0:
                raise ValueError
            else:
                costs["coefficient"] = tmp
                break
        except ValueError:
            print("The fixed costs number has to be a positive number!")

    while True:
        try:
            if (tmp := float(input("Enter the fixed costs for the company: "))) < 0:
                raise ValueError
            else:
                costs["constant"] = tmp
                break
        except ValueError:
            print("The fixed costs number has to be a positive number!")

    while True:
        try:
            if (item_price := float(input("Enter the item price: "))) <= 0:
                raise ValueError
            else:
                break
        except ValueError:
            print("The item price has to be a positive number!")

    # get the intersections
    intersection = tuple(fsolve(function, array([0, 0]), ([costs['coefficient'], item_price], [costs['constant'], 0])))
    if intersection[0] <= 0 or intersection[1] <= 0 or len(intersection) == 0:
        print("There is no intersection!")
        exit(1)

    intersection = (round(intersection[1], 3), round(intersection[0], 3))

    # get the max graph value for the x coordinate
    max_x_value = 2 * intersection[0]
    x_values = append(arange(0, max_x_value, round(max_x_value/15, 1)), max_x_value).round(1).tolist()

    # get the max graph value for the y coordinate
    max_y_value = 2 * intersection[1]
    y_values = append(arange(0, max_y_value, round(max_y_value/15, 1)), max_y_value).round(1).tolist()

    # makes the graph
    graph = MultipleLinesGraph(f"Production Evaluation\nBreak-Even Point: {intersection[0]} items for {intersection[1]}$", "Costs", "Prices", 15, 15, 15)  # creates a new graph

    y = [costs["coefficient"] * number + costs["constant"] for number in x_values]
    graph.add_line(x_values, y, "Costs")

    y = [item_price * number for number in x_values]
    graph.add_line(x_values, y, "Prices")

    graph.show_values_in_x_axis(append(x_values, intersection[0]).tolist())
    graph.show_values_in_y_axis(append(y_values, intersection[1]).tolist())

    graph.set_legend("lower right", 20)  # setting up the legend

    graph.add_point(intersection[0], intersection[1])

    graph.save_to_file("graph", "png")  # saves the graph to .png (all the others picture formats work as well)


# starts script only if directly called
if __name__ == "__main__":
    main()
