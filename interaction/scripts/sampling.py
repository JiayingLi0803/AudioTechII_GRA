from collections import OrderedDict
from bokeh.charts import Dot, output_file, show

# dict, OrderedDict, lists, arrays and DataFrames are valid inputs
xyvalues = OrderedDict()
xyvalues['python']=[2, 5]
xyvalues['pypy']=[12, 40]
xyvalues['jython']=[22, 30]

dot = Dot(xyvalues, ['cpu1', 'cpu2'], title='dots')

output_file('dot.html')
show(dot)