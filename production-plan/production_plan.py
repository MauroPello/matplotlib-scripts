import sys
import os
import inspect
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import OnlyColumnsTable, MultipleLinesGraph
from datetime import datetime,  timedelta


def main():

    order = {
        "date": None,
        "quantity": None,
        "product": {"name": str(input("Enter the name of the item: ")), "time_to_manufacture": -1}
    }

    while True:
        try:
            order["product"]["time_to_manufacture"] = int(input(f"Enter the amount of minutes needed to manufacture a {order['product']['name']}: "))
            if order["product"]["time_to_manufacture"] <= 0:
                raise ValueError
            else:
                break
        except ValueError:
            print("The amount of minutes needed to manufacture the item has to be a positive integer!")

    while True:
        try:
            order["date"] = datetime.strptime(input("Enter the order date (DD/MM/YYYY): "), "%d/%m/%Y")
            break
        except ValueError:
            print("The date was not correctly formatted (DD/MM/YYYY)!")

    while True:
        try:
            order["quantity"] = int(input(f"Enter the number of {order['product']['name']} to manufacture: "))
            if order["quantity"] <= 0:
                raise ValueError
            else:
                break
        except ValueError:
            print("The number of items ordered has to be a positive integer!")

    while True:
        try:
            work_hours = int(input(f"Enter the amount of work hours for a day: "))
            if work_hours <= 0 or work_hours > 24:
                raise ValueError
            else:
                break
        except ValueError:
            print("The amount of work hours for a day has to be a positive integer between 0 and 24!")

    table_data = {
        "Date": [],
        "Weekday": [],
        "Daily Items": [],
        "Total Items": []
    }

    days = 0
    products_manufactured = 0
    while True:
        date = order["date"] + timedelta(days=days)

        todays_products = 0

        # firms usually are closed on Saturdays and Sundays
        if date.isoweekday() != 6 and date.isoweekday() != 7:
            todays_products = work_hours * 60 / order["product"]["time_to_manufacture"]
            products_manufactured += todays_products

        table_data["Date"].append(date.strftime('%d/%m/%Y'))
        table_data["Weekday"].append(date.strftime('%A'))
        table_data["Daily Items"].append(f"{todays_products} {order['product']['name']}")
        table_data["Total Items"].append(f"{products_manufactured} {order['product']['name']}")

        if products_manufactured >= order["quantity"]:
            break

        days += 1

    # makes a table
    table = OnlyColumnsTable(f"Production Plan Table ({order['quantity']} {order['product']['name']}, {work_hours} hrs/day)", 20)    # creates a new table
    table.fill(table_data)  # fills the newly created table
    table.format(15, 15)    # formats the table
    table.save_to_file("table", "png")   # saves the table to .png


# starts script only if directly called
if __name__ == "__main__":
    main()
