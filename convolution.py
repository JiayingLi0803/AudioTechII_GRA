from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider
from bokeh.plotting import figure, output_file, show, curdoc, save
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
y2 = convolve(x, h, t)
for i in range(len(y2)):
    if i>=1:
        y2[i] = np.inf
x = x.tolist()
h = h.tolist()
hinv = hinv.tolist()
y = y.tolist()
y2 = y2.tolist()
# Set up Bokeh data sources for the signals
x_source = ColumnDataSource(data=dict(x=t, y1=x, y2=h))
h_source = ColumnDataSource(data=dict(x=t, y1=x, y2=hinv))
y_source = ColumnDataSource(data=dict(x=t, y=y))
y2_source = ColumnDataSource(data=dict(x=t, y=y2))
# Set up Bokeh figures for the signals
x_fig = figure(title='Input Signal', width=350, height=300, x_range=(-1, 4.01), y_range=(-1, 2))
# x_fig.varea(x='x', y1='y1', y2='y2', source=x_source, fill_alpha=0.5)
x_fig.line('x', 'y1', source=x_source, line_width=2, line_color='blue', legend_label="x(t)")
x_fig.line('x', 'y2', source=x_source, line_width=2, line_color='red', line_dash="dotted", legend_label="h(t)")
x_fig.legend.location = "top_left"
h_fig = figure(title='Shift', width=350, height=300, x_range=(-1, 4.01), y_range=(-1, 2))
h_fig.line('x', 'y1', source=h_source, line_width=2, line_color='blue', legend_label="x(t-t')")
h_fig.line('x', 'y2', source=h_source, line_width=2, line_color='red', line_dash="dotted", legend_label="h(t-t')")
h_fig.legend.location = "top_left"
y_fig = figure(title='Output Signal', width=350, height=300, x_range=(-1, 4.01), y_range=(-1, 2))
y_fig.line('x', 'y', source=y_source, line_width=2, line_color='green', line_alpha=0.2)
y_fig.line('x', 'y', source=y2_source, line_width=2, line_color='green', legend_label="x(t)*h(t)")
y_fig.legend.location = "top_left"

shift_slider = Slider(title='t', value=-1, start=-1, end=4, step=0.006, width=340, height=300)
# shift_slider.on_change('value', update_data)


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

callback = CustomJS(args=dict(x_source=x_source, h_source=h_source, y_source=y_source, y2_source=y2_source, shiftval=shift_slider),
                    code="""
    const xdata = x_source.data;
    const hdata = h_source.data;
    const ydata = y_source.data;
    const y2data = y2_source.data;
    const timeshift = shiftval.value;
    const t = xdata["x"];
    const x = xdata["y1"];
    const h = xdata["y2"];
    const hinv = hdata["y2"];
    const y = ydata["y"];
    const t2 = y2data["x"];
    const y2 = y2data["y"];


    const dt = t[1]-t[0];
    
    const shift = Math.round((timeshift+2)/dt);
    const result = h.slice(0, shift + 1).reverse(); 
    const padlen = 1000 - result.length;
    for (let i = 0; i < padlen ; i++) {
        result.push(0);
    }

    for (let i = 0; i < result.length ; i++) {
        hinv[i] = result[i];
    }

    const pts = Math.round((timeshift+1)/dt);
    for (let i = 0; i < pts ; i++) {
        y2[i] = y[i];
    }
    console.log(y2);

    h_source.change.emit();
    y2_source.change.emit();
""")

shift_slider.js_on_change('value', callback)

# Combine the figures and sliders into a Bokeh layout
layout = gridplot([[row(x_fig, h_fig)], [row(shift_slider, y_fig)]])

show(layout)
# bokeh serve --show --port 5001 convolution.py