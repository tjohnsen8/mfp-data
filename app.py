from flask import Flask, render_template, request, session, send_from_directory
import os
import myfitnesspal
from mfp_tom import make_chart

application = Flask(__name__)

@application.route('/')
def showMain():
	return render_template("main.html")

@application.route('/login', methods=['POST'])
def loginAndCalculate():
	# print(request.form['username'])
	
	try:
		client = myfitnesspal.Client(request.form['username'], request.form['password'])
	except ValueError:
		return showMain()

	session['logged_in'] = True
	numDays = 7
	make_chart(client, numDays)
	session['chart_made'] = True
	return showChart()

@application.route('/chart')
def showChart():
	return send_from_directory('.', 'calories.html')

if __name__ == '__main__':
	application.secret_key = os.urandom(12)
	application.run(host='0.0.0.0')