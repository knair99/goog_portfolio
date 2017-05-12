from yahoo_finance import Share 
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties

dict_stock_to_five_day_prices = {}
portfolio_dates = []

def clear_everything():
	global dict_stock_to_five_day_prices, portfolio_dates
	dict_stock_to_five_day_prices = {}
	portfolio_history_list = []
	portfolio_dates = []

def draw_stock(stock, index):
	global dict_stock_to_five_day_prices, portfolio_dates
	stock_dictionary = {}
	#Plot five day data
	date_now = datetime.now().date()
	date_five_before = (datetime.now() - timedelta(days=10)).date()
	
	try:
		five_day_data = stock.get_historical(str(date_five_before), str(date_now))
	except:
		print 'Server error (History) - Retrying'
		return False

	five_day_data = five_day_data[:5]

	list_dates = []
	list_prices = []

	for each in five_day_data:
		list_dates.append(each['Date'])
		list_prices.append(each['Close'])

	dict_stock_to_five_day_prices[each['Symbol']] = list_prices[:]
	portfolio_dates = list_dates


	x = [datetime.strptime(d,'%Y-%m-%d').date() for d in list_dates]
	y = list_prices
	ax = plt.subplot(111)
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	p, = plt.plot(x,y, label=stock.get_name())
	plt.gcf().autofmt_xdate()
	fontP = FontProperties()
	fontP.set_size('small')
	ax.legend(loc='upper center', bbox_to_anchor=(1,1), ncol=1, fancybox=True, shadow=True, prop=fontP)
	plt.savefig('static/stocks.png')
	return True

def draw_portfolio(portfolio):
	global dict_stock_to_five_day_prices, portfolio_dates

	# print dict_stock_to_five_day_prices
	# print "*" * 80

	for each_stock, five_day_prices in dict_stock_to_five_day_prices.items():
		count = portfolio[each_stock]['count']
		count_five_day_prices = [count * float(x) for x in five_day_prices] 
		dict_stock_to_five_day_prices[each_stock] = count_five_day_prices

	# print dict_stock_to_five_day_prices

	list_prices = [0,0,0,0,0]
	for each in dict_stock_to_five_day_prices.values():
		for index in range(0, 5):
			list_prices[index] += int(each[index])
		
	# print list_prices

	x = [datetime.strptime(d,'%Y-%m-%d').date() for d in portfolio_dates]
	y = list_prices
	plt.clf() 
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator())
	plt.plot(x,y, label='portfolio')
	plt.gcf().autofmt_xdate()
	ax = plt.subplot(111)
	ax.legend(loc='upper center', bbox_to_anchor=(1,1), ncol=1, fancybox=True, shadow=True)

	plt.savefig('static/portfolio.png')
	plt.clf() 





