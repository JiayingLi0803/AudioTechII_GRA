from bokeh.plotting import curdoc, figure, output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Slider



# Create a data source and a plot
x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 2, 1]
source = ColumnDataSource(data=dict(x=x, y=y))
plot = figure(width=400, height=400)
plot.line('x', 'y', source=source, line_width=2)

# Define a callback function for the slider
def update_data(attrname, old, new):
    # Get the current value of the slider
    a = slider.value
    
    # Update the y values of the data source
    y_new = [y_val + a for y_val in y]
    source.data = dict(x=x, y=y_new)

# Create a slider and attach the callback function
slider = Slider(title="Slider", start=0, end=10, value=0, step=0.1)
slider.on_change('value', update_data)

# Create a layout with the plot and the slider
layout = column(slider, plot)
output_file(filename="custom_filename.html", title="Static HTML file")
save(layout)

# # Generate an HTML file that contains the plot and associated JavaScript callbacks
# curdoc().add_root(layout)
