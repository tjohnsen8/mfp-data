# using python 3.5.x
import math
import time
from datetime import date
from datetime import timedelta
# pip install myfitnesspal
import myfitnesspal 
# pip install bokeh for all these
from bokeh.plotting import figure 
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource, Span
from bokeh.core.properties import value


uname = input('enter username ')
pw = input('enter password ')
numDays = int(input('enter number of days to look at '))
# username and password required, could be hashed for secrecy
# list of the last x days to count
#numDays = 90
client = myfitnesspal.Client(uname, pw)

# macros and colors to fill data with
macros = ['carbs', 'protein', 'fat']
colors = ['#c9d9d3', '#718dbf', '#e84d60']
# fill data with what you want to see
data = { 'days' : [], 'carbs' : [], 'protein': [], 'fat': [] }

x = list(range(1, numDays+1))
x.reverse()
# info placeholder getting the mfp data
info = {}
today = date.today()
goals = client.get_date(today).goals
calorieList = {}
for day in x:
	# it really is this easy
	# for a month need to be smarter
	# start at the earliest day
	dayToEval = today - timedelta(days=day)
	info[day] = client.get_date(dayToEval.year, dayToEval.month, dayToEval.day)
	print(info[day])
	# just check the calories to make sure information is present
	data['days'].append(day)
	if 'calories' in info[day].totals:
		data['carbs'].append(info[day].totals['carbohydrates'])
		data['protein'].append(info[day].totals['protein'])
		data['fat'].append(info[day].totals['fat'])
	else:
		# error case handling to keep the x and y sizes equal
		data['carbs'].append(math.nan)
		data['protein'].append(math.nan)
		data['fat'].append(math.nan)

	# look for calories per item
	for meal in info[day].meals:
		for food in meal.entries:
			calorieList[food.name] = food.totals['calories']

# sort the foods by calories
sortedCalList = [(k, calorieList[k]) for k in sorted(calorieList, key=calorieList.get, reverse=True)]
for i in range(1, 15):
	print(sortedCalList[i])

# set up the bokeh plot, stacked bar graph for now
#source = ColumnDataSource(data=data)
p = figure(title='Macros Per Day')
#p.vbar_stack(macros, x='days', width=0.9, color=colors, source=source,legend=[value(m) for m in macros])
#p.xgrid.grid_line_color=None
p.multi_line([data['days'], data['days'], data['days']], [data['carbs'], data['protein'], data['fat']], 
	line_color=colors, line_width=4)
# create three lines with the goals
carbGoal = Span(location=goals['carbohydrates'], dimension='width', line_color=colors[0], line_dash='dashed', line_width=3)
proteinGoal = Span(location=goals['protein'], dimension='width', line_color=colors[1], line_dash='dashed', line_width=3)
fatGoal = Span(location=goals['fat'], dimension='width', line_color=colors[2], line_dash='dashed', line_width=3)
p.add_layout(carbGoal)
p.add_layout(proteinGoal)
p.add_layout(fatGoal)
output_file("calories.html")
show(p)