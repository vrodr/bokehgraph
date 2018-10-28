import numpy as np
import csv
from bokeh.plotting import figure, output_file, show
import random
from concurrent.futures import ThreadPoolExecutor

def random_color():
    r = lambda: random.randint(0,255)
    return ('#%02X%02X%02X' % (r(),r(),r()))



# output to static HTML file (with CDN resources)
output_file("circles.html", title="circles", mode="cdn")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

# create a new plot with the tools above, and explicit ranges
p = figure(tools=TOOLS, x_range=(-100, 100), y_range=(-100, 100))

dict_of_tems = {}
list_of_colors = []

# prepare some data
with open('data/mini.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[4] not in dict_of_tems:
            color = random_color()
            while color in list_of_colors:
                color = random_color()
            list_of_colors.append(color)
            dict_of_tems[row[4]] = color
        p.circle(float(row[1]), float(row[2]), fill_color=dict_of_tems[row[4]], fill_alpha=0.6, line_color=None)




# show the results
show(p)
