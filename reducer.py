#!/usr/bin/python
import sys
import csv

reader = csv.reader(sys.stdin, delimiter=',')
writer = csv.writer(sys.stdout, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

def outputCount(oldKey,countTotal):
    output = []
    output.append(oldKey)
    output.append(countTotal)
    writer.writerow(output)

countTotal = 0
oldKey = None

for data in reader:
    if len(data) != 2:
        # Something has gone wrong. Skip this line.
        continue

    thisKey = data[0]
    if oldKey and oldKey != thisKey:
        outputCount(oldKey,countTotal)
        oldKey = thisKey
        countTotal = 0

    oldKey = thisKey
    countTotal += 1

if oldKey != None:
    outputCount(oldKey,countTotal)