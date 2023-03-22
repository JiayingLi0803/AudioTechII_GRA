from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, output_file, show, curdoc
import numpy as np

# Define the exponential function
def exp_func(t, a):
    return np.exp(-a * t) * (t >= 0)

# Define the unit step function
def unit_func(t):
    return 1.0 * (t >= 0)

# Define the convolution function
def convolve(signal, impulse, time):
    dt = time[1] - time[0]
    result = np.zeros_like(time)
    for i in range(len(time)):
        # result[i] = np.sum(signal[:i+1] * impulse[i::-1]) * dt
        result[i] = np.sum(signal[:i+1] * impulse[i::-1][::-1]) * dt
    return result

# Define the impulse response flip signal
def flip(signal, time, timeshift):
    dt = time[1] - time[0]
    shift = int((timeshift+2)/dt)
    signal_remove = signal[signal!=0]
    result = signal[shift::-1]
    result = np.pad(result, (0, 1000-len(result)), "constant")
    return result

def update_data(attrname, old, new):
    # Get the current value of the slider: current time
    a = shift_slider.value
    pts = int((a+1)/(t[1]-t[0]))
    # Update the values of the data source: y2_source
    hinv_new = flip(h, t, a)
    h_source.data = dict(x=t, y1=x, y2=hinv_new)

    # Update the values of the data source: y2_source
    x2_new = t[:pts]
    y2_new = y[:pts]
    y2_source.data = dict(x=x2_new, y=y2_new)
    
# Generate input and impulse response signals
# Set up the time axis
t = np.linspace(-1, 5, 1000)
# Set up the functions to convolve
x = unit_func(t)
h = exp_func(t, 1)
hinv = flip(h, t, 0)
y = convolve(x, h, t)
# Set up Bokeh data sources for the signals
x_source = ColumnDataSource(data=dict(x=t, y1=x, y2=h))
h_source = ColumnDataSource(data=dict(x=t, y1=x, y2=hinv))
y_source = ColumnDataSource(data=dict(x=t, y=y))
y2_source = ColumnDataSource(data=dict(x=t[:1], y=y[:1]))
# Set up Bokeh figures for the signals
x_fig = figure(title='Input Signal', width=500, height=200, x_range=(-1, 4.01), y_range=(-1, 2))
# x_fig.varea(x='x', y1='y1', y2='y2', source=x_source, fill_alpha=0.5)
x_fig.line('x', 'y1', source=x_source, line_width=2, line_color='blue')
x_fig.line('x', 'y2', source=x_source, line_width=2, line_color='red', line_dash="dotted")
h_fig = figure(title='Impulse Response', width=500, height=200, x_range=(-1, 4.01), y_range=(-1, 2))
h_fig.line('x', 'y1', source=h_source, line_width=2, line_color='blue')
h_fig.line('x', 'y2', source=h_source, line_width=2, line_color='red', line_alpha=0.6, line_dash="dotted")
y_fig = figure(title='Output Signal', width=500, height=200, x_range=(-1, 4.01), y_range=(-1, 2))
y_fig.line('x', 'y', source=y_source, line_width=2, line_color='green', line_alpha=0.2)
y_fig.line('x', 'y', source=y2_source, line_width=2, line_color='green')

shift_slider = Slider(title='t', value=-1, start=-1, end=4, step=0.006)
shift_slider.on_change('value', update_data)

# Combine the figures and sliders into a Bokeh layout
layout = column(x_fig, h_fig, y_fig, shift_slider)

# Display the Bokeh layout in a new browser window
output_file('convolution.html')
# show(layout)
curdoc().add_root(layout)

# bokeh serve --show --port 5001 convolution.py