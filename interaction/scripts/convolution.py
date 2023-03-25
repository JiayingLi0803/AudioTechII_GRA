from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider, Select
from bokeh.plotting import figure, output_file, show, curdoc, save
import numpy as np

# Define the exponential function
def exp_func(t, a):
    return np.exp(-a * t) * (t >= 0)

# Define the unit step function
def unit_func(t):
    return 1.0 * (t >= 0)

# Define the dirace impulse
def dirac_func(t):
    dt = t[1] - t[0]
    dirc = np.zeros_like(t)
    dirc[166] = 1/dt
    return dirc

# Define the convolution function
# def convolve(signal, impulse, time):
#     dt = time[1] - time[0]
#     result = np.zeros_like(time)
#     for i in range(len(time)):
#         # result[i] = np.sum(signal[:i+1] * impulse[i::-1]) * dt
#         result[i] = np.sum(signal[:i+1] * impulse[i::-1][::-1]) * dt
#     return result
def convolve(signal, impulse, time):
    dt = time[1] - time[0]
    result = np.convolve(signal, impulse, "full")
    return result[167:1167] * dt

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
# x func
x_unit = unit_func(t)
x_dirc = dirac_func(t)
x_exp = exp_func(t, 1)
# h func
h_unit = unit_func(t)
h_dirc = dirac_func(t)
h_exp = exp_func(t, 1)
# # hinv func
# hinv_unit = flip(h_unit, t, 0)
# hinv_dirc = flip(h_dirc, t, 0)
# hinv_dirc = flip(h_exp, t, 0)
# # y func
y_unit_unit = convolve(x_unit, h_unit, t)
y_unit_dirc = convolve(x_unit, h_dirc, t)
y_unit_exp = convolve(x_unit, h_exp, t)
y_dirc_unit = convolve(x_dirc, h_unit, t)
y_dirc_dirc = convolve(x_dirc, h_dirc, t)
y_dirc_exp = convolve(x_dirc, h_exp, t)
y_exp_unit = convolve(x_exp, h_unit, t)
y_exp_dirc = convolve(x_exp, h_dirc, t)
y_exp_exp = convolve(x_exp, h_exp, t)
# # y2 func
# y2_unit_unit = convolve(x_unit, h_unit, t)
# y2_unit_dirc = convolve(x_unit, h_dirc, t)
# y2_unit_exp = convolve(x_unit, h_exp, t)
# y2_dirc_unit = convolve(x_dirc, h_unit, t)
# y2_dirc_dirc = convolve(x_dirc, h_dirc, t)
# y2_dirc_exp = convolve(x_dirc, h_exp, t)
# y2_exp_unit = convolve(x_exp, h_unit, t)
# y2_exp_dirc = convolve(x_exp, h_dirc, t)
# y2_exp_exp = convolve(x_exp, h_exp, t)

for i in range(len(y2)):
    if i>=1:
        y2[i] = np.inf
        # y2_unit_unit[i] = np.inf
        # y2_unit_dirc[i] = np.inf
        # y2_unit_exp[i] = np.inf
        # y2_dirc_unit[i] = np.inf
        # y2_dirc_dirc[i] = np.inf
        # y2_dirc_dirc[i] = np.inf
        # y2_exp_unit[i] = np.inf
        # y2_exp_dirc[i] = np.inf
        # y2_exp_exp[i] = np.inf

# Transfer to list
x = x.tolist()
h = h.tolist()
hinv = hinv.tolist()
y = y.tolist()
y2 = y2.tolist()
# x list
x_unit = x_unit.tolist()
x_dirc = x_dirc.tolist()
x_exp = x_exp.tolist()
# h list
h_unit = h_unit.tolist()
h_dirc = h_dirc.tolist()
h_exp = h_exp.tolist()
# # hinv list
# hinv_unit = hinv_unit.tolist()
# hinv_dirc = hinv_dirc.tolist()
# hinv_exp = hinv_exp.tolist()
# y list
y_unit_unit = y_unit_unit.tolist()
y_unit_dirc = y_unit_dirc.tolist()
y_unit_exp = y_unit_exp.tolist()
y_dirc_unit = y_dirc_unit.tolist()
y_dirc_dirc = y_dirc_dirc.tolist()
y_dirc_exp = y_dirc_exp.tolist()
y_exp_unit = y_exp_unit.tolist()
y_exp_dirc = y_exp_dirc.tolist()
y_exp_exp = y_exp_exp.tolist()
# # y2 list
# y2_unit_unit = y2_unit_unit.tolist()
# y2_unit_dirc = y2_unit_dirc.tolist()
# y2_unit_exp = y2_unit_exp.tolist()
# y2_dirc_unit = y2_dirc_unit.tolist()
# y2_dirc_dirc = y2_dirc_dirc.tolist()
# y2_dirc_exp = y2_dirc_exp.tolist()
# y2_exp_unit = y2_exp_unit.tolist()
# y2_exp_dirc = y2_exp_dirc.tolist()
# y2_exp_exp = y_2exp_exp.tolist()

