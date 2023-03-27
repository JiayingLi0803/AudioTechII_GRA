from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider, Select, Div
from bokeh.plotting import figure, output_file, show, curdoc, save
import numpy as np

# Define the exponential function
def exp_func(t, a):
    return np.exp(-a * t) * (t >= 0)

# Define the rectangular function
def rect_func(t, a):
    return np.piecewise(t, [t < 0, (t>=0)*(t<a), t >= a], [0, 1, 0])

# Define the triagular function
def tri_func(t, a):
    return np.piecewise(t, [t < 0, (t>=0)*(t<a), t >= a], [0, lambda t: a-t, 0])

# Define correlation function
def corr(signal, impulse, time):
    dt = time[1] - time[0]
    result = np.correlate(signal, impulse, "full")
    return result[500:1500] * dt

# Define shift function
def shift(signal, time, shifttime):
    dt = time[1] - time[0]
    pts = int(np.abs(shifttime)/dt)
    if shifttime >= 0:
        result = signal[:len(signal)-pts]
        result = np.pad(result, (1000-len(result), 0), "constant")
    else:
        print(pts)
        result = signal[pts:]
        result = np.pad(result, (0, 1000-len(result)), "constant")
    return result

# Generate input and impulse response signals
# Set up the time axis
t = np.linspace(-5, 5, 1000)
# Set up the functions to convolve
x = rect_func(t, 1)
h = exp_func(t, 1)
hshift = shift(h, t, -4)
y = corr(x, h, t)
y2 = corr(x, h, t)
# x func
x_rect = rect_func(t, 1)
x_tri = tri_func(t, 1)
x_exp = exp_func(t, 1)
# h func
h_rect = rect_func(t, 1)
h_tri = tri_func(t, 1)
h_exp = exp_func(t, 1)
# hshift func
hshift_rect = shift(h_rect, t, 0)
hshift_tri = shift(h_tri, t, 0)
hshift_exp = shift(h_exp, t, 0)
# y func
y_rect_rect = corr(x_rect, h_rect, t)
y_rect_tri = corr(x_rect, h_tri, t)
y_rect_exp = corr(x_rect, h_exp, t)
y_tri_rect = corr(x_tri, h_rect, t)
y_tri_tri = corr(x_tri, h_tri, t)
y_tri_exp = corr(x_tri, h_exp, t)
y_exp_rect = corr(x_exp, h_rect, t)
y_exp_tri = corr(x_exp, h_tri, t)
y_exp_exp = corr(x_exp, h_exp, t)

for i in range(len(y2)):
    if i>=1:
        y2[i] = np.inf

# Transfer to list
x = x.tolist()
h = h.tolist()
y = y.tolist()
y2 = y2.tolist()
# x list
x_rect = x_rect.tolist()
x_tri = x_tri.tolist()
x_exp = x_exp.tolist()
# h list
h_rect = h_rect.tolist()
h_tri = h_tri.tolist()
h_exp = h_exp.tolist()
# y list
y_rect_rect = y_rect_rect.tolist()
y_rect_tri = y_rect_tri.tolist()
y_rect_exp = y_rect_exp.tolist()
y_tri_rect = y_tri_rect.tolist()
y_tri_tri = y_tri_tri.tolist()
y_tri_exp = y_tri_exp.tolist()
y_exp_rect = y_exp_rect.tolist()
y_exp_tri = y_exp_tri.tolist()
y_exp_exp = y_exp_exp.tolist()

# Set up Bokeh data sources for the signals
x_source = ColumnDataSource(data=dict(x=t, y1=x, y2=h))
h_source = ColumnDataSource(data=dict(x=t, y1=x, y2=hshift))
y_source = ColumnDataSource(data=dict(x=t, y=y))
y2_source = ColumnDataSource(data=dict(x=t, y=y2))
xfunc_source = ColumnDataSource(data=dict(x_rect=x_rect, x_tri=x_tri, x_exp=x_exp))        
hfunc_source = ColumnDataSource(data=dict(h_rect=h_rect, h_tri=h_tri, h_exp=h_exp))  
corr_source = ColumnDataSource(data=dict(y_rect_rect = y_rect_rect, 
                                         y_rect_tri = y_rect_tri, 
                                         y_rect_exp = y_rect_exp, 
                                         y_tri_rect = y_tri_rect,
                                         y_tri_tri = y_tri_tri,
                                         y_tri_exp = y_tri_exp,
                                         y_exp_rect = y_exp_rect,
                                         y_exp_tri = y_exp_tri,
                                         y_exp_exp = y_exp_exp))
                                 

