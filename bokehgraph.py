import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
import random


# random color for themes
def random_color():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

TOOLS = "crosshair, pan, box_zoom, reset, hover"
TOOLTIPS = [("index", "$index"),
            ("(x, y)", "($x, $y)"),
            ("desc", "@Message")]

output_file("circles.html", title="circles", mode="cdn")
p = figure(tools=TOOLS, x_range=(-40, 40), y_range=(-40, 40), tooltips=TOOLTIPS)

# prepare data
df = pd.read_csv('data/export.csv', sep=',')
dict_of_themes = {}
list_of_colors = []
for ind, row in df.iterrows():
    if row['Result Chat'] not in dict_of_themes:
        color = random_color()
        while color in list_of_colors:
            color = random_color()
        list_of_colors.append(color)
        dict_of_themes[row['Result Chat']] = color
df['color'] = df['Result Chat']
df = df.replace({'color': dict_of_themes})

source = ColumnDataSource(df)

#build dots
p.circle('x', 'y', fill_color='color', line_color='color', source=source)

# show the results
show(p)
