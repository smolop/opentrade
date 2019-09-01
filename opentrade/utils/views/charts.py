from random import randint
from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView
from opentrade.utils.functions import shares as f_shares
import json 

class LineChartJSONView(BaseLineChartView):

    
    def dispatch(self, request, *args, **kwargs):
        self.symbol = kwargs.get('symbol', "any_default")
        print("###SYMBOL DISPATCH")
        print(self.symbol)
        self.dates, self.closed_prices = f_shares.get_dates_to_chart(self.symbol)
        return super(BaseLineChartView, self).dispatch(request, *args, **kwargs)
        
        
    def get(self, request, *args, **kwargs):
        print("######GET")
        response = super(LineChartJSONView, self).get(self, request, *args, **kwargs)
        user = request.user
        self.symbol = kwargs['symbol']
        self.dates, self.closed_prices = f_shares.get_dates_to_chart(self.symbol)
        print(self.symbol)
        return response    

    def get_labels(self):
        print("######LABEL")
        """ example: ['January', 'February']"""
        return self.dates

    def get_providers(self):
        print("######PROVIDER")
        """Return names of datasets."""
        return [self.symbol, ]

    def get_data(self):
        print("######DATA")
        return [ self.closed_prices, ]

    


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()