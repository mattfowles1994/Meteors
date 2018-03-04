import sqlite3
import time
import zlib

conn = sqlite3.connect('meteors.sqlite')
cur = conn.cursor()

# Pulls necessary tables together for required information

cur.execute('SELECT id, Year FROM Year')
year = dict()
for meteor_row in cur :
    year[meteor_row[0]] = meteor_row[1]

meteorpoints = dict()

cur.execute('SELECT Meteorites.Name,Year.Year FROM Meteorites JOIN Year ON Meteorites.Year_id = Year.id')

count = 0
year = list()

for meteor_row in cur:
    meteor = meteor_row[1]
    # skips meteor if year not knowm
    if meteor == 'NO DATA' : continue
    year.append(int(meteor))
    for item in year:
        count = count+1
        if count > 100000 : break
        if item not in meteorpoints:
            meteorpoints[item] = 1
        else:
            meteorpoints[item] = meteorpoints[item] +1

# Creates Javascript file of data points

points = list()
years = list()
counts = list()

for key in meteorpoints:
    counts.append(meteorpoints[key])
    years.append(key)

points.append(years)
points.append(counts)
for data in points:
    print(data)

years.sort()

fhand = open('gline.js','w')
fhand.write("gline = [ ['Years', 'Meteors'],\n")


for index, count in enumerate(counts):
    fhand.write("[")
    fhand.write("'"+str(years[index])+"'")
    fhand.write(","+str(counts[index]))
    fhand.write("]")
    if len(counts) - 1 != index:
        fhand.write(",")
    else: continue
    fhand.write("\n")


print(len(years))
fhand.write("\n];\n")
fhand.close()

