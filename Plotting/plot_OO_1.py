#!/usr/bin/env python
# Object-oriented template, as opposed to state model of pyplot
# Each object can be passed into functions, useful for related analysis
#   over same datasets.

from matplotlib import figure
from matplotlib.backends.backend_agg import (
FigureCanvasAgg as FigureCanvas)

# Figure is the conceptual container
fig = figure.Figure()

# Canvas is what gets rendered to; color set by "facecolor" option in print_figure
# Area around plots.
canvas = FigureCanvas(fig)

# Axes are what scientists typically consider as "plot"
#   You always want to make things subplots
#   Will have axes on top of the canvas.
ax1 = fig.add_subplot(2,2,1)

# Modify properties
ax1.xaxis.grid(True)  # Add vertical lines
ax1.set_xlabel('text')
ax1.set_xlim(-1., 1.)

# Markers: can make custom, or choose from bunch. markerstyle='x', almost any alphanumeric x defined
markerlist = matplotlib.markers.MarkerStyle.markers.keys()
print mlist

# Scatter points. Colors can be anything in HTML or otherwise; can have transparency as well
# Marker size s can be an array, so size changes with x array
ax1.scatter(0.5, 0.5, marker='0', s=500, edgecolor='b', color='pink', alpha=0.5)

# Line styles -- solid, -. dot-dash, - dashed, : dotted; color, width, etc.

# 3D plot example
ax2 = fig.add_subplot(2,2,2, projection='3d')
ax2.set_zlim((-1,1,))

# Annotations: axis.annotate(marker, xy, xytext, bbox=dict(boxstyle='round',fc='w',arrowprops=dict(arrowstyle='->'))
#  bbox is dictionary of keyword properties. Compound object properties can be defined with dictionaries (e.g., arrowprops)

# Spines--customize borderlines of plot
ax2.spines('top').set_linewidth(5)
ax2.spines('right').set_color('b')
ax2.spines('right').set_color('none')  # Make colorless/delete

# Data series

# Check and get rid of overlaps in figure
fig.tight_layout()

# Like pyplot's savefig.
canvas.print_figure('canvas.png', facecolor='lightgray')

