from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, CustomJS, Slider, Select
from bokeh.plotting import figure, output_file, show, curdoc, save
import numpy as np

# dict, OrderedDict, lists, arrays and DataFrames are valid inputs


t1 = np.linspace(-5, 5, 50)
y1 = np.sin(t1)
origin = y1.tolist()

t2 = t1[::4]
y2 = np.sin(t2)
sample = origin[::4]

origin_source = ColumnDataSource(data=dict(x=t1, y=origin))
sample_source = ColumnDataSource(data=dict(x=t2, y=sample))

x_fig = figure(title='Origin Signal', width=350, height=300, x_range=(-5, 5), y_range=(-3, 3))
x_fig.scatter('x', 'y', source=origin_source, size=3, color="blue", legend_label="origin", fill_alpha=0.6, line_alpha=0.6)

y_fig = figure(title='Sample Signal', width=350, height=300, x_range=(-5, 5), y_range=(-3, 3))
y_fig.scatter('x', 'y', source=origin_source, size=3, color="blue", legend_label="origin", fill_alpha=0.2, line_alpha=0.2)
y_fig.scatter('x', 'y', source=sample_source, size=3, color='blue', legend_label="sample", fill_alpha=0.8, line_alpha=0.8)

slider = Slider(title='step', value=1, start=1, end=10, step=1, width=700, height=300)

callback = CustomJS(args=dict(source=source, amp=amp_slider, freq=freq_slider, phase=phase_slider, offset=offset_slider),
                    code="""
    const data = source.data;
    const A = amp.value;
    const k = freq.value;
    const phi = phase.value;
    const B = offset.value;
    const x = data['x']
    const y = data['y']
    for (let i = 0; i < x.length; i++) {
        y[i] = B + A*Math.sin(k*x[i]+phi);
    }
    source.change.emit();
""")

amp_slider.js_on_change('value', callback)


layout=column(row(x_fig, y_fig), slider)
show(layout)