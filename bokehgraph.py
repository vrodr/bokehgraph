import pandas as pd
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
i = 0

# prepare some data
df = pd.read_csv('data/export.csv', sep=',')
for row in df.iterrows():
    if row[1]['Result Chat'] not in dict_of_tems:
        color = random_color()
        while color in list_of_colors:
            color = random_color()
        list_of_colors.append(color)
        dict_of_tems[row[1]['Result Chat']] = color
    p.circle(float(row[1]['x']), float(row[1]['y']), fill_color=dict_of_tems[row[1]['Result Chat']], fill_alpha=0.6, line_color=None)
    i += 1
    print(i)

# show the results
show(p)

