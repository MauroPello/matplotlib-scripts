import sys
import os
import inspect
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.realpath(os.path.dirname(inspect.getfile(inspect.currentframe())))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
from data_plotting_lib.simple_data_plotting_lib import OnlyColumnsTable, MultipleLinesGraph
