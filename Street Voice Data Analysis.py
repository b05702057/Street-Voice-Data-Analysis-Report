import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import datetime
import matplotlib.pyplot as plt

def regression(x,y):
	n = len(x)
	average_x = sum(x) / n
	average_y = sum(y) / n
	up = 0
	down = 0
	for i in range(n):
		up += (x[i] - average_x) * (y[i] - average_y)
		down += (x[i] - average_x) ** 2
	b = up / down
	a = average_y - (b * average_x)
	return a, b

fn1 = 'C:\\Users\\lanpa\\Desktop\\result.csv'
fh1 = open(fn1, 'r', newline = '', encoding = 'utf-8')
csv1 = csv.DictReader(fh1)
cname1 = csv1.fieldnames

followers_data = {}
song_data = {}
like_data = {}
data_data = {}
prize_record = {}
date_data = {}

for aline in csv1:
	if(aline[cname1[2]] == 'ERROR'):
		continue
	elif(aline[cname1[3]] == 'ERROR'):
		continue
	elif(aline[cname1[4]] == 'ERROR'):
		continue
	elif(aline[cname1[5]] == 'ERROR'):
		continue
	elif(aline[cname1[6]] == 'ERROR'):
		continue
	elif(aline[cname1[7]] == 'ERROR'):
		continue
	else:
		aline[cname1[7]] = datetime.datetime.strptime(aline[cname1[7]], "%Y 年 %m 月 %d 日")
		followers_data[aline[cname1[1]]] = aline[cname1[2]]
		song_data[aline[cname1[1]]] = aline[cname1[3]]
		like_data[aline[cname1[1]]] = aline[cname1[4]]
		data_data[aline[cname1[1]]] = aline[cname1[5]]
		prize_record[aline[cname1[1]]] = aline[cname1[6]]
		date_data[aline[cname1[1]]] = aline[cname1[7]]

temp = []
for i in followers_data:
	temp.append(int(followers_data[i]))
temp = np.asarray(temp)
iqr = np.percentile(temp, 75) - np.percentile(temp, 25)
del_list = []
for i in followers_data:
	if(int(followers_data[i]) < int(np.percentile(temp, 25)) - 1.5 * iqr or int(followers_data[i]) > int(np.percentile(temp, 75)) + 1.5 * iqr):
		del_list.append(i)

plt.figure(figsize=(10,25))

x = []
y = []
for i in followers_data:
	delta = datetime.datetime.now() - date_data[i]
	year = delta.days / 365
	x.append(int(song_data[i]) / year)
	y.append(int(followers_data[i]))
a,b = regression(x,y)
x1 = []
y1 = []
summ = 0
for i in range(len(x)):
	summ += x[i]
avey = (summ / len(x)) * b + a
ssr = 0
sst = 0
for i in range(len(x)):
	x1.append(x[i])
	y1.append(x[i] * b + a)
	ssr += (y1[i] - avey) ** 2
	sst += (y[i] - avey) ** 2
print('SSR:%-20.3f' %float(ssr), 'SST:%-20.3f' %float(sst),'判定係數:%.3f' %float(ssr/sst))
plt.subplot(1,5,1)
plt.plot(x1,y1, color='r')
plt.scatter(x,y, marker = '.')
plt.title("Relationship between Followers & Song per year")
plt.xlabel("Song per year")
plt.ylabel("Followers")

x = []
y = []
for i in followers_data:
	x.append(int(prize_record[i]))
	y.append(int(followers_data[i]))
a,b = regression(x,y)
x1 = []
y1 = []
summ = 0
for i in range(len(x)):
	summ += x[i]
avey = (summ / len(x)) * b + a
ssr = 0
sst = 0
for i in range(len(x)):
	x1.append(x[i])
	y1.append(x[i] * b + a)
	ssr += (y1[i] - avey) ** 2
	sst += (y[i] - avey) ** 2
print('SSR:%-20.3f' %float(ssr), 'SST:%-20.3f' %float(sst),'判定係數:%.3f' %float(ssr/sst))
plt.subplot(1,5,3)
plt.plot(x1,y1, color='r')
plt.scatter(x,y, marker = '.')
plt.title("Relationship between Followers & Prize")
plt.xlabel("Prize")
plt.ylabel("Followers")

x = []
y = []
for i in like_data:
	x.append(int(like_data[i]) / int(song_data[i]))
	y.append(int(followers_data[i]))
a,b = regression(x,y)
x1 = []
y1 = []
summ = 0
for i in range(len(x)):
	summ += x[i]
avey = (summ / len(x)) * b + a
ssr = 0
sst = 0
for i in range(len(x)):
	x1.append(x[i])
	y1.append(x[i] * b + a)
	ssr += (y1[i] - avey) ** 2
	sst += (y[i] - avey) ** 2
