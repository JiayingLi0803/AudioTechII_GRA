from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Select
import numpy as np

# Create the figure for the plot
plot = figure(width=600, height=400)

# Define the x-axis range for the plot
x = np.linspace(-5, 5, 100)

# Define the initial function to be displayed
y = np.zeros(len(x))

x = x.tolist()
y = y.tolist()

# Create a data source for the plot
source = ColumnDataSource(data=dict(x=x, y=y))
x_fig = figure(title='Input Signal', width=350, height=300, x_range=(-6, 6), y_range=(-1, 4))
x_fig.line('x', 'y', source=source)

# Define the selector widget and its options
options = ['Unit Step', 'Dirac Impulse', 'Exponential']
selector = Select(title='Function:', value=options[0], options=options)

# Define the JavaScript callback for the selector
callback = CustomJS(args=dict(source=source, selector=selector), code="""
    let data = source.data;
    const func = selector.value;
    const x = data["x"];
    let y = data["y"];
    
    if (func === 'Unit Step') {
        y = x.map(val => val >= 0 ? 1 : 0);
    } else if (func === 'Dirac Impulse') {
        y = Array.from({length: x.length}, (_, i) => i === x.length / 2 ? 1 : 0);
    } else if (func === 'Exponential') {
        y = x.map(val => Math.exp(val));
        console.log(y);
    }
    
    
    source.change.emit();
    console.log(data["y"]);
""")

# Attach the callback to the selector
selector.js_on_change('value', callback)

# Create a layout with the plot and the selector
layout = column(x_fig, selector)

# Display the plot and the selector
show(layout)
