import csv
from simple_data_plotting_lib import OnlyColumnsTable, MultipleLinesGraph

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
            tmp = int(input("Inserire costante Ricavo/Quantità: "))
            if tmp <= 0:
                raise ValueError
            else:
                constant = (tmp, )
                break
        except ValueError:
            print("La costante deve essere un numero positivo!")

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
        outcome.append("Profitto" if item > 0 else "Non Profitto")

    # assembling all the data gathered
    table_data = {
        "Quantità": [item for item in range(quantity)],
        "Ricavi": proceeds,
        "Costi": costs,
        "Profitti": profits,
        "ΔRicavi": marginal_proceeds,
        "ΔCosti": marginal_costs,
        "ΔProfitti": marginal_profits,
        "Conclusione": outcome
    }

    table = OnlyColumnsTable(f"Tabella dei Margini (k = {constant[0]})", 20)    # creates a new table
    table.fill(table_data)  # fills the newly created table
    table.format(15, 15)    # formats the table
    table.save_to_file("table", "png")   # saves the table to .png

    graph = MultipleLinesGraph(f"Costi/Ricavi Azienda (k = {constant[0]})", "Quantità", "Prezzi", 15, 15, 20)     # creates a new graph
    graph.add_line(range(quantity), costs, "Costi")     # adding the costs line
    graph.add_line(range(quantity), proceeds, "Ricavi")     # adding the proceeds line
    graph.set_legend("lower right", 20)         # setting up the legend
    graph.show_values_in_x_axis(range(quantity))        # enables better viewing of quantity values
    graph.show_values_in_y_axis(costs)      # enables better viewing of costs values
    graph.save_to_file("graph", "png")       # saves the graph to .png (all the others picture formats work as well)


# starts script only if directly called
if __name__ == "__main__":
    main()