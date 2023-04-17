import numpy as np

from bokeh.layouts import column, row
from bokeh.models import CustomJS, Slider, Div, TeX, PreText
from bokeh.embed import components
from bokeh.plotting import ColumnDataSource, figure, show

x = np.linspace(0, 1, 500)
y = np.sin(2*np.pi*x)
cosbase

source = ColumnDataSource(data=dict(x=x, y=y))

# Define plot figure
plot = figure(title='Signal', y_range=(-10, 10), width=350, height=300, x_axis_label='time (s)', y_axis_label='Amplitude')
plot.line('x', 'y',source=source, line_color='blue', line_width=2)

# Define text div
formuladiv = Div(text=r"""Expression: $$y = Asin(2 \pi f t + \phi) + s$$""")
Atext = PreText(text=r"""Amplitude: 1.00""")
ftext = PreText(text=r"""Frequency (Hz):    1.00""")
ptext = PreText(text=r"""Phase:                0.00""")
otext = PreText(text=r"""Offset:                   0.00""")

# Define Slider

callback = CustomJS(args=dict(source=source, amp=amp_slider, freq=freq_slider, 
                              phase=phase_slider, offset=offset_slider, 
                              Atext=Atext, ftext=ftext, ptext=ptext, otext=otext),
                    code="""
    const data = source.data;
    const A = amp.value;
    const k = freq.value;
    const phi = phase.value;
    const B = offset.value;
    const x = data['x'];
    const y = data['y'];
    const At = Atext;
    const ft = ftext;
    const pt = ptext;
    const ot = otext;
    
    At.text = "Amplitude: " + A.toFixed(2);
    ft.text = "Frequency:        " + k.toFixed(2);
    pt.text = "Phase:                " + phi.toFixed(2);
    ot.text = "Offset:                   " + B.toFixed(2);


    for (let i = 0; i < x.length; i++) {
        y[i] = B + A*Math.sin(k*x[i]+phi);
    }
    source.change.emit();
    Atext.change.emit();
    ftext.change.emit();
    ptext.change.emit();
    otext.change.emit();
""")

amp_slider.js_on_change('value', callback)
freq_slider.js_on_change('value', callback)
phase_slider.js_on_change('value', callback)
offset_slider.js_on_change('value', callback)

layout = column(row(
    plot,
    column(amp_slider, freq_slider, phase_slider, offset_slider)),
    column(formuladiv, Atext, ftext, ptext, otext)
)

show(layout)


script, div = components(plot)
print(script)
print(div)

