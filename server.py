from flask import Flask
from flask import request
from flask import render_template
from flask import abort
from flask import jsonify
import json
import stock_bot as sb
import urllib2


app = Flask(__name__)

@app.errorhandler(400)
def custom400(error):
    response = jsonify({'message': error.description,
    	'code': 400})
    return response

 
@app.route("/")
def enter():
	return render_template('index.html')	

@app.route("/calculate", methods=["POST"])
def runn():
	try:
		urllib2.urlopen('http://216.58.192.142', timeout=1)
	except urllib2.URLError as err:
		abort(400, 'No internet connection!')

	data = request.data
	sb.reset()
	
	if not request.form['total_amount']:
		abort(400, 'Enter a valid amount, greater than 5000!')
	else:
		try:
			total_amount = float(request.form['total_amount'])
		except ValueError:
			abort(400, 'Please enter a valid numerical amount')
		if total_amount < 5000:
			abort(400, 'Enter a valid amount, greater than 5000!')


	if request.form['strategy_1'] == 'None':
		abort(400, 'Primary investment strategy cannot be blank. Please choose a strategy')

	strategy_1 = request.form['strategy_1']

	if request.form['strategy_2'] == 'None':
			portfolio = sb.execute(total_amount, strategy_1.lower(), ex='single')
	else:
		strategy_2 = request.form['strategy_2']
		portfolio = sb.execute(total_amount/2, strategy_1.lower(), ex='double_1')
		sb.reset()
		portfolio = sb.execute(total_amount/2, strategy_2.lower(), ex='double_2')


	web_response = {}
	web_response['code'] = 0
	web_response['portfolio'] = json.dumps(portfolio)
	return jsonify(web_response)


@app.route('/live_value', methods= ['GET'])
def get_live():
    live_portfolio_value = sb.get_live_portfolio_value()
    return jsonify(live_value=live_portfolio_value)
 	
 	
if __name__ == "__main__":
    app.run()