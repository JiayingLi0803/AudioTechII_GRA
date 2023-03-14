import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Select
from bokeh.embed import components
from bokeh.plotting import ColumnDataSource, figure, show

x = np.linspace(-10, 10, 500)
y = np.where(abs(x)<=0.5, 1, 0)

source = ColumnDataSource(data=dict(x=x, y=y))

plot = figure(y_range=(-1, 2), x_range=(-5, 5), width=400, height=400)
plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

select1 = Select(title="Function 1:", value="unit step", options=["unit step", "exponential"])
select1.js_on_change("value", CustomJS(code="""
    console.log('select: value=' + this.value, this.toString())
"""))
select2 = Select(title="Function 2:", value="unit step", options=["unit step", "exponential"])
select2.js_on_change("value", CustomJS(code="""
    console.log('select: value=' + this.value, this.toString())
"""))
time_slider = Slider(start=-5, end=10, value=0, step=.1, title="time")




callback = CustomJS(args=dict(source=source, time=time_slider),
                    code="""
    const data = source.data;
    
    const t = time.value;
    const f1 = select1.value;
    const f2 = select2.value;

    const x = data['x']
    const y = data['y']

    for (let i = 0; i < x.length; i++) {
        y[i] = Math.abs(x[i]-t);
    }
    

    source.change.emit();
""")

time_slider.js_on_change('value', callback)
select1.js_on_change('value', callback)
select2.js_on_change('value', callback)

layout = column(
    plot,
    row(select1, select2, time_slider),
)

show(layout)


# x = np.linspace(0, 10, 500)
# y = np.sin(x)

# source = ColumnDataSource(data=dict(x=x, y=y))

# plot = figure(y_range=(-10, 10), width=400, height=400)

# plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)

# amp_slider = Slider(start=0.1, end=10, value=1, step=.1, title="Amplitude")
# freq_slider = Slider(start=0.1, end=10, value=1, step=.1, title="Frequency")
# phase_slider = Slider(start=0, end=6.4, value=0, step=.1, title="Phase")
# offset_slider = Slider(start=-5, end=5, value=0, step=.1, title="Offset")

# callback = CustomJS(args=dict(source=source, amp=amp_slider, freq=freq_slider, phase=phase_slider, offset=offset_slider),
#                     code="""
#     const data = source.data;
#     const A = amp.value;
#     const k = freq.value;
#     const phi = phase.value;
#     const B = offset.value;
#     const x = data['x']
#     const y = data['y']
#     for (let i = 0; i < x.length; i++) {
#         y[i] = B + A*Math.sin(k*x[i]+phi);
#     }
#     source.change.emit();
# """)

# amp_slider.js_on_change('value', callback)
# freq_slider.js_on_change('value', callback)
# phase_slider.js_on_change('value', callback)
# offset_slider.js_on_change('value', callback)

# layout = row(
#     plot,
#     column(amp_slider, freq_slider, phase_slider, offset_slider),
# )

# show(layout)


# script, div = components(plot)
# print(script)
# print(div)


