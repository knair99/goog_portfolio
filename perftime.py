
from yahoo_finance import Share as sh
import operator
import urllib2
import time
from datetime import datetime, timedelta


growth_stocks 	= ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
value_stocks 	= ['ARW', 'COF', 'CI', 'FITB', 'USB']
ethical_stocks 	= ['WFM', 'SBUX', 'MSFT', 'SBUX', 'NSRGY']
quality_stocks 	= ['PORTX', 'ENS', 'EME', 'CVG', 'AXP']
index_stocks 	= ['IXUS', 'VTI', 'ILTB', 'VTSMX', 'VXUS']


dictionary_strategies = {
	'growth' 	: growth_stocks,
	'value'		: value_stocks,
	'ethical'	: ethical_stocks,
	'quality'	: quality_stocks,
	'index'		: index_stocks
}

five_day_data = {}


def cache_stocks(stock_type):
	for each_stock in stock_type:
		try:
			stock = sh(each_stock)
			price = stock.get_price()
			# date_now = datetime.now().date()
			# date_five_before = (datetime.now() - timedelta(days=10)).date()
			# five_day_data[each_stock] = stock.get_historical(str(date_five_before), str(date_now))
			# five_day_data[each_stock] = five_day_data[each_stock][:5]
		except urllib2.HTTPError:
			print "Server error (Cache) - Retrying"
			return False
	return True



strategy = 'growth'
stock_type = dictionary_strategies[strategy]
cache_stocks(stock_type)