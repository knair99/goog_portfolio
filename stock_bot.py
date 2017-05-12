
from yahoo_finance import Share as sh
import operator
import urllib2
import lookup
import time
from datetime import datetime, timedelta

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

def clear_everything():
	global global_stock_index, portfolio, is_stock_drawn, is_ratio_method_over, uninvested_amount
	global_stock_index = {}
	portfolio = {}
	is_stock_drawn = False
	is_ratio_method_over = False
	uninvested_amount = 0
	#lookup.clear_everything()
	#execute clean script here


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
			five_day_data[each_stock] = stock.get_historical(str(date_five_before), str(date_now))
			five_day_data[each_stock] = five_day_data[each_stock][:5]
		except urllib2.HTTPError:
			print "Server error (Cache) - Retrying"
			return False
	return True

def generate_five_day():
	for symbol, each in global_stock_index.items():
		success = False
		while not success:
			success = lookup.draw_stock(each, portfolio[symbol]['index'])
			#repeat for http errors

	lookup.draw_portfolio(portfolio)

def get_portfolio(amount, stock_type):
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

	#get new stocks with highest peg AND < price

	#if dictionary was empty
	if bool(portfolio) == False:
		#print 'updating once'
		portfolio = stock_dictionary.copy()

	return total_balance


def run_diagnostics():
	sum_stocks = 0
	sum_portfolio_counts = 0 
	for each in portfolio:
		print portfolio[each], '-- amount ->', portfolio[each]['amount']
		sum_stocks += portfolio[each]['amount']
		print portfolio[each], 'count ', portfolio[each]['count'], 'price', portfolio[each]['price']
		print 'for a total of ', portfolio[each]['count'] * portfolio[each]['price']
		sum_portfolio_counts += portfolio[each]['count'] * portfolio[each]['price']
		print "***" * 3
	print "Total spent: ", sum_portfolio_counts
	print "total allocated:", sum_stocks


def execute(amount, strategy, ex):
	global portfolio, dictionary_strategies, older_portfolio
	global global_stock_index, older_global_stock_index
	balance = amount

	stock_type = dictionary_strategies[strategy]
	ret = False
	while ret != True:
		ret = cache_stocks(stock_type)

	while balance > 0:
		balance = get_portfolio(balance, stock_type)
		#run_diagnostics()


	#plot five day historical data for new stocks
	if ex == 'double_1':
		print 'Round 1'
		older_portfolio = {}
		older_global_stock_index = {} 
		older_portfolio = portfolio.copy()
		older_global_stock_index = global_stock_index.copy()
		print older_portfolio
	elif ex == 'double_2':
		print 'round 2'
		portfolio = dict( portfolio.items() + older_portfolio.items() )
		global_stock_index =  dict(older_global_stock_index.items() + global_stock_index.items())
		print portfolio

	#generate_five_day()
	
	return portfolio

	