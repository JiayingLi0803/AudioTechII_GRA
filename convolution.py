from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, output_file, show
import numpy as np

# Generate input and impulse response signals
x = np.linspace(0, 1, 1000)
h = np.exp(-100*(x-0.5)**2)
y = np.convolve(x, h, mode='same')

# Set up Bokeh data sources for the signals
x_source = ColumnDataSource(data=dict(x=x, y=x))
h_source = ColumnDataSource(data=dict(x=x, y=h))
y_source = ColumnDataSource(data=dict(x=x, y=y))

# Set up Bokeh figures for the signals
x_fig = figure(title='Input Signal', width=800, height=300, x_range=(0, 1), y_range=(-1, 1))
x_fig.line('x', 'y', source=x_source, line_width=2, line_color='blue')
h_fig = figure(title='Impulse Response', width=800, height=300, x_range=(0, 1), y_range=(-1, 1))
h_fig.line('x', 'y', source=h_source, line_width=2, line_color='green')
y_fig = figure(title='Output Signal', width=800, height=300, x_range=(0, 1), y_range=(-1, 1))
y_fig.line('x', 'y', source=y_source, line_width=2, line_color='red')

# Set up Bokeh sliders for the convolution parameters
center_slider = Slider(title='Center', value=0.5, start=0, end=1, step=0.01)
width_slider = Slider(title='Width', value=0.1, start=0, end=0.5, step=0.01)

# Set up Bokeh JavaScript callback for updating the signals
callback = CustomJS(args=dict(x_source=x_source, h_source=h_source, y_source=y_source,
                              center_slider=center_slider, width_slider=width_slider), code='''
    const x = x_source.data['y'];
    const h = h_source.data['y'];
    const y = y_source.data['y'];
    const center = center_slider.value;
    const width = width_slider.value;
    for (let i = 0; i < x.length; i++) {
        h[i] = Math.exp(-100*(x[i]-center)**2/width**2);
    }
    for (let i = 0; i < y.length; i++) {
        let sum = 0;
        for (let j = 0; j < h.length; j++) {
            if (i-j >= 0 && i-j < x.length) {
                sum += x[i-j] * h[j];
            }
        }
        y[i] = sum;
    }
    x_source.change.emit();
    h_source.change.emit();
    y_source.change.emit();
''')

# Connect the sliders to the JavaScript callback
center_slider.js_on_change('value', callback)
width_slider.js_on_change('value', callback)

# Combine the figures and sliders into a Bokeh layout
layout = column(x_fig, h_fig, y_fig, center_slider, width_slider)

# Display the Bokeh layout in a new browser window
output_file('convolution.html')
show(layout)
