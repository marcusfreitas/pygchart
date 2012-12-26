import os
import shutil
import unittest
from pgchart import *


class TestPgChart(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('tmp'):
            os.mkdir('tmp')

    def tearDown(self):
        if os.path.exists('tmp'):
            shutil.rmtree('tmp')

    def test_data_class_init(self):
        self.assertRaises(AssertionError, Data, None, None, None)
        self.assertRaises(AssertionError, Data, {}, None, None)
        self.assertRaises(AssertionError, Data, [], {}, None)
        self.assertRaises(AssertionError, Data, [], {}, [])
        self.assertRaises(AssertionError, Data, [], ['test'], {})
        data = Data(['a', 'b'], ['string', 'number'], {})
        self.assertTrue(data != None)

    def test_data_get_json_data(self):
        data = Data(['a', 'b'], ['string', 'number'], 
            {'label1': 1, 'label2': 2})
        result = data.get_json_data()
        self.assertTrue(isinstance(result, str))

    def test_chart_class_init(self):
        self.assertRaises(InvalidParametersException, Chart, None, None, 
            None, None)
        self.assertRaises(InvalidParametersException, Chart, 'title', None, 
            None, None)
        self.assertRaises(InvalidParametersException, Chart, 'title', 'div', 
            None, None)
        self.assertRaises(InvalidParametersException, Chart, 'title', 'div', 
            '', None)
        self.assertRaises(AbstractClassException, Chart, 'title', 'div', 
            Data(['a'], ['string'], {}), None)

    def test_pie_chart_get_js_function(self):
        options = {'title': 'Title', 'height': 250, 'width': 400}
        data = Data(['a', 'b'], ['string', 'number'], {"a": 1, "b": 2})
        pie_chart = PieChart('Title', 'div', data, options)
        result = pie_chart.get_js_function()
        self.assertTrue(isinstance(result, str))

    def test_chart_hub_class_init(self):
        self.assertRaises(AssertionError, ChartHub, None)
        chart_hub = ChartHub([])
        self.assertTrue(chart_hub != None)

    def test_chart_hub_create_js_file(self):
        options = {'title': 'Title', 'height': 250, 'width': 400}
        data = Data(['a', 'b'], ['string', 'number'], {"a": 1, "b": 2})
        pie_chart = PieChart('Title', 'div', data, options)
        chart_hub = ChartHub([pie_chart])
        self.assertRaises(InvalidParametersException, chart_hub.create_js_file,
            None)
        chart_hub.create_js_file('tmp/tmp.js')
        self.assertTrue(os.path.exists('tmp/tmp.js'))

    def test_chart_hub_create_html_file(self):
        options = {'title': 'Title', 'height': 250, 'width': 400}
        data = Data(['a', 'b'], ['string', 'number'], {"a": 1, "b": 2})
        pie_chart = PieChart('Title', 'div', data, options)
        chart_hub = ChartHub([pie_chart])
        self.assertRaises(InvalidParametersException, chart_hub.create_js_file,
            None)
        chart_hub.create_html_file('tmp/tmp.html')
        self.assertTrue(os.path.exists('tmp/tmp.html'))


if __name__ == '__main__':
    unittest.main()


        