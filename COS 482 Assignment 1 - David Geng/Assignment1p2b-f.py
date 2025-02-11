""" 
David Geng
COS 482 
Assignment 1
10/6/24
"""
###############
#This file is for Task 2b-f 
#I commented most of the tasks out to organize them, uncomment the divided tasks for them to work
###############

import pandas as pd
import matplotlib.pyplot as mat

#Getting the csv in and dropping extra index
df2 = pd.read_csv('ml_articles_info-cleaned.csv')
df2 = df2.drop("Unnamed: 0", axis=1)

#Task B/////////////////////////////////////////////////////////////////////////
#Filters for 2023+ and citation 300+ and prints it

filter = df2[(df2['year'] >= 2023) & (df2['citation_count'] > 300)]
i = len(filter) 
#print ('TASK 2B RESULT')
print(i)
print(filter)

#Task C//////////////////////////////////////////////////////////////////////////
#Plots the citation count vs the average citations per year

#df2.plot(kind='scatter', x= 'citation_count' ,y= 'avg_citations_per_year')
#mat.title('Citation Count vs Average Citations per Year')  
#mat.xlabel('Citation Count')  
#mat.ylabel('Average Citations per Year')
#mat.show()

#Task D/////////////////////////////////////////////////////////////////////
#Plots the histogram on distribution of average citations per year

#df2['avg_citations_per_year'].plot(kind='hist')
#mat.title('Distribution of Average Citations per Year for Articles')  
#mat.xlabel('Average Citations Per Year')  
#mat.ylabel('Number of Articles')
#mat.show()

#Task E////////////////////////////////////////////////////// (This section is required for Task F to work)
#Filters each of the years into frames 

filter22 = df2[(df2['year'] == 2022)]
print(len(filter22))

filter23 = df2[(df2['year'] == 2023)]
print(len(filter23))

filter24 = df2[(df2['year'] == 2024)]
print(len(filter24))

#///////////////////////////////////////////////////////////
#Turns the count into a data frame and chart it

#count = {
    #'year': ['2022', '2023', '2024'], 
    #'number': [len(filter22), len(filter23), len(filter24)]}

#count_df = pd.DataFrame(count)
#count_df.plot(kind='bar', x='year', y='number')
#mat.title('Articles Published Each Year Since 2022')  
#mat.xlabel('Year')  
#mat.ylabel('Number of Articles Published')
#mat.show()

#Task F/////////////////////////////////////////////////////////
#Using the mean2X from task E calculates the averages and charts them 

mean22 = filter22['citation_count'].mean()
print(mean22)

mean23 = filter23['citation_count'].mean()
print(mean23)

mean24 = filter24['citation_count'].mean()
print(mean24)

count2 = {
    'year': ['2022', '2023', '2024'], 
    'mean': [mean22, mean23, mean24]}

count2_df = pd.DataFrame(count2)
count2_df.plot(kind='bar', x='year', y='mean')
mat.title('Average Citation Count of Articles Published in X Year')  
mat.xlabel('Year')  
mat.ylabel('Average Citation Count')
mat.show()