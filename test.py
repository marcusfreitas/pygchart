import os
import shutil
import unittest
from pygchart import *


class TestPgChart(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        if not os.path.exists('examples'):
            os.mkdir('examples')

    def tearDown(self):
        if os.path.exists('tmp'):
            shutil.rmtree('tmp')

    def test_data_class_init(self):
        self.assertRaises(AssertionError, Data, None, None, None)
        self.assertRaises(AssertionError, Data, {}, None, None)
        self.assertRaises(AssertionError, Data, [], {}, None)
        self.assertRaises(AssertionError, Data, [], {}, [])
        self.assertRaises(AssertionError, Data, [], ['test'], {})
        data = Data(['a', 'b'], ['string', 'number'], [])
        self.assertTrue(data != None)

    def test_data_get_json_data(self):
        data = Data(['a', 'b'], ['string', 'number'], 
            [['label1', 1], ['label2', 2]])
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
            Data(['a'], ['string'], []), None)

    def test_pie_chart_get_js_function(self):
        options = {'title': 'Title', 'height': 250, 'width': 400}
        data = Data(['a', 'b'], ['string', 'number'], [["a", 1], ["b", 2]])
        pie_chart = PieChart('Title', 'div', data, options)
        result = pie_chart.get_js_function()
        self.assertTrue(isinstance(result, str))

    def test_chart_hub_class_init(self):
        self.assertRaises(AssertionError, ChartHub, None)
        chart_hub = ChartHub([])
        self.assertTrue(chart_hub != None)

    def test_chart_hub_create_js_file(self):
        options = {'title': 'Title', 'height': 250, 'width': 400}
        data = Data(['a', 'b'], ['string', 'number'], [["a", 1], ["b", 2]])
        pie_chart = PieChart('Title', 'div', data, options)
        chart_hub = ChartHub([pie_chart])
        self.assertRaises(InvalidParametersException, chart_hub.create_js_file,
            None)
        chart_hub.create_js_file('tmp/tmp.js')
        self.assertTrue(os.path.exists('tmp/tmp.js'))

    def test_chart_hub_create_html_file(self):
        options = {'title': 'Title', 'height': 250, 'width': 400}
        data = Data(['a', 'b'], ['string', 'number'], [["a", 1], ["b", 2]])
        pie_chart = PieChart('Title', 'div', data, options)
        chart_hub = ChartHub([pie_chart])
        self.assertRaises(InvalidParametersException, chart_hub.create_js_file,
            None)
        chart_hub.create_html_file('tmp/tmp.html')
        self.assertTrue(os.path.exists('tmp/tmp.html'))

    def test_bar_chart(self):
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
        self.bar_chart = BarChart(name='CompPerform', 
            target_div='comp_perf_bar_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.bar_chart])
        chart_hub.create_js_file('examples/bar_chart.js')
        chart_hub.create_html_file('examples/bar_chart.html')

    def test_pie_chart(self):
        data = Data(
                columns_list=['Tasks', 'Hours'],
                types_list=[Data.STRING, Data.NUMBER],
                values_list=[
                    ["Work", 11],
                    ["Eat", 2],
                    ["Commute", 2],
                    ["Watch TV", 2],
                    ["Sleep", 7]
                ]
            )
        options = {'title':'My Daily Activities'}
        self.pie_chart = PieChart(name='DailyActivity', 
            target_div='activity_div',
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.pie_chart])
        chart_hub.create_js_file('examples/pie_chart.js')
        chart_hub.create_html_file('examples/pie_chart.html')

    def test_column_chart(self):
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
        options = {'title': 'Company Performance', 'height': 450, 'width':600,
        'hAxis': {'title': 'Year', 'titleTextStyle': {'color': 'red'}}}
        self.column_chart = ColumnChart(name='CompPerform', 
            target_div='com_perf_col_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.column_chart])
        chart_hub.create_js_file('examples/column_chart.js')
        chart_hub.create_html_file('examples/column_chart.html')

    def test_line_chart(self):
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
        options = {'title': 'Company Performance', 'height': 500, 'width':900}
        self.line_chart = LineChart(name='CompPerform', 
            target_div='com_perf_line_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.line_chart])
        chart_hub.create_js_file('examples/line_chart.js')
        chart_hub.create_html_file('examples/line_chart.html')

    def test_candle_stick_chart(self):
        data = Data(columns_list=['Day', 'StickStart', 'StickEnd', 
            'CandleStart', 'CandleEnd'],
            types_list=[Data.STRING, Data.NUMBER, Data.NUMBER, Data.NUMBER,
            Data.NUMBER],
            values_list=[
                ['Mon', 20,28, 38, 45],
                ['Tue', 31, 38, 55, 66],
                ['Wed', 50, 55, 77, 80],
                ['Thu', 77, 77, 66, 50],
                ['Fri', 68, 66, 22, 15]
            ])
        options = {'legend':'none', 'height': 500, 'width': 900}

        self.candle_stick_chart = CandleStickChart(name="CandleStickChart",
            target_div='cand_stick_chart_div', data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.candle_stick_chart])
        chart_hub.create_js_file('examples/candle_stick_chart.js')
        chart_hub.create_html_file('examples/candle_stick_chart.html')

    def test_area_chart(self):
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
        options = {'title': 'Company Performance', 'height': 500, 'width':900}
        self.area_chart = AreaChart(name='AreaCompPerform', 
            target_div='com_perf_area_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.area_chart])
        chart_hub.create_js_file('examples/area_chart.js')
        chart_hub.create_html_file('examples/area_chart.html')

    def test_bubble_chart(self):
        data = Data(
                columns_list=['ID', 'Life Expectancy', 'Fertility Rate', 
                'Region', 'Population'],
                types_list=[Data.STRING, Data.NUMBER, Data.NUMBER, Data.STRING,
                Data.NUMBER],
                values_list=[
                    ['CAN', 80.66, 1.67, 'North America', 33739900],
                    ['DEU', 79.84, 1.36, 'Europe', 81902307],
                    ['DNK', 78.6, 1.84, 'Europe', 5523095],
                    ['EGY', 72.73, 2.78, 'Middle East', 79716203],
                    ['GBR', 80.05, 2, 'Europe', 61801570],
                    ['IRN', 72.49, 1.7, 'Middle East', 73137148],
                    ['IRQ', 68.09, 4.77, 'Middle East', 31090763],
                    ['ISR', 81.55, 2.96, 'Middle East', 7485600],
                    ['RUS', 68.6, 1.54, 'Europe', 141850000],
                    ['USA', 78.09, 2.05, 'North America', 307007000]
                ])

        options = {'title': 'Correlation between life expectancy, \
        fertility rate and population of some world countries (2010)',
        'hAxis':{'title': 'Life Expectancy'},
        'vAxis':{'title': 'Fertility Rate'},
        'bubble':{'textStyle': {'fontSize':11}},
        'width': 900, 'height': 500
        }

        self.bubble_chart = BubbleChart(name='BubleLifeExpectancy', 
            target_div='life_expec_bubble_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.bubble_chart])
        chart_hub.create_js_file('examples/bubble_chart.js')
        chart_hub.create_html_file('examples/bubble_chart.html')

    def test_combo_chart(self):
        data = Data(
                columns_list=['Month', 'Bolivia', 'Ecuador', 'Madagascar',
                'Papua New Guinea', 'Rwanda', 'Average'],
                types_list=[Data.STRING, Data.NUMBER, Data.NUMBER, Data.NUMBER,
                Data.NUMBER, Data.NUMBER, Data.NUMBER],
                values_list=[
                    ['2004/05', 165, 938, 522, 998, 450, 614.6],
                    ['2005/06', 135, 1120, 599, 1268, 288, 682],
                    ['2006/07', 157, 1167, 587, 807, 397, 623],
                    ['2007/08', 139, 1110, 615, 968, 215, 609.4],
                    ['2008/09', 136, 691, 629, 1026, 366, 569.6]
                ]
            )
        options = {'title':'Montly Coffe Production by Country',
        'vAxis':{'title':'Cups'},
        'hAxis':{'title':'Month'},
        'seriesType':"bars",
        'series':{5:{'type':'line'}},
        'width': 900, 'height': 500
        }

        self.combo_chart = ComboChart(name='ComboMontlyCoffeProduction', 
            target_div='montly_coffe_combo_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.combo_chart])
        chart_hub.create_js_file('examples/combo_chart.js')
        chart_hub.create_html_file('examples/combo_chart.html')

    def test_scatter_chart(self):
        data = Data(
                columns_list=['Age', 'Weight'],
                types_list=[Data.NUMBER, Data.NUMBER],
                values_list=[
                    [ 8, 12],
                    [ 4, 5.5],
                    [ 11, 14],
                    [ 4, 5],
                    [ 3, 3.5],
                    [ 6.5, 7]
                ]
            )
        options = {'title':'Age vs. Weight comparison',
        'vAxis':{'title':'Weight', 'minValue': 0, 'maxValue': 15},
        'hAxis':{'title':'Age', 'minValue': 0, 'maxValue': 15},
        'legend':"none",
        'width': 900, 'height': 500
        }

        self.scatter_chart = ScatterChart(name='ScatterAgeWeight', 
            target_div='age_weight_scatter_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.scatter_chart])
        chart_hub.create_js_file('examples/scatter_chart.js')
        chart_hub.create_html_file('examples/scatter_chart.html')

    def test_stepped_area_chart(self):
        data = Data(
                columns_list=['Director (Year)', 'Rotten Tomatoes', 'IMDB'],
                types_list=[Data.STRING, Data.NUMBER, Data.NUMBER],
                values_list=[
                    ['Alfred Hitchcock (1935)', 8.4, 7.9],
                    ['Ralph Thomas (1959)', 6.9, 6.5],
                    ['Don Sharp (1978)', 6.5, 6.4],
                    ['James Hawes (2008)', 4.4, 6.2]
                ]
            )

        options = {
        'title':'Decline of \'The 39 Steps\'',
        'vAxis': {'title':'Accumulated Rating'},
        'isStacked': True,
        'width': 900, 'height': 500
        }

        self.stepped_area_chart = SteppedAreaChart(name='SteppedDecline', 
            target_div='decline_stepped_area_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.stepped_area_chart])
        chart_hub.create_js_file('examples/stepped_area_chart.js')
        chart_hub.create_html_file('examples/stepped_area_chart.html')

    def test_gauge_chart(self):
        data = Data(
                columns_list=['Label', 'Value'],
                types_list=[Data.STRING, Data.NUMBER],
                values_list=[
                    ['Memory', 80],
                    ['CPU', 55],
                    ['Network', 68]
                ]
            )

        options = {
        'redFrom': 90, 'redTo': 100,
        'yellowFrom': 75, 'yellowTo': 90,
        'minorTicks': 5,
        'width': 400, 'height': 120
        }

        self.gauge_chart = GaugeChart(name='GaugeExample', 
            target_div='gauge_chart_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.gauge_chart])
        chart_hub.create_js_file('examples/gauge_chart.js')
        chart_hub.create_html_file('examples/gauge_chart.html')

    def test_geo_chart(self):
        data = Data(
                columns_list=['Country', 'Popularity'],
                types_list=[Data.STRING, Data.NUMBER],
                values_list=[
                    ['Germany', 200],
                    ['United States', 300],
                    ['Brazil', 400],
                    ['Canada', 500],
                    ['France', 600],
                    ['RU', 700]
                ]
            )

        options = {
        'width': 900, 'height': 500
        }

        self.geo_chart = GeoChart(name='GeoExample', 
            target_div='geo_chart_div', 
            data=data, chart_options=options)

        chart_hub = ChartHub(charts_list=[self.geo_chart])
        chart_hub.create_js_file('examples/geo_chart.js')
        chart_hub.create_html_file('examples/geo_chart.html')


if __name__ == '__main__':
    unittest.main()


        