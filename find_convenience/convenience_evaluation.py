from simple_data_plotting_lib import OnlyColumnsTable, MultipleLinesGraph
from numpy import append, zeros, array, arange
from scipy.optimize import fsolve


def function(x, *data):
    coefficients, constants = data
    y = zeros(len(coefficients))
    for i in range(len(coefficients)):
        y[i] = coefficients[i] * x[1] + constants[i] - x[0]
    return y


def main():
    while True:
        try:
            count = int(input("Enter the number of companies: "))
            if count <= 0:
                raise ValueError
            else:
                break
        except ValueError:
            print("The number of companies has to be a positive integer!")

    companies = []

    for index in range(count):
        name = str(input("Enter the company name: "))
        while True:
            try:
                coefficient = float(input("Enter the company coefficient: "))
                if coefficient <= 0:
                    raise ValueError
                else:
                    break
            except ValueError:
                print("The company coefficient has to be a positive number!")
        while True:
            try:
                constant = float(input("Enter the company constant: "))
                break
            except ValueError:
                print("The company constant has to be a number!")
        companies.append(dict(name=name, coefficient=coefficient, constant=constant))

    # get all the intersections
    companies_intersections = []
    for i in range(count):
        for j in range(i + 1, count):
            companies_intersections.append(tuple(filter(lambda num: True if num > 0 else False, fsolve(function, array([0, 0]), (
                [companies[i]['coefficient'], companies[j]['coefficient']],
                [companies[i]['constant'], companies[j]['constant']])))))
    companies_intersections = sorted(companies_intersections, key=lambda k: (k[1], k[0]))
    companies_intersections = [(round(intersection[1], 3), round(intersection[0], 3)) for intersection in companies_intersections]

    # get the max graph value for the x coordinate
    max_x_value = 2 * companies_intersections[0][0] + companies_intersections[len(companies_intersections) - 1][0]
    x_values = append(arange(0, max_x_value, round(max_x_value/15, 1)), max_x_value).round(1).tolist()

    # get the max graph value for the y coordinate
    max_y_value = companies_intersections[0][1] + companies_intersections[len(companies_intersections) - 1][1]
    y_values = append(arange(0, max_y_value, round(max_y_value/15, 1)), max_y_value).round(1).tolist()

    # evaluate companies near the intersections
    best_path = []
    for intersection in companies_intersections:
        evaluation = [(intersection[0] - 0.1) * companies[index]["coefficient"] + companies[index]["constant"] for index in range(count)]
        name = companies[evaluation.index(min(evaluation))]["name"]

        if len(best_path) == 0:
            best_path.append({
                "name": name,
                "start": (0, 0),
                "end": intersection
            })
        elif best_path[len(best_path) - 1]["name"] == name:
            best_path[len(best_path) - 1] = {
                "name": name,
                "start": best_path[len(best_path) - 1]["start"],
                "end": intersection
            }
        else:
            best_path.append({
                "name": name,
                "start": best_path[len(best_path) - 1]["end"],
                "end": intersection
            })
    evaluation = [(best_path[len(best_path) - 1]["end"][0] + 0.1) * companies[index]["coefficient"] + companies[index]["constant"] for index in
                  range(count)]
    best_path.append({
        "name": companies[evaluation.index(min(evaluation))]["name"],
        "start": best_path[len(best_path) - 1]["end"],
        "end": (max_x_value + 1, 0)
    })

    # get x and y values for the best path
    best_path_x = []
    best_path_y = []
    for node in best_path:
        intervals = append(arange(node["start"][0], node["end"][0], round(node["end"][0]/15, 1)), node["end"][0]).round(1).tolist()
        best_path_x += intervals
        tmp = next(company for company in companies if company["name"] == node["name"])
        best_path_y += [tmp["coefficient"] * number + tmp["constant"] for number in intervals]

    # makes the graph
    graph = MultipleLinesGraph("Convenience Graph", "Quantity", "Costs", 15, 15, 20)  # creates a new graph

    for company in companies:
        y = [company["coefficient"] * number + company["constant"] for number in x_values]
        graph.add_line(x_values, y, company["name"])
    graph.add_line(best_path_x, best_path_y, "Convenience")

    graph.show_values_in_x_axis(append(x_values, [intersection[0] for intersection in companies_intersections]).tolist())
    graph.show_values_in_y_axis(append(y_values, [intersection[1] for intersection in companies_intersections]).tolist())

    graph.fill_between_x_axis(best_path_x, best_path_y)

    graph.set_legend("lower right", 20)  # setting up the legend

    for intersection in companies_intersections:
        graph.add_point(intersection[0], intersection[1])

    graph.save_to_file("graph", "png")  # saves the graph to .png (all the others picture formats work as well)

    # assembling all the data gathered
    table_data = {
        "Company": [node["name"] for node in best_path],
        "Start of Convenience Range": [f'{node["start"][0]} items'for node in best_path],
        "End of Convenience Range": map(lambda num: "Infinite Items" if num > max_x_value else f"{num} items", [node["end"][0] for node in best_path])
    }

    # makes a table
    table = OnlyColumnsTable(f"Convenience Table", 20)    # creates a new table
    table.fill(table_data)  # fills the newly created table
    table.format(15, 15)    # formats the table
    table.save_to_file("table", "png")   # saves the table to .png


# starts script only if directly called
if __name__ == "__main__":
    main()
