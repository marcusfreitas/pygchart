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
                columns_list=['Year', 'Sales', 'Expenses'],
                types_list=[Data.STRING, Data.NUMBER, Data.NUMBER],
                values_list=[
                    ['2004',  1000,      400],
                    ['2005',  1170,      460],
                    ['2006',  660,       1120],
                    ['2007',  1030,      540]
                ]
          ) 
            
    options = {'title': 'Company Performance', 'height': 450, 'width':600}

    bar_chart = BarChart(name='CompPerform', target_div='comp_perf_bar_div', 
                         data=data, chart_options=options)

    chart_hub = ChartHub(charts_list=[bar_chart])

    chart_hub.create_js_file('examples/bar_chart.js')

    chart_hub.create_html_file('examples/bar_chart.html')