print('SSR:%-20.3f' %float(ssr), 'SST:%-20.3f' %float(sst),'判定係數:%.3f' %float(ssr/sst))
plt.subplot(1,5,5)
plt.plot(x1,y1, color='r')
plt.scatter(x,y, marker = '.')
plt.title("Relationship between Followers & Average likes")
plt.xlabel("Average likes")
plt.ylabel("Followers")
plt.show()
plt.figure(figsize=(10,25))

x = []
y = []
for i in followers_data:
	if(i in del_list):
		continue
	delta = datetime.datetime.now() - date_data[i]
	year = delta.days / 365
	x.append(int(song_data[i]) / year)
	y.append(int(followers_data[i]))
a,b = regression(x,y)
x1 = []
y1 = []
summ = 0
for i in range(len(x)):
	summ += x[i]
avey = (summ / len(x)) * b + a
ssr = 0
sst = 0
for i in range(len(x)):
	x1.append(x[i])
	y1.append(x[i] * b + a)
	ssr += (y1[i] - avey) ** 2
	sst += (y[i] - avey) ** 2
print('SSR:%-20.3f' %float(ssr), 'SST:%-20.3f' %float(sst),'判定係數:%.3f' %float(ssr/sst))
plt.subplot(1,5,1)
plt.plot(x1,y1, color='r')
plt.scatter(x,y, marker = '.')
plt.title("Relationship between Followers & Song per year")
plt.xlabel("Song per year")
plt.ylabel("Followers")

x = []
y = []
for i in followers_data:
	if(i in del_list):
		continue
	x.append(int(prize_record[i]))
	y.append(int(followers_data[i]))
a,b = regression(x,y)
x1 = []
y1 = []
summ = 0
for i in range(len(x)):
	summ += x[i]
avey = (summ / len(x)) * b + a
ssr = 0
sst = 0
for i in range(len(x)):
	x1.append(x[i])
	y1.append(x[i] * b + a)
	ssr += (y1[i] - avey) ** 2
	sst += (y[i] - avey) ** 2
print('SSR:%-20.3f' %float(ssr), 'SST:%-20.3f' %float(sst),'判定係數:%.3f' %float(ssr/sst))
plt.subplot(1,5,3)
plt.plot(x1,y1, color='r')
plt.scatter(x,y, marker = '.')
plt.title("Relationship between Followers & Prize")
plt.xlabel("Prize")
plt.ylabel("Followers")

x = []
y = []
for i in like_data:
	if(i in del_list):
		continue
	x.append(int(like_data[i]) / int(song_data[i]))
	y.append(int(followers_data[i]))
a,b = regression(x,y)
x1 = []
y1 = []
summ = 0
for i in range(len(x)):
	summ += x[i]
avey = (summ / len(x)) * b + a
ssr = 0
sst = 0
for i in range(len(x)):
	x1.append(x[i])
	y1.append(x[i] * b + a)
	ssr += (y1[i] - avey) ** 2
	sst += (y[i] - avey) ** 2
print('SSR:%-20.3f' %float(ssr), 'SST:%-20.3f' %float(sst),'判定係數:%.3f' %float(ssr/sst))
plt.subplot(1,5,5)
plt.plot(x1,y1, color='r')
plt.scatter(x,y, marker = '.')
plt.title("Relationship between Followers & Average likes")
plt.xlabel("Average likes")
plt.ylabel("Followers")
plt.show()

X = []
y = []
for i in like_data :
	a = int(data_data[i])
	b = int(like_data[i])
	if(b == 0):
		continue
	c = int(prize_record[i])
	temp = []
	temp.append(a/b)
	temp.append(c)
	X.append(temp)
	y.append(c)
avey = float(sum(y) / len(y))
X = np.asarray(X)
y = np.asarray(y)

lm = LinearRegression()
lm.fit(X, y)

x1 = []
x2 = []
for i in range(len(X)):
	x1.append(X[i][0])
	x2.append(X[i][1])

fig = plt.figure(figsize=(10,25))
ax = Axes3D(fig)
ax.scatter(x1,x2,y, marker = '.')
plt.show()

X = []
y = []
for i in like_data :
	if(i in del_list):
		continue
	a = int(data_data[i])
	b = int(like_data[i])
	if(b == 0):
		continue
	c = int(prize_record[i])
	temp = []
	temp.append(a/b)
	temp.append(c)
	X.append(temp)
	y.append(c)
avey = float(sum(y) / len(y))
X = np.asarray(X)
y = np.asarray(y)

lm = LinearRegression()
lm.fit(X, y)

x1 = []
x2 = []
for i in range(len(X)):
	x1.append(X[i][0])
	x2.append(X[i][1])

fig = plt.figure(figsize=(10,25))
ax = Axes3D(fig)
ax.scatter(x1,x2,y, marker = '.')
plt.show()