# Set up Bokeh data sources for the signals
x_source = ColumnDataSource(data=dict(x=t, y1=x, y2=h))
h_source = ColumnDataSource(data=dict(x=t, y1=x, y2=hinv))
y_source = ColumnDataSource(data=dict(x=t, y=y))
y2_source = ColumnDataSource(data=dict(x=t, y=y2))
conv_source = ColumnDataSource(data=dict(y_unit_unit = y_unit_unit, 
                                         y_unit_dirc = y_unit_dirc, 
                                         y_unit_exp = y_unit_exp, 
                                         y_dirc_unit = y_dirc_unit,
                                         y_dirc_dirc = y_dirc_dirc,
                                         y_dirc_exp = y_dirc_exp,
                                         y_exp_unit = y_exp_unit,
                                         y_exp_dirc = y_exp_dirc,
                                         y_exp_exp = y_exp_exp))

# Set up Bokeh figures for the signals
x_fig = figure(title='Input Signal', width=350, height=300, x_range=(-1, 4.01), y_range=(-1, 4))
# x_fig.varea(x='x', y1='y1', y2='y2', source=x_source, fill_alpha=0.5)
x_fig.line('x', 'y1', source=x_source, line_width=2, line_color='blue', legend_label="x(t)")
x_fig.line('x', 'y2', source=x_source, line_width=2, line_color='red', line_dash="dotted", legend_label="h(t)")
x_fig.legend.location = "top_left"
h_fig = figure(title='Shift', width=350, height=300, x_range=(-1, 4.01), y_range=(-1, 4))
h_fig.line('x', 'y1', source=h_source, line_width=2, line_color='blue', legend_label="x(t')")
h_fig.line('x', 'y2', source=h_source, line_width=2, line_color='red', line_dash="dotted", legend_label="h(t-t')")
h_fig.varea(x='x', y1='y1', y2='y2', source=h_source, fill_alpha=0.2)
h_fig.legend.location = "top_left"
y_fig = figure(title='Output Signal', width=350, height=300, x_range=(-1, 4.01), y_range=(-1, 4))
y_fig.line('x', 'y', source=y_source, line_width=2, line_color='green', line_alpha=0.2)
y_fig.line('x', 'y', source=y2_source, line_width=2, line_color='green', legend_label="x(t)*h(t)")
y_fig.legend.location = "top_left"

# Define time shift slider
shift_slider = Slider(title='t', value=0, start=-1, end=4, step=0.006, width=340, height=300)
# shift_slider.on_change('value', update_data)

# # Define the selector widget and its options
options = ['Unit Step', 'Dirac Impulse', 'Exponential']
x_selector = Select(title='input signal:', value=options[0], options=options)
h_selector = Select(title='impulse response:', value=options[2], options=options)


# def update_data(attrname, old, new):
#     # Get the current value of the slider: current time
#     a = shift_slider.value
#     pts = int((a+1)/(t[1]-t[0]))
#     # Update the values of the data source: y2_source
#     hinv_new = flip(h, t, a)
#     h_source.data = dict(x=t, y1=x, y2=hinv_new)

#     # Update the values of the data source: y2_source
#     x2_new = t[:pts]
#     y2_new = y[:pts]
#     y2_source.data = dict(x=x2_new, y=y2_new)

