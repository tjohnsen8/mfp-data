from datetime import datetime, date, time, timedelta
from gmail import GMail, Message
import myfitnesspal
import math
import matplotlib.pyplot as plt
import pandas as pd

uname = ''
pw = ''
today = date.today()

client = myfitnesspal.Client(uname, pw)

todays_mfp = client.get_date(today).totals
goals = client.get_date(today).goals

email_str  = f"Ivis stats for {today}\n"
email_str += f"Cals {todays_mfp['calories']}/{goals['calories']}\n"
email_str += f"Carbs {todays_mfp['carbohydrates']}/{goals['carbohydrates']}\n"
email_str += f"Protein {todays_mfp['protein']}/{goals['protein']}\n"
email_str += f"Fat {todays_mfp['fat']}/{goals['fat']}\n"
print(email_str)

start_day = date(2019,2,19)
numDays = (today - start_day).days + 1
date_list = [today - timedelta(days=x) for x in range(0, numDays)]
date_list.reverse()
cals = []
colors = []
for day in date_list:
	stats = client.get_date(day.year, day.month, day.day)
	# want to plot the calories from day to day
	if 'calories' in stats.totals:
		diff = stats.totals['calories'] - goals['calories']
		if diff > 0:
			colors.append('r')
		else:
			colors.append('g')
		cals.append(diff)
	else:
		cals.append(0)

xlabels = [f'{date}' for date in date_list]
index = range(0, numDays)
s = pd.Series(cals, index=xlabels)
plt.xlabel('Date')
plt.ylabel('Calories')
plt.xticks(index, xlabels, rotation=30)
plt.title("Calories over Time since 2/19/19")
s.plot(kind='bar', color=colors)
plt.savefig('calories.png')

gmail = GMail('Me <t.johnsen8@gmail.com>', '')
msg = Message('MFP Stats', to='<t.johnsen8@gmail.com>', text=email_str, attachments=['calories.png'])
gmail.send(msg)