# Set up Bokeh figures for the signals
x_fig = figure(title='Input Signal', width=350, height=300, x_range=(-4.01, 4.01), y_range=(-1, 4))
# x_fig.varea(x='x', y1='y1', y2='y2', source=x_source, fill_alpha=0.5)
x_fig.line('x', 'y1', source=x_source, line_width=2, line_color='blue', legend_label="x(t)")
x_fig.line('x', 'y2', source=x_source, line_width=2, line_color='red', line_dash="dotted", legend_label="h(t)")
x_fig.legend.location = "top_left"
h_fig = figure(title='Signal Shift', width=350, height=300, x_range=(-4.01, 4.01), y_range=(-1, 4))
h_fig.line('x', 'y1', source=h_source, line_width=2, line_color='blue', legend_label="x(t)")
h_fig.line('x', 'y2', source=h_source, line_width=2, line_color='red', line_dash="dotted", legend_label="h(t-t')")
h_fig.varea(x='x', y1='y1', y2='y2', source=h_source, fill_alpha=0.2)
h_fig.legend.location = "top_left"
y_fig = figure(title='Output Signal', width=350, height=300, x_range=(-4.01, 4.01), y_range=(-1, 4))
y_fig.line('x', 'y', source=y_source, line_width=2, line_color='green', line_alpha=0.2)
y_fig.line('x', 'y', source=y2_source, line_width=2, line_color='green', legend_label="correlation")
y_fig.legend.location = "top_left"

# Define time shift slider
shift_slider = Slider(title='t', value=-4, start=-4, end=4, step=0.01, width=340, height=300)
# shift_slider.on_change('value', update_data)

# Define the selector widget and its options
options = ['Rectangular', 'Triangular', 'Exponential']
x_selector = Select(title='Signal 1:', value=options[0], options=options)
h_selector = Select(title='Signal 2:', value=options[2], options=options)

# Define the text


callback = CustomJS(args=dict(x_source=x_source, 
                              h_source=h_source, 
                              y_source=y_source, 
                              y2_source=y2_source,
                              xfunc_source=xfunc_source,
                              hfunc_source=hfunc_source,
                              corr_source=corr_source,
                              shiftval=shift_slider,
                              x_selector=x_selector,
                              h_selector=h_selector),
                    code="""
    const xdata = x_source.data;
    const hdata = h_source.data;
    const ydata = y_source.data;
    const y2data = y2_source.data;
    const xfuncdata = xfunc_source.data;
    const hfuncdata = hfunc_source.data;
    const corrdata = corr_source.data;
    const timeshift = shiftval.value;
    const x_func = x_selector.value;
    const h_func = h_selector.value;
    const t = xdata["x"];
    const x = xdata["y1"];
    const h = xdata["y2"];
    const x2 = hdata["y1"]
    const hshift = hdata["y2"];
    const y = ydata["y"];
    const t2 = y2data["x"];
    const y2 = y2data["y"];
    let corry = corrdata["y_rect_exp"];

    if (x_func == "Rectangular"){
        if (h_func == "Rectangular"){
            corry = corrdata["y_rect_rect"];
        } else if (h_func == "Triangular"){
            corry = corrdata["y_rect_tri"];
        }else if (h_func == "Exponential"){
            corry = corrdata["y_rect_exp"];
        }
    } else if (x_func == "Triangular"){
        if (h_func == "Rectangular"){
            corry = corrdata["y_tri_rect"];
        } else if (h_func == "Triangular"){
            corry = corrdata["y_tri_tri"];
        }else if (h_func == "Exponential"){
            corry = corrdata["y_tri_exp"];
        }
    } else if (x_func == "Exponential"){
        if (h_func == "Rectangular"){
            corry = corrdata["y_exp_rect"];
        } else if (h_func == "Triangular"){
            corry = corrdata["y_exp_tri"];
        }else if (h_func == "Exponential"){
            corry = corrdata["y_exp_exp"];
        }
    }

    if (x_func == "Rectangular"){
        for (let i = 0; i < t.length ; i++) {
            x[i] = xfuncdata["x_rect"][i];
            x2[i] = xfuncdata["x_rect"][i];
        }
    } else if (x_func == "Triangular"){
        for (let i = 0; i < t.length ; i++) {
            x[i] = xfuncdata["x_tri"][i];
            x2[i] = xfuncdata["x_tri"][i];
        }
    } else if (x_func == "Exponential"){
        for (let i = 0; i < t.length ; i++) {
            x[i] = xfuncdata["x_exp"][i];
            x2[i] = xfuncdata["x_exp"][i];
        }
    }

    if (h_func == "Rectangular"){
        for (let i = 0; i < t.length ; i++) {
            h[i] = hfuncdata["h_rect"][i];
        }
    } else if (h_func == "Triangular"){
        for (let i = 0; i < t.length ; i++) {
            h[i] = hfuncdata["h_tri"][i];
        }
    } else if (h_func == "Exponential"){
        for (let i = 0; i < t.length ; i++) {
            h[i] = hfuncdata["h_exp"][i];
        }
    }

    const dt = t[1]-t[0];
    const shift = Math.round(timeshift/dt);
    var result = h;
    var padlen = 0;
    if (shift >= 0){
        result = h.slice(0, 1000-shift);
        console.log(result.length);
        padlen = 1000 - result.length;
        for (let i = 0; i < padlen ; i++) {
            result.unshift(0);
        }
    } else if (shift < 0){
        result = h.slice(-shift-1000);
        padlen = 1000 - result.length;
        for (let i = 0; i < padlen ; i++) {
            result.push(0);
        }
    }

    for (let i = 0; i < result.length ; i++) {
        hshift[i] = result[i];
    }

    for (let i = 0; i < corry.length ; i++) {
        y[i] = corry[i];
    }

    const pts = Math.round((timeshift+5)/dt);
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