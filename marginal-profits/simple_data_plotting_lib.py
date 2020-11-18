import matplotlib.pyplot as plt
import pandas as pd


# very simple line graph with the possibility of adding multiple lines and having a legend
class MultipleLinesGraph:
    def __init__(self, title, x_label, y_label, width, height, font_size):
        self.fig, self.ax = plt.subplots(figsize=(width, height))   # graph subplot (space where we will be working)
        self.ax.set_title(title, fontsize=font_size * 1.3, fontweight='bold')   # setting the graph title

        self.ax.set_xlabel(x_label, fontsize=font_size, fontweight='bold')      # setting the label for the x axis
        self.ax.set_ylabel(y_label, fontsize=font_size, fontweight='bold')      # setting the label for the y axis

        self.ax.set_xlim(left=0)            # making the x axis start from x=0
        self.ax.set_ylim(bottom=0)          # making the y axis start from y=0

        self.ax.grid()          # enables the grid to allow better viewing of values in the graph

    # adds a line with a label assigned to it
    def add_line(self, x_arr, y_arr, label):
        self.ax.plot(x_arr, y_arr, label=label, linewidth=2, marker="o")

    # sets the legend up with the existing lines
    def set_legend(self, location, font_size):
        self.ax.legend(loc=location, handles=self.ax.get_lines(), prop={'size': font_size})

    # makes sure that the values in arr are shown on the x axis (better readability)
    def show_values_in_x_axis(self, arr):
        self.ax.set_xticks(arr)

    # makes sure that the values in arr are shown on the y axis (better readability)
    def show_values_in_y_axis(self, arr):
        self.ax.set_yticks(arr)

    # saves the graph to a file with DPI=200 and no extra white space ('tight')
    def save_to_file(self, file_name, file_format):
        self.fig.savefig(f'{file_name}.{file_format}', format=file_format, dpi=200, bbox_inches='tight')


# very simple table with only columns already formatted for nice readability
class OnlyColumnsTable:
    def __init__(self, title, title_font_size):
        self.fig, self.ax = plt.subplots()          # table subplot (space where we will be working)
        self.ax.set_title(title, fontsize=title_font_size, loc="center", fontweight='bold') # setting the table title

        # removing the axis (useless in this case because we are rendering a table, not a graph)
        self.ax.axis('off')

        # initializing the table variable to use it across different use cases
        self.table = None

    # fills the table with data
    def fill(self, data):
        data_frame = pd.DataFrame(data)     # using pandas to correctly render data into the table

        column_colors = ["#d9d9d9" for i in range(data_frame.shape[1])]         # list of colors specific to each column
        cell_colors = [["#f2f2f2" for i in range(data_frame.shape[1])] for i in range(data_frame.shape[0])]         # list of colors specific to each cell

        # creating the table by using the pandas data frame and the two lists of colors
        self.table = self.ax.table(cellText=data_frame.values, colLabels=data_frame.columns, loc="upper center",
                                   cellLoc='center', cellColours=cell_colors, colColours=column_colors)

    def format(self, column_font_size, text_font_size):
        self.table.auto_set_font_size(False)        # disables auto_set_font_size
        self.table.set_fontsize(text_font_size)     # sets the custom fontsize
        self.table.scale(2, 2)                      # scales up the table to make it bigger

        # cycling through every cell to change the fontweight and fontsize of the text inside the column cells
        col_names = []
        for (row, col), cell in self.table.get_celld().items():
            if (row == 0) or (col == -1):
                col_names.append(cell.get_text().get_text())
                cell.set_text_props(fontsize=column_font_size, fontweight='bold')

        # set auto column width
        self.table.auto_set_column_width(col=list(range(len(col_names))))

    # saves the graph to a file with DPI=200 and no extra white space ('tight')
    def save_to_file(self, file_name, file_format):
        self.fig.savefig(f'{file_name}.{file_format}', format=file_format, dpi=200, bbox_inches='tight')
