from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import row
import numpy as np

# Define the number of points in the signal and its frequency components
N = 16
freqs = [2, 4, 8]

# Generate a random signal with those frequency components
t = np.arange(N)
signal = np.sum([np.sin(2*np.pi*f*t/N) for f in freqs], axis=0)

# Create the initial data source for the signal plot
source_signal = ColumnDataSource(data=dict(x=t, y=signal))

# Create the initial data source for the transform plot
transform_data = dict(x=[], y=[], color=[])
for i in range(N):
    transform_data['x'].append(i)
    transform_data['y'].append(0)
    transform_data['color'].append('blue' if i == 0 else 'gray')
source_transform = ColumnDataSource(data=transform_data)

# Create the signal plot
signal_plot = figure(title='Signal', plot_width=400, plot_height=400)
signal_plot.line(x='x', y='y', source=source_signal)

# Create the transform plot
transform_plot = figure(title='Discrete Fourier Transform', plot_width=400, plot_height=400, x_range=(0, N))
transform_plot.vbar(x='x', top='y', width=0.8, color='color', source=source_transform)

# Define the function to update the transform plot
def update_transform():
    # Get the current data from the signal plot
    t = source_signal.data['x']
    signal = source_signal.data['y']
    
    # Calculate the discrete Fourier transform of the signal
    transform = np.zeros(N, dtype=np.complex)
    for k in range(N):
        for n in range(N):
            transform[k] += signal[n] * np.exp(-1j*2*np.pi*k*n/N)
            
        # Update the data source for the transform plot
        source_transform.data['y'][k] = np.abs(transform[k])
        source_transform.data['color'][k] = 'blue' if k == 0 else 'gray'
        source_transform.stream(dict(y=[], color=[]))
        source_transform.patch({'y': [(0, source_transform.data['y'][0])], 'color': [(0, 'blue')]})
        source_transform.stream(dict(y=[source_transform.data['y'][k]], color=['gray']))
        
# Add both plots to the document and define the update callback
curdoc().add_root(row(signal_plot, transform_plot))
curdoc().add_periodic_callback(update_transform, 1000)
