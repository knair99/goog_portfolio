from flask import Flask
from flask import request
from flask import render_template
from flask import abort
from flask import jsonify

import lookup as lk
import json
import stock_bot as sb

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
	data = request.data
	sb.clear_everything()
	
	if not request.form['total_amount']:
		abort(400, 'Enter a valid amount, greater than 5000!')
	else:
		total_amount = float(request.form['total_amount'])
		if total_amount < 5000:
			abort(400, 'Enter a valid amount, greater than 5000!')


	if request.form['strategy_1'] == 'None':
		abort(400, 'Please choose atleast one valid strategy')

	strategy_1 = request.form['strategy_1']


	if request.form['strategy_2'] == 'None':
			portfolio = sb.execute(total_amount, strategy_1.lower(), ex='single')
	else:
		strategy_2 = request.form['strategy_2']
		portfolio = sb.execute(total_amount/2, strategy_1.lower(), ex='double_1')
		sb.clear_everything()
		portfolio = sb.execute(total_amount/2, strategy_2.lower(), ex='double_2')


	# ticker_symbol = request.form["stock_symbol"]
	# stock_dict = lk.pull_stock(ticker_symbol)	
	web_response = {}
	web_response['code'] = 0
	web_response['portfolio'] = json.dumps(portfolio)
	#json_values = json.dumps(web_response)
	return jsonify(web_response)
 	
if __name__ == "__main__":
    app.run()