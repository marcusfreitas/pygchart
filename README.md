pygchart
========

This is a google chart wrapper which generate a java script code reponsible for generating a google chart.
It allows you to generate a js file with the charts' code and a html file with all your charts' codes and divs wich you 
can use right away.

PyGChart has been written on Python, so you can use open source package anywhere you have Python, even in Windows if you like.

## Installation
You can install PyGChart as a python script.

### Requirements
PyGChart needs **Python 2.x** from **2.4 and later**.

#### Usage

from pygchart import *

data = Data(
	columns_list=['Country', 'States'],
	types_list=[Data.STRING, Data.Number],
	values_dict={'Brazil': 27, 'USA': 50}
	) 
options = {'title': 'How many states', 'heigth': 250, 'width':300}

bar_chart = BarChart(name='StatesNumber', target_div='states_div', data, options)

chart_hub = ChartHub(charts_list=[bar_chart])

chart_hub.create_js_file('state_number_chart.js')

chart_hub.create_html_file('state_number_page.html')