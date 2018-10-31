import random
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull

# random color for themes
def random_color():
    r = lambda: random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())

TOOLS = "wheel_zoom, pan, box_zoom, reset, hover, zoom_in, zoom_out"
TOOLTIPS = [("index", "$index"),
            ("(x, y)", "($x, $y)"),
            ("desc", "@Message")]

output_file("circles.html", title="circles", mode="cdn")
p = figure(tools=TOOLS, x_range=(-40, 40), y_range=(-40, 40),
           tooltips=TOOLTIPS, plot_width=850, plot_height=850)

# prepare data
df = pd.read_csv('data/export.csv', sep=',')
data = df[['x', 'y']].values
clustering = DBSCAN(eps=0.1).fit(data)
df['cluster'] = [str(element) for element in clustering.labels_]

dict_of_themes = {}
list_of_color = []
dict_of_clusters = {'-1': '#000000'}

for ind, row in df.iterrows():
    if row['Result Chat'] not in dict_of_themes:
        color = random_color()
        while color in list_of_color:
            color = random_color()
        list_of_color.append(color)
        dict_of_themes[row['Result Chat']] = color
    if row['cluster'] not in dict_of_clusters:
        color = random_color()
        while color in list_of_color:
            color = random_color()
        list_of_color.append(color)
        dict_of_clusters[row['cluster']] = color

df['color_theme'] = df['Result Chat']
df = df.replace({'color_theme': dict_of_themes})
df['color_cluster'] = df['cluster']
df = df.replace({'color_cluster': dict_of_clusters})

# make noise
mu, sigma = 0, 0.1
df['x'] = df['x'].apply(lambda x: x + np.random.normal(mu, sigma))
df['y'] = df['y'].apply(lambda x: x + np.random.normal(mu, sigma))

# build dots themes
list_of_themes = list(dict_of_themes.keys())
list_of_themes.sort()
for theme in list_of_themes:
    temp = df[df['Result Chat'] == theme]
    r = p.circle(temp['x'].values, temp['y'].values,
                 color=temp['color_theme'].values,
                 legend=theme)

# build clusters
list_of_clusters = list(dict_of_clusters.keys())
list_of_clusters.sort()
for cluster in list_of_clusters[1:]:
    temp = df[df['cluster'] == cluster]
    hull = ConvexHull(temp[['x', 'y']].values)
    con = temp.iloc[hull.vertices]
    r = p.patch(con['x'].values, con['y'].values,
                color=dict_of_clusters[cluster], alpha=0.5,
                line_width=2)

p.legend.click_policy = "hide"

# show the results
show(p)
