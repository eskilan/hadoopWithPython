#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 18:18:00 2018

@author: ilan
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re

mrDF = pd.read_csv('hadoopOutput1.csv',header=None,  names = ['BibNum','nCheckouts']).set_index('BibNum') # 321772 rows
libRefDF = pd.read_csv('Library_Collection_Inventory.csv').set_index('BibNum') # ~2.6 million rows
libRefDF = libRefDF[['Title','Author','ISBN','PublicationYear']].drop_duplicates()
# cross reference column1 from mrDF with BibNum of libRefDF
n = 100
topN = mrDF.nlargest(n, 'nCheckouts')

results = topN.join(libRefDF,how='inner').sort_values(by=['nCheckouts'], ascending=False)

splitTitle = results.Title.str.split('/')
pattern = re.compile('\[.*\]')
results['Title_1'] = splitTitle.str[0].str.replace(pattern,'')
results['Title_2'] = splitTitle.str[1]

def selectEarliestYear(myList):
    numericList = []
    for item in myList:
        if item.isnumeric():
            numericList.append(int(item))
    if len(numericList) > 0:
        return min(numericList)
    else:
        return np.nan

# let's clean up the publication year from libRefDF and results
def cleanYear(df):
    mySeries = df['PublicationYear'].str.split(',|\.|\[|\]|-|c|©')
    mySeries = mySeries.apply(selectEarliestYear)
    return mySeries

## Now we can compare the distribution of publication years between the overall library and our most checked out items
resultsYear = cleanYear(results)
overallYear = cleanYear(libRefDF.dropna().head(1000))

f, (ax1, ax2) = plt.subplots(1,2)

g1 = sns.distplot(resultsYear.dropna(),norm_hist=True, ax=ax1)
g2 = sns.distplot(overallYear.dropna(),norm_hist=True, ax=ax2)
g1.set(xlim=(1970,2017))
g2.set(xlim=(1970,2017))
g1.set_title('Top 100 most popular items')
g2.set_title('Sample of items in collection')

print(results[['nCheckouts','Title_1','Title_2']].head(20))
#libRefDF.PublicationYear = cleanYear(libRefDF)
#
#films = results[results['Title'].str.contains('videorecording'|'Films'|'Film')]
#other = results[~results['Title'].str.contains('videorecording')]
#nFilms = films.shape[0]
