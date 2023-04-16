from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider, Select
from bokeh.plotting import figure, output_file, show, curdoc, save
import numpy as np

# dict, OrderedDict, lists, arrays and DataFrames are valid inputs


t1 = np.linspace(-5, 5, 500)
y1 = np.sin(t1)
t1.tolist()
origin = y1.tolist()

t2 = t1
sample = np.sin(t2).tolist()

for i in range(len(sample)):
    if i%20 != 0:
        sample[i] = np.Inf

origin_source = ColumnDataSource(data=dict(x=t1, y=origin))
sample_source = ColumnDataSource(data=dict(x=t2, y=sample))

x_fig = figure(title='Input Signal', width=350, height=300, x_range=(-5, 5), y_range=(-3, 3), x_axis_label='time (s)', y_axis_label='Amplitude')
x_fig.scatter('x', 'y', source=origin_source, size=3, color="blue", fill_alpha=0.6, line_alpha=0.6)

y_fig = figure(title='Sample Signal', width=350, height=300, x_range=(-5, 5), y_range=(-3, 3), x_axis_label='time (s)', y_axis_label='Amplitude')
y_fig.scatter('x', 'y', source=origin_source, size=3, color="blue", fill_alpha=0.05, line_alpha=0)
y_fig.scatter('x', 'y', source=sample_source, size=3, color='blue', fill_alpha=0.8, line_alpha=0.8)

slider = Slider(title='sample rate', value=1, start=1, end=20, step=1, width=700, height=300)

callback = CustomJS(args=dict(origin_source=origin_source, sample_source=sample_source, slider=slider),
                    code="""
    const origin_data = origin_source.data;
    const sample_data = sample_source.data;
    const rateval = slider.value;
    const t = origin_data['x'];
    const y = origin_data['y'];
    const t2 = sample_data['x'];
    const y2 = sample_data['y'];

    var rate = 21-rateval;
    for (let i = 0; i < t.length; i++) {
        if (i % rate != 0){
            y2[i] = Infinity;
        } else {
            y2[i] = y[i];
        }
    }
    sample_source.change.emit();
""")

slider.js_on_change('value', callback)


layout=column(row(x_fig, y_fig), slider)
show(layout)