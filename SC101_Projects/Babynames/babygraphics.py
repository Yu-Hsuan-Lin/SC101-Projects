"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    x = (width - GRAPH_MARGIN_SIZE*2)/(len(YEARS))*year_index + GRAPH_MARGIN_SIZE
    return x


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    # horizontal lines
    x1 = GRAPH_MARGIN_SIZE
    x2 = CANVAS_WIDTH - GRAPH_MARGIN_SIZE
    y1 = GRAPH_MARGIN_SIZE
    y2 = CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
    canvas.create_line(x1, y1, x2, y1, width=LINE_WIDTH)
    canvas.create_line(x1, y2, x2, y2, width=LINE_WIDTH)
    # vertical line
    y_v1 = 0
    y_v2 = CANVAS_HEIGHT
    for year_index in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, year_index)
        canvas.create_line(x, y_v1, x, y_v2, width=LINE_WIDTH)
        canvas.create_text(x+TEXT_DX, y2, text=YEARS[year_index], anchor=tkinter.NW)

    #################################


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid
    # Write your code below this line
    # each name
    for lookup_name in lookup_names:
        # create color
        color = lookup_names.index(lookup_name) % 4
        # each year
        for year_index in range(len(YEARS) - 1):
            # create coordinators
            x1 = get_x_coordinate(CANVAS_WIDTH, year_index)
            x2 = get_x_coordinate(CANVAS_WIDTH, year_index + 1)
            y1 = get_y_coordinate_and_rank_text_for_name(year_index, name_data, lookup_name)[0]
            y2 = get_y_coordinate_and_rank_text_for_name(year_index+1, name_data, lookup_name)[0]
            # create line
            canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=COLORS[color])
            # create rank shown on text
            rank_show = get_y_coordinate_and_rank_text_for_name(year_index, name_data, lookup_name)[1]
            # create text
            canvas.create_text(x1 + TEXT_DX, y1, text=lookup_name + ' ' + str(rank_show), fill=COLORS[color],
                               anchor=tkinter.SW)
        # the last text
        last_index = len(YEARS)-1
        x_last = get_x_coordinate(CANVAS_WIDTH, last_index)
        y_last = get_y_coordinate_and_rank_text_for_name(last_index, name_data, lookup_name)[0]
        rank_show = get_y_coordinate_and_rank_text_for_name(last_index, name_data, lookup_name)[1]
        canvas.create_text(x_last + TEXT_DX, y_last, text=lookup_name + ' ' + str(rank_show),
                           fill=COLORS[color], anchor=tkinter.SW)
    #################################


def get_y_coordinate_and_rank_text_for_name(year_index, name_data, lookup_name):
    """
    :param year_index: the given year_index
    :param name_data: dict, Dictionary holding baby name data
    :param lookup_name: the name whose data you want to plot
    :return: this function will return the y_coordinate and the rank text of the name in a given year.
    """
    if str(YEARS[year_index]) in name_data[lookup_name]:
        rank_show = name_data[lookup_name][str(YEARS[year_index])]
        # adjust the ratio to show 1000 on (600-40+20)
        y = int(rank_show)*(CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)//1000+GRAPH_MARGIN_SIZE
    else:
        # if rank > 1000, than the text becomes *
        y = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
        rank_show = '*'
    return y, rank_show


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    """
    Given a name, this program will give out the baby name usage in each year.
    :return:
    """
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