callback = CustomJS(args=dict(x_source=x_source, 
                              h_source=h_source, 
                              y_source=y_source, 
                              y2_source=y2_source,
                              conv_source=conv_source,
                              shiftval=shift_slider,
                              x_selector=x_selector,
                              h_selector=h_selector),
                    code="""
    const xdata = x_source.data;
    const hdata = h_source.data;
    const ydata = y_source.data;
    const y2data = y2_source.data;
    const convdata = conv_source.data;
    const timeshift = shiftval.value;
    const x_func = x_selector.value;
    const h_func = h_selector.value;
    const t = xdata["x"];
    const x = xdata["y1"];
    const h = xdata["y2"];
    const x2 = hdata["y1"]
    const hinv = hdata["y2"];
    const y = ydata["y"];
    const t2 = y2data["x"];
    const y2 = y2data["y"];
    let convy = convdata["y_unit_exp"];

    if (x_func == "Unit Step"){
        if (h_func == "Unit Step"){
            convy = convdata["y_unit_unit"];
        } else if (h_func == "Dirac Impulse"){
            convy = convdata["y_unit_dirc"];
        }else if (h_func == "Exponential"){
            convy = convdata["y_unit_exp"];
        }
    } else if (x_func == "Dirac Impulse"){
        if (h_func == "Unit Step"){
            convy = convdata["y_dirc_unit"];
        } else if (h_func == "Dirac Impulse"){
            convy = convdata["y_dirc_dirc"];
        }else if (h_func == "Exponential"){
            convy = convdata["y_dirc_exp"];
        }
    } else if (x_func == "Exponential"){
        if (h_func == "Unit Step"){
            convy = convdata["y_exp_unit"];
        } else if (h_func == "Dirac Impulse"){
            convy = convdata["y_exp_dirc"];
        }else if (h_func == "Exponential"){
            convy = convdata["y_exp_exp"];
        }
    }
    
    const dt = t[1]-t[0];

    if (x_func == "Unit Step"){
        for (let i = 0; i < t.length ; i++) {
            if (t[i] >= 0){
                x[i] = 1;
                x2[i] = 1;
            } else{
                x[i] = 0;
                x2[i] = 0;
            }
        }
    } else if (x_func == "Dirac Impulse"){
        for (let i = 0; i < t.length ; i++) {
            if (i == 166){
                x[i] = 1/dt;
                x2[i] = 1/dt;
            } else{
                x[i] = 0;
                x2[i] = 0;
            }
        }
    } else if (x_func == "Exponential"){
        for (let i = 0; i < t.length ; i++) {
            if (t[i] >= 0){
                x[i] = Math.exp(-t[i]);
                x2[i] = Math.exp(-t[i]);
            } else{
                x[i] = 0;
                x2[i] = 0;
            }
        }
    }

    if (h_func == "Unit Step"){
        for (let i = 0; i < t.length ; i++) {
            if (t[i] >= 0){
                h[i] = 1;
            } else{
                h[i] = 0;
            }
        }
    } else if (h_func == "Dirac Impulse"){
        for (let i = 0; i < t.length ; i++) {
            if (i == 166){
                h[i] = 1/dt;
            } else{
                h[i] = 0;
            }
        }
    } else if (h_func == "Exponential"){
        for (let i = 0; i < t.length ; i++) {
            if (t[i] >= 0){
                h[i] = Math.exp(-t[i]);
            } else{
                h[i] = 0;
            }
        }
    }


    
    const shift = Math.round((timeshift+2)/dt);
    const result = h.slice(0, shift + 1).reverse(); 
    const padlen = 1000 - result.length;
    for (let i = 0; i < padlen ; i++) {
        result.push(0);
    }

    for (let i = 0; i < result.length ; i++) {
        hinv[i] = result[i];
    }

    for (let i = 0; i < convy.length ; i++) {
        y[i] = convy[i];
    }

    const pts = Math.round((timeshift+1)/dt);
    for (let i = 0; i < pts ; i++) {
        y2[i] = y[i];
    }
    for (let i = pts; i < result.length ; i++) {
        y2[i] = Infinity;
    }

    x_source.change.emit();
    h_source.change.emit();
    y_source.change.emit();
    y2_source.change.emit();
""")

shift_slider.js_on_change('value', callback)
x_selector.js_on_change('value', callback)
h_selector.js_on_change('value', callback)
# Combine the figures and sliders into a Bokeh layout
layout = gridplot([[row(x_fig, h_fig)], 
                   [row(column(x_selector, h_selector, shift_slider), y_fig)]])
# layout = gridplot([[row(x_fig, h_fig)], [row(shift_slider, y_fig)]])

show(layout)
# bokeh serve --show --port 5001 convolution.py