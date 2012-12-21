"""
pygchart - A Python wrapper for the Google Chart Java Script API

https://github.com/vinyguitar/pygchart

"""

import os
import json

__version__ = '0.0.1'
__author__ = 'Vinicius Freitas'


# Exception Classes
# -----------------------------------------------------------------------------


class PyGoogleChartException(Exception):
    pass


class NoDataGivenException(PyGoogleChartException):
    pass


class InvalidParametersException(PyGoogleChartException):
    pass


class BadContentTypeException(PyGoogleChartException):
    pass


class AbstractClassException(PyGoogleChartException):
    pass


class UnknownChartType(PyGoogleChartException):
    pass


# Data Classes
# -----------------------------------------------------------------------------


class Data(object):
    """"""

    STRING = 'string'
    NUMBER = 'number'
    DATE = 'date'
    DATETIME = 'DateTime'
    TYPES = [STRING, NUMBER, DATE, DATETIME]

    def __init__(self, columns_list, types_list, values_dict):
        assert(isinstance(columns_list, list))
        assert(isinstance(types_list, list))
        assert(isinstance(values_dict, dict))
        for type_item in types_list:
            assert(type_item in Data.TYPES)
        
        self.columns = columns_list
        self.types = types_list
        self.rows = values_dict

    def get_json_data(self):
        json_buffer = "{cols:[COLS_TOKEN], rows:[ROWS_TOKEN]}"
        tmp_buffer = ""
        for x in xrange(0, len(self.columns)):
            tmp_buffer += "{id:'%s', label:'%s', type:'%s'}" % (self.columns[x], 
                self.columns[x], self.types[x])
            if x < len(self.columns):
                tmp_buffer += ","
        json_buffer = json_buffer.replace("COLS_TOKEN", tmp_buffer)

        rows = self.rows.keys()
        tmp_buffer = ""
        count = 0
        for row in rows:
            tmp_buffer += "{c:[{v:'%s'},{v:%s}]}" % (row, self.rows[row])
            count += 1
            if count < len(rows):
                tmp_buffer += ","
        json_buffer = json_buffer.replace("ROWS_TOKEN", tmp_buffer)

        return json_buffer


# Chart Classes
# -----------------------------------------------------------------------------


class ChartHub(object):
    """"""
    def __init__(self, charts_list, js_file_name):
        assert(isinstance(charts_list, list))
        if not js_file_name:
            raise InvalidParametersException('js_file_name must be informed!')
        self.charts_list = charts_list
        self.js_file_name = js_file_name

    def get_js_function(self):
        function_buffer = "function drawChart(){CONTENT_TOKEN}"
        content_buffer = ""
        for chart in self.charts_list:
            content_buffer += "draw%sChart();" % chart.title        
        return function_buffer.replace("CONTENT_TOKEN", content_buffer)

    def create_js_file(self):
        content_buffer = """
        // Load the Visualization API and the piechart package.
        google.load('visualization', '1.0', {'packages':['corechart']});
        // Set a callback to run when the Google Visualization API is loaded.
        google.setOnLoadCallback(drawChart);\n"""
        for chart in self.charts_list:
            content_buffer += chart.get_js_function()

        content_buffer += self.get_js_function()

        js_file = open(self.js_file_name, "w")
        js_file.write(content_buffer)
        js_file.close()
        return content_buffer

    def create_html_file(self, html_file_name):
        html_buffer = \
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="utf-8">
        <title></title>
        <!-- Custom report generate -->
        <script src="%s"></script>
        </head>

        <body>
        CHARTS_DIV_TOKEN
        </body>
        </html>
        """
        content_buffer = ""
        for chart in self.charts_list:
            content_buffer += "<div id=%s></div>" % (chart.target_div)

        html_buffer = html_buffer.replace("CHARTS_DIV_TOKEN", content_buffer)

        html_file = open(html_file_name, "w")
        html_file.write(html_buffer)
        html_file.close()
        return html_buffer

class Chart(object):
    """"""
    def __init__(self, title, target_div, data, chart_options):
        if not title:
            raise InvalidParametersException("title must be informed")
        if not target_div:
            raise InvalidParametersException("target_div must be informed")
        if type(data) != Data:
            raise InvalidParametersException('data must be a Data class')
        if not chart_options:
            InvalidParametersException('chart_options must be informed')
        if type(self) == Chart:
            raise AbstractClassException('This is an abstract class')
            
        self.title = title
        self.target_div = target_div
        self.chart_type = ""
        self.data = data
        self.chart_options = chart_options

    def _set_data(self, structure):
        data_buffer = str('var data = new google.visualization.DataTable(%s);')\
        % structure
        return data_buffer

    def _set_options(self, title, height, width):
        options_buffer = str(
            "var options = {'title':'%s', 'width':%s, 'height': %s};") \
        % (title, width, height)
        return options_buffer

    def _set_chart(self):
        chart_buffer = str("var chart = new google.visualization.%s \
            (document.getElementById('%s')); chart.draw(data, options);") \
        % (self.chart_type, self.target_div)
        return chart_buffer

    def get_js_function(self):
        function_buffer = "function draw%sChart(){CONTENT_TOKEN}" % self.title
        content_buffer = self._set_data(self.data.get_json_data())
        content_buffer += self._set_options(
            self.chart_options['title'],
            self.chart_options['height'],
            self.chart_options['width'])
        content_buffer += self._set_chart()
        function_buffer = function_buffer.replace("CONTENT_TOKEN", 
            content_buffer)
        return function_buffer


class BarChart(Chart):
    """"""
    def __init__(self, title, target_div, data, chart_options):
        Chart.__init__(self, title, target_div, data, chart_options)
        self.chart_type = "BarChart"


class PieChart(Chart):
    """"""
    def __init__(self, title, target_div, data, chart_options):
        Chart.__init__(self, title, target_div, data, chart_options)
        self.chart_type = "PieChart"


if __name__ == '__main__':

    options = {'title': 'Total', 'height': 250, 'width': 400}
    data = Data(['Apks', 'Count'], ['string', 'number'], {"Malicious": 2571, "Trusted": 3751})
    bar_chart = BarChart('Totals', 'total_chart_div', data, options)

    # options = {'title': 'Signature Efficiency', 'height': 250, 'width': 400}
    # data = Data(['Apks', 'Count'], ['string', 'number'], {"Malicious": 0, "Classified": 2571})
    # pie_chart = PieChart('SignatureEfficiency', 'sig_eff_div', data, options)

    options = {'title': 'Heuristic Efficiency (Malicious Base)', 'height': 250, 'width': 400}
    total_malicious = 2571
    classified = 88 * total_malicious / 100
    unclassified = total_malicious - classified
    data = Data(['Apks', 'Count'], ['string', 'number'], {"Unclassified": unclassified, "Classified": classified})
    heuri_mal_pie_chart = PieChart('HeuristicMaliciousEfficiency', 'heur_mal_div', data, options)

    options = {'title': 'Heuristic Efficiency (Trusted Base)', 'height': 250, 'width': 400}
    total_trusted = 3571
    classified = 99 * total_trusted / 100
    unclassified = total_trusted - classified
    data = Data(['Apks', 'Count'], ['string', 'number'], {"Unclassified": unclassified, "Classified": classified})
    heuri_tru_pie_chart = PieChart('HeuristicTrustedEfficiency', 'heur_tru_div', data, options)

    charts = ChartHub(
        [bar_chart, heuri_mal_pie_chart, heuri_tru_pie_chart],
        'chart.js'
        )
    charts.create_js_file()
    print charts.create_html_file('report.html')
    
        
    





    