
# from yahoo_finance import Share as sh
# from pprint import pprint

# st = sh ('NFLX')
# pprint (st.get_historical('2017-05-01', '2017-05-12'))

import urllib2
from BeautifulSoup import BeautifulSoup as bs

growth_stocks 	= ['AAPL', 'FB', 'VMW', 'NFLX', 'AMZN']
value_stocks 	= ['ARW', 'COF', 'CI', 'FITB', 'USB']
ethical_stocks 	= ['WFM', 'SBUX', 'MSFT', 'SBUX', 'NSRGY']
quality_stocks 	= ['PORTX', 'ENS', 'EME', 'CVG', 'AXP']
index_stocks 	= ['IXUS', 'VTI', 'ILTB', 'VTSMX', 'VXUS']


base_url_1 = "https://finance.yahoo.com/quote/" 
base_url_2 = "/history/"

url = base_url_1 + 'COF' + base_url_2

response = urllib2.urlopen(url)
html = response.read()

soup = bs(html)
table = soup.findAll('table')

rows = table[1].tbody.findAll('tr')

for each_row in rows:
	divs = each_row.findAll('td')
	
	date_div = divs[0].span.text
	close_text = divs[1].span.text
	if close_text == 'Dividend':
		continue
	price_close = float(close_text)

	print date_div, price_close
