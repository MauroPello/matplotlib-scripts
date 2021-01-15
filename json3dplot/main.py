import inspect
import json
import os
import sys
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from dataplotting.simple_data_plotting_lib import Plot3D

def main():
    with open('input.json') as f:
        to_plot = json.load(f)

    space = Plot3D(4, 4)

    print(to_plot)
    for item in to_plot:
        print(item)
        if item["type"] == "point":
            space.add3Dpoint(item["coordinates"]["x"], item["coordinates"]["y"], item["coordinates"]["z"])
            pass
        elif item["type"] == "plane":
            space.add3Dplane()
            pass
        else:
            print("The entered json file was wrongly written!")
            exit(1)

    space.save_to_file("output", "png")


# starts script only if directly called
if __name__ == "__main__":
    main()
