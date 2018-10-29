import pandas as pd
from bokeh.plotting import figure, output_file, show
import random
import numpy as np
from bokeh.models import Legend

# random color for themes
def random_color():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

TOOLS = "crosshair, pan, box_zoom, reset, hover"
TOOLTIPS = [("index", "$index"),
            ("(x, y)", "($x, $y)"),
            ("desc", "@Message")]

output_file("circles.html", title="circles", mode="cdn")
p = figure(tools=TOOLS, x_range=(-40, 40), y_range=(-40, 40), tooltips=TOOLTIPS,
           plot_width=850, plot_height=850)


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

# make noise
mu, sigma = 0, 0.1
df['x'] = df['x'].apply(lambda x: x + np.random.normal(mu, sigma))
df['y'] = df['y'].apply(lambda x: x + np.random.normal(mu, sigma))

list_of_themes = list(dict_of_themes.keys())
list_of_themes.sort()

# build dots
i = 10
for theme in list_of_themes:
    temp = df[df['Result Chat'] == theme]
    r = p.circle(temp['x'].values, temp['y'].values,
                 fill_color=temp['color'].values, line_color=temp['color'].values,
                 legend=theme)



p.legend.click_policy = "hide"



'''legend = Legend(location=(100, 100))
p.add_layout(legend, 'left')
 legend = Legend(items=[(theme, [r])], location=(i, i), orientation="vertical")
    #p.add_layout(legend, 'below')
    i -= 10
p.legend.orientation = "horizontal'''
# show the results
show(p)
