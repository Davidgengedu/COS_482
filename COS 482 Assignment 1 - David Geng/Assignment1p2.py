""" 
David Geng
COS 482 
Assignment 1
10/6/24
"""
#Task 2A Cleans the data frame by splitting publication info into the four colums and adds averages, removes "Cited by"

import pandas as pd

#Sets up the new columns and deletes extra index 
df1 = pd.read_csv('ml_articles_info.csv')
df1 = df1.drop("Unnamed: 0", axis=1)
new_columns = ({'authors': pd.Series(dtype = 'string'),
                 'year': pd.Series(dtype = 'int'),
                 'venue': pd.Series(dtype = 'string'),
                 'publisher': pd.Series(dtype = 'string'),
                 'avg_citations_per_year': pd.Series(dtype = 'double')})

#The loop of splitting it by comma and dash 
i = 0
while i <= 996: #996
    Splitter = df1.loc[i]['publication_info']
    #print(Splitter)
    hold = Splitter.split('- ')
    #print (hold)
    authors = hold[0]
    hold2 = hold[1].rsplit(', ', 1) #Inconsistent naming so adding r.split
    try:
        venue = hold2[0]
        year = hold2[1]
    except Exception as e:
        year = hold2[0]
    
    try:
        publisher = hold[2]
    except Exception as e: 
        publisher = "N/A"

#sets the df to the value
    df1.at[i, 'authors'] = authors
    df1.at[i, 'venue'] = venue
    df1.at[i, 'year'] = year
    df1.at[i, 'publisher'] = publisher

#Getting rid of "Cited by"
    df1.at[i,'cited_by'] = df1.loc[i]['cited_by'].replace('Cited by ', ' ')

#Setting up division with float casts
    floatc = float(df1.loc[i]['cited_by'])
    df1.at[i,'avg_citations_per_year'] = round((floatc / ((2024 - float(year)) + 1.0)))

    i = i+1

    print (authors)
    print (venue)
    print (year)
    print (publisher)

#Drops extra column and renames it
df1 = df1.drop("publication_info", axis=1)
df1 = df1.rename(columns={'cited_by': 'citation_count'})
#rearranges columns
df1 = df1[['title', 'authors', 'year', 'venue', 'publisher', 'citation_count', 'avg_citations_per_year']]
print(df1)

#send to csv
df1.to_csv('ml_articles_info-cleaned.csv', sep = ',')
