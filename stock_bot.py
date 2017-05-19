
from yahoo_finance import Share as sh
import operator
import urllib2
import time
from datetime import datetime, timedelta
from BeautifulSoup import BeautifulSoup as bs

#Global
growth_stocks 	= ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
value_stocks 	= ['ARW', 'COF', 'CI', 'FITB', 'USB']
ethical_stocks 	= ['WFM', 'SBUX', 'MSFT', 'SBUX', 'NSRGY']
quality_stocks 	= ['PORTX', 'ENS', 'EME', 'CVG', 'AXP']
index_stocks 	= ['IXUS', 'VTI', 'ILTB', 'VTSMX', 'VXUS']

portfolio = {}
dictionary_strategies = {
	'growth' 	: growth_stocks,
	'value'		: value_stocks,
	'ethical'	: ethical_stocks,
	'quality'	: quality_stocks,
	'index'		: index_stocks
}
uninvested_amount = 0
is_stock_drawn = False
global_stock_index = {}
is_ratio_method_over = False
older_portfolio = {}
older_global_stock_index = {}
five_day_data = {}
cached_portfolio = {}
last_amount = 0
last_strategy = ''
never_calculated = True

def reset():
	global global_stock_index, portfolio, is_stock_drawn, is_ratio_method_over, uninvested_amount
	global_stock_index = {}
	portfolio = {}
	is_stock_drawn = False
	is_ratio_method_over = False
	uninvested_amount = 0


def get_eligible_stock(stock_dictionary, amount):
	sorted_stocks_by_peg = sorted(stock_dictionary.items(), key=operator.itemgetter(1), reverse=True)
	for each_element in sorted_stocks_by_peg:
		stock_symbol = each_element[0]
		stock_details = each_element[1]
		stock_price = stock_details['price']
		if stock_price < amount:
			return stock_symbol

def cache_stocks(stock_type):
	for each_stock in stock_type:
		try:
			stock = sh(each_stock)
			global_stock_index[each_stock] = stock
			date_now = datetime.now().date()
			date_five_before = (datetime.now() - timedelta(days=10)).date()
			#five_day_data[each_stock] = stock.get_historical(str(date_five_before), str(date_now))
			five_day_data[each_stock] = get_custom_historical_data(each_stock)
			#five_day_data[each_stock] = five_day_data[each_stock][:5]
		except urllib2.HTTPError:
			print "Server error (Cache) - Retrying"
			return False
	return True

def get_custom_historical_data(name):
	base_url_1 = "https://finance.yahoo.com/quote/" 
	base_url_2 = "/history/"

	url = base_url_1 + name + base_url_2

	response = urllib2.urlopen(url)
	html = response.read()

	soup = bs(html)
	table = soup.findAll('table')

	rows = table[1].tbody.findAll('tr')

	five_day_data = []
	for each_row in rows:
		d = {} 
		divs = each_row.findAll('td')
		date_div = divs[0].span.text
		close_text = divs[1].span.text
		if close_text == 'Dividend':
			continue
		price_close = float(close_text)
		d['Date'] = date_div
		d['Close'] = price_close
		five_day_data.append(d)

	return five_day_data[:5]



def get_portfolio(amount, stock_type, strategy):
	global portfolio, uninvested_amount, is_stock_drawn, global_stock_index, is_ratio_method_over

	sum_peg = 0
	total_balance = 0
	stock_dictionary = {}
	index = 0

	for each_stock in stock_type:
		internal_dictionary = {}
		stock = global_stock_index[each_stock]

		price = float(stock.get_price())

		if(price > amount):
			continue

		internal_dictionary['price'] = float(price)
		individual_peg = float(stock.get_price_earnings_growth_ratio())
		if individual_peg == 0:
			individual_peg = 1
		internal_dictionary['peg'] = abs(individual_peg)
		internal_dictionary['name'] = stock.get_name()
		internal_dictionary['index'] = index
		internal_dictionary['five_day_data'] = five_day_data[each_stock]
		internal_dictionary['strategy'] = strategy
		index = index + 1
		#calculate sum here for later on
		sum_peg += internal_dictionary['peg']
		stock_dictionary[each_stock] = internal_dictionary


	if is_ratio_method_over == False:
		for each_stock in stock_dictionary.keys():
			each_stock_price = float(stock_dictionary[each_stock]['price'])
			each_stock_peg = stock_dictionary[each_stock]['peg']
			each_stock_ratio = float(each_stock_peg)/sum_peg	
			each_stock_amount = float(amount * each_stock_ratio)
			
			each_stock_count = int(each_stock_amount/each_stock_price)
			total_balance += (each_stock_amount % each_stock_price)

			stock_dictionary[each_stock]['ratio'] = each_stock_ratio
			stock_dictionary[each_stock]['amount'] = each_stock_amount
			stock_dictionary[each_stock]['count'] = each_stock_count

			#if dictionary was already there
			if bool(portfolio) == True:
				portfolio[each_stock]['count'] += each_stock_count
				portfolio[each_stock]['amount'] += each_stock_amount


	#check if ratio method won't work:
	if total_balance >= amount:
		is_ratio_method_over = True
		stock_symbol = get_eligible_stock(stock_dictionary, amount)
		stock_price = stock_dictionary[stock_symbol]['price']
		extra_stocks = int(total_balance / stock_price)
		amount_spent = extra_stocks * stock_price
		total_balance = total_balance - amount
		portfolio[stock_symbol]['count'] += extra_stocks
		portfolio[stock_symbol]['amount'] += amount_spent
		return total_balance

	if total_balance == 0:
		uninvested_amount =  amount
		return 0

	#if dictionary was empty
	if bool(portfolio) == False:
		portfolio = stock_dictionary.copy()

	return total_balance

def get_live_portfolio_value():
	live_portfolio_value = 0
	if bool(portfolio) == False:
		if never_calculated is False:
			cached_portfolio = get_portfolio(last_amount, last_strategy, ex='single')
		else:
			return 0
	else:
		cached_portfolio = portfolio.copy()

	for stock, details in cached_portfolio.items():
		live_portfolio_value += details['count'] * details['price']
	return live_portfolio_value

def execute(amount, strategy, ex):
	global portfolio, dictionary_strategies, older_portfolio
	global global_stock_index, older_global_stock_index
	
	global last_strategy, last_amount
	last_amount = amount
	last_strategy = strategy

	balance = amount

	stock_type = dictionary_strategies[strategy]
	ret = False
	while ret != True:
		ret = cache_stocks(stock_type)

	while balance > 0:
		balance = get_portfolio(balance, stock_type, strategy)

	if ex == 'double_1':
		older_portfolio = {}
		older_global_stock_index = {} 
		older_portfolio = portfolio.copy()
		older_global_stock_index = global_stock_index.copy()
	elif ex == 'double_2':
		portfolio = dict( portfolio.items() + older_portfolio.items() )
		global_stock_index =  dict(older_global_stock_index.items() + global_stock_index.items())

	never_calculated = False
	return portfolio

	