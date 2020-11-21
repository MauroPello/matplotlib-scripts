import sys
import os
import inspect
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import OnlyColumnsTable, MultipleLinesGraph
import csv


# functions that returns a new array where every value has been subtracted by the one before
def calculate_margin(arr):
    tmp = [0]
    for i in range(1, len(arr)):
        tmp.append(arr[i] - arr[i - 1])
    return tmp


def main():
    # the user types the constant (ex. 7)
    while True:
        try:
            tmp = int(input("Enter Costs/Proceeds constant: "))
            if tmp <= 0:
                raise ValueError
            else:
                constant = (tmp, )
                break
        except ValueError:
            print("The constant has to be a positive number!")

    # reads the production costs for n products manufactured starting from 0
    costs = []
    with open('costs.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            for item in row:
                costs.append(int(item))

    # total products quantity
    quantity = len(costs)

    # calculates proceeds (list comprehension)
    proceeds = [item * constant[0] for item in range(quantity)]

    # calculates profits (list comprehension)
    profits = [proceeds[i] - costs[i] for i in range(quantity)]

    # calculates the margin for every factor
    marginal_proceeds = calculate_margin(proceeds)
    marginal_costs = calculate_margin(costs)
    marginal_profits = calculate_margin(profits)

    # calculates whether or not the company is doing good and profiting from it's products
    outcome = []
    for item in marginal_profits:
        outcome.append("Profit" if item > 0 else "No Profit")

    # assembling all the data gathered
    table_data = {
        "Quantity": [item for item in range(quantity)],
        "Proceeds": proceeds,
        "Costs": costs,
        "Profits": profits,
        "ΔProceeds": marginal_proceeds,
        "ΔCosts": marginal_costs,
        "ΔProfits": marginal_profits,
        "Outcome": outcome
    }

    table = OnlyColumnsTable(f"Profits Table (k = {constant[0]})", 20)    # creates a new table
    table.fill(table_data)  # fills the newly created table
    table.format(15, 15)    # formats the table
    table.save_to_file("table", "png")   # saves the table to .png

    graph = MultipleLinesGraph(f"Costs/Proceeds (k = {constant[0]})", "Quantity", "Prices", 15, 15, 20)     # creates a new graph
    graph.add_line(range(quantity), costs, "Costs")     # adding the costs line
    graph.add_line(range(quantity), proceeds, "Proceeds")     # adding the proceeds line
    graph.set_legend("lower right", 20)         # setting up the legend
    graph.show_values_in_x_axis(range(quantity))        # enables better viewing of quantity values
    graph.show_values_in_y_axis(costs)      # enables better viewing of costs values
    graph.save_to_file("graph", "png")       # saves the graph to .png (all the others picture formats work as well)


# starts script only if directly called
if __name__ == "__main__":
    main()
