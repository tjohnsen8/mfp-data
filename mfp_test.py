# using python 3.5.x
import random
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
# local file
from color_list import color_list

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
foods = {'breakfast': {}, 'lunch': {}, 'dinner': {}, 'snacks': {} }
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
		# create food list - types of food
		# create calorie list
		for food in meal.entries:
			if food.short_name == None:
				continue
			if not food.short_name in foods[meal.name]:
				foods[meal.name][food.short_name] = 1
			else: 
				foods[meal.name][food.short_name] += 1
			calorieList[food.name] = food.totals['calories']


# sort the foods by calories
sortedCalList = [(k, calorieList[k]) for k in sorted(calorieList, key=calorieList.get, reverse=True)]
for i in range(1, 15):
	print(sortedCalList[i])

p = figure(title='Macros Per Day')
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

# use the food list to create a pie chart of foods
pie_colors = []
pie_colors.append("red")
percents = []
percents.append(0)
foodLabels = []
# test with lunch
totalFoods = sum(foods['lunch'].values())
for name, num in foods['lunch'].items():
	print(name, ' ', num)
	foodLabels.append(name)
	pie_color = random.choice(color_list)
	while (pie_color in pie_colors): pie_color = random.choice(color_list)
	pie_colors.append(pie_color)
	# percent calculation
	perFood = num / totalFoods
	percents.append(percents[-1] + perFood)

print(foodLabels)
print(percents)
print(pie_colors)

starts = [p*2*math.pi for p in percents[:-1]]
ends = [p*2*math.pi for p in percents[1:]]
p2 = figure(title='Lunch foods', x_range=(-1,1), y_range=(-1,1))

source = ColumnDataSource(dict(
    st=starts,
    end=ends,
    color=pie_colors[:-1],
    label=foodLabels
))



p2.wedge(x=0, y=0, radius=1, start_angle='st', end_angle='end', color='color', legend='label', source=source)
output_file('pie.html')
show(p2)
