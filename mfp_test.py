# using python 3.5.x
# pip install myfitnesspal
import myfitnesspal 
# pip install bokeh for all these
from bokeh.plotting import figure 
from bokeh.io import output_file, show
from bokeh.models import ColumnDataSource
from bokeh.core.properties import value

uname = input('enter username ')
pw = input('enter password ')
# username and password required, could be hashed for secrecy
client = myfitnesspal.Client(uname, pw)
# macros and colors to fill data with
macros = ['carbs', 'protein', 'fat']
colors = ['#c9d9d3', '#718dbf', '#e84d60']
# fill data with what you want to see
data = { 'days' : [], 'carbs' : [], 'protein': [], 'fat': [] }
# list of the last x days to count
x = [1, 2, 3, 4, 5, 6, 7]
# info placeholder getting the mfp data
info = {}
for day in x:
	# it really is this easy
	info[day] = client.get_date(2017, 12, (20-len(x))+day)
	print(info[day])
	data['days'].append(day)
	# just check the calories to make sure information is present
	if 'calories' in info[day].totals:
		data['carbs'].append(info[day].totals['carbohydrates'])
		data['protein'].append(info[day].totals['protein'])
		data['fat'].append(info[day].totals['fat'])
	else:
		# error case handling to keep the x and y sizes equal
		data['carbs'].append(0)
		data['protein'].append(0)
		data['fat'].append(0)

# set up the bokeh plot, stacked bar graph for now
source = ColumnDataSource(data=data)
p = figure(title='Macros Per Day', toolbar_location=None, tools="")
p.vbar_stack(macros, x='days', width=0.9, color=colors, source=source,legend=[value(m) for m in macros])
p.xgrid.grid_line_color=None
p.y_range.start=0
output_file("calories.html")
show(p)