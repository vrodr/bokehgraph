import numpy as np
import csv
from bokeh.plotting import figure, output_file, show

# output to static HTML file (with CDN resources)
output_file("color_scatter.html", title="color_scatter.py example", mode="cdn")

TOOLS = "crosshair,pan,wheel_zoom,box_zoom,reset,box_select,lasso_select"

# create a new plot with the tools above, and explicit ranges
p = figure(tools=TOOLS, x_range=(-100, 100), y_range=(-100, 100))
list_of_tems = []
# prepare some data
with open('mini.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        if row[4] not in list_of_tems:
            list_of_tems.append(row[4])
    for tem in list_of_tems:
        tem_collor =
    for row in reader:
        p.circle(float(row[1]), float(row[2]), fill_color=color, fill_alpha=0.6, line_color=None)



# show the results
show(p)
