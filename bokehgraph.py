import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from sklearn.cluster import DBSCAN
from scipy.spatial import ConvexHull
from sklearn.metrics.cluster import adjusted_rand_score
from bokeh.models import ColumnDataSource


np.random.seed(5)

# Random color for themes.
def random_color():
    r = lambda: np.random.randint(0, 255)
    return '#%02X%02X%02X' % (r(), r(), r())


def draw_graph(file, noise=False):
    '''
    This function create file circles.html with help of bokeh module. First of
    all, dots are drawn by topics. Secondarily, clusters of coordinates are
    superimposed on the points.

    :param file: str or PandasDataFrame
    This parameter is responsible for path to the file with the table scv. But
    you can straight away give PandasDataFrame.
    :param noise: True or False
    This parameter is responsible for imposing noise on the coordinates of points.
    :return: circles.html

    Examples
    --------
    draw_graph('data/export.csv')

    '''

    # Constants for tooltips.
    TOOLS = "wheel_zoom, pan, reset, hover"
    TOOLTIPS = [("index", "$index"),
                ("(x, y)", "($x, $y)"),
                ("desc", "@Message"), ]

    # Make file and main graph.
    output_file("circles.html", title="circles", mode="cdn")
    p = figure(tools=TOOLS, x_range=(-40, 40), y_range=(-40, 40),
               tooltips=TOOLTIPS, plot_width=850, plot_height=850)

    # Prepare data.
    if type(file) is str:
        df = pd.read_csv(file, sep=',')
    else:
        df = file
    data = df[['x', 'y']].values
    clustering = DBSCAN(eps=0.1).fit(data)
    df['cluster'] = [str(element) for element in clustering.labels_]

    print('Adjusted Rand index: ', adjusted_rand_score(df['Result Chat'].values, df['cluster'].values))

    # Add 2 columns in DataFrame: color_theme and color_cluster.
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

    # Make noise.
    if noise:
        mu, sigma = 0, 0.1
        df['x'] = df['x'].apply(lambda x: x + np.random.normal(mu, sigma))
        df['y'] = df['y'].apply(lambda x: x + np.random.normal(mu, sigma))

    # Build themes.
    list_of_themes = list(dict_of_themes.keys())
    list_of_themes.sort()
    for theme in list_of_themes:
        temp = df[df['Result Chat'] == theme]
        source = ColumnDataSource(temp)
        p.circle('x', 'y', color='color_theme', legend=theme, source=source)
    p.legend.click_policy = "hide"

    # Build clusters.
    list_of_clusters = list(dict_of_clusters.keys())
    list_of_clusters.sort()
    for cluster in list_of_clusters[1:]:
        temp = df[df['cluster'] == cluster]
        hull = ConvexHull(temp[['x', 'y']].values)
        con = temp.iloc[hull.vertices]
        p.patch(con['x'].values, con['y'].values,
                color=dict_of_clusters[cluster], alpha=0.5, line_width=2)

    # Show the results.
    show(p)
