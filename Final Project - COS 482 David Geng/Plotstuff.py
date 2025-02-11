"""
David Geng
COS 482
12/20/2024
Final Project: Plotting The Data
"""

import psycopg2
import pandas as pd
import csv
import matplotlib.pyplot as plt
import os
from scipy import stats
import numpy as np

#Connect to the database
conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=test")
cur = conn.cursor()

df = pd.read_csv("CombinedReviews2.csv", encoding="latin-1")

#Graphing wordcount vs ratings with a line of best fit
x = df["Stars"]
y = df["Word Count"]

#Best Fit Line calculation 
slope, intercept = np.polyfit(x, y, 1)
best_fit_line = slope * x + intercept

# Plotting the data
plt.figure(figsize=(8, 5))
plt.scatter(x, y, color="blue", alpha=0.7, label="Data Points")  # Scatter plot for individual data points
plt.plot(x, best_fit_line, color="red", label=f"Best Fit Line (y={slope:.2f}x+{intercept:.2f})")
plt.title("Word Count vs Ratings with Line of Best Fit")
plt.xlabel("Rating")
plt.ylabel("Word Count")
plt.legend()
plt.grid(True)
plt.show()

#Plotting the average ratings per month overall, and organizing the months into order
avg_rating = df.groupby("Month")["Stars"].mean().reset_index()
month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
avg_rating["Month"] = pd.Categorical(avg_rating["Month"], categories=month_order, ordered=True)
avg_rating = avg_rating.sort_values("Month")

plt.figure(figsize=(12, 6))
plt.bar(avg_rating["Month"], avg_rating["Stars"], color="blue")
plt.title("Average Ratings per Month")
plt.xlabel("Month of 2024")
plt.ylabel("Average Stars out of 5")
plt.xticks(rotation=45) 
plt.grid(True)
plt.show()



# Calculate average stars by brand
brand_avg = df.groupby("Brand")["Stars"].mean() 
plt.figure(figsize=(12, 6))
brand_avg.plot(kind="bar", color="blue")
plt.title("Average Rating for Each Brand")
plt.xlabel("Brands 1 = Crest, 2 = Google, 3 = Kraft, 4 = Amazon")
plt.ylabel("Average Review Score") 
plt.xticks(rotation=90) 
plt.grid(True)
plt.show()

#ANOVA Test
#Determining if there is a significant difference between the ratings of different months of all the brands
months = df["Month"].unique()
rating_month = [df[df["Month"] == month]["Stars"] for month in months]
f_statistic, p_value = stats.f_oneway(*rating_month)

# Print the F/P stat/value
print(f"F-statistic: {f_statistic}")
print(f"P-value: {p_value}")
if p_value < 0.05:
    print("There is a significant difference between the ratings of different months.")
else:
    print("There is no significant difference between the ratings of different months.")


#Organizing the data by brand
df_brand1 = df[df["Brand"] == 1]
df_brand2 = df[df["Brand"] == 2]
df_brand3 = df[df["Brand"] == 3]
df_brand4 = df[df["Brand"] == 4]

#Plotting for Crest
avg_rating = df_brand1.groupby("Month")["Stars"].mean().reset_index()
avg_rating["Month"] = pd.Categorical(avg_rating["Month"], categories=month_order, ordered=True)
avg_rating = avg_rating.sort_values("Month")

plt.figure(figsize=(12, 6))
plt.bar(avg_rating["Month"], avg_rating["Stars"], color="blue")
plt.title("Average Ratings per Month for Crest")
plt.xlabel("Month")
plt.ylabel("Average Rating")
plt.xticks(rotation=45) 
plt.grid(True)
plt.show()

#Plotting for Google
avg_rating = df_brand2.groupby("Month")["Stars"].mean().reset_index()
avg_rating["Month"] = pd.Categorical(avg_rating["Month"], categories=month_order, ordered=True)
avg_rating = avg_rating.sort_values("Month")

plt.figure(figsize=(12, 6))
plt.bar(avg_rating["Month"], avg_rating["Stars"], color="blue")
plt.title("Average Ratings per Month for Google")
plt.xlabel("Month")
plt.ylabel("Average Rating")
plt.xticks(rotation=45) 
plt.grid(True)
plt.show()

#Plotting for Kraft
avg_rating = df_brand3.groupby("Month")["Stars"].mean().reset_index()
avg_rating["Month"] = pd.Categorical(avg_rating["Month"], categories=month_order, ordered=True)
avg_rating = avg_rating.sort_values("Month")

plt.figure(figsize=(12, 6))
plt.bar(avg_rating["Month"], avg_rating["Stars"], color="blue")
plt.title("Average Ratings per Month for Kraft")
plt.xlabel("Month")
plt.ylabel("Average Rating")
plt.xticks(rotation=45) 
plt.grid(True)
plt.show()

#Plotting for Amazon
avg_rating = df_brand4.groupby("Month")["Stars"].mean().reset_index()
avg_rating["Month"] = pd.Categorical(avg_rating["Month"], categories=month_order, ordered=True)
avg_rating = avg_rating.sort_values("Month")

plt.figure(figsize=(12, 6))
plt.bar(avg_rating["Month"], avg_rating["Stars"], color="blue")
plt.title("Average Ratings per Month for Amazon")
plt.xlabel("Month")
plt.ylabel("Average Rating")
plt.xticks(rotation=45) 
plt.grid(True)
plt.show()


# Execute the query to find the top 20 words with the highest average ratings that have more than 40 occurrences
cur.execute("""
    SELECT Word, AvgStars, Occurences
    FROM AvgStuff
    WHERE Occurences > 40
    AND LENGTH(Word) >= 4
    ORDER BY AvgStars DESC
    LIMIT 20;
""")

rows = cur.fetchall()
df = pd.DataFrame(rows, columns=["Word", "AvgStars", "Occurences"])

#Plot results
plt.figure(figsize=(12, 6))
plt.bar(df["Word"], df["AvgStars"], color="blue")
plt.title("Top 20 Words with > 40 Occurrences vs Average Stars")
plt.xlabel("Word")
plt.ylabel("Average Stars")
plt.xticks(rotation=45)  
plt.grid(True)
plt.show()

# Execute the query to find the bottom 20 words with the lowest average ratings that have more than 40 occurrences
cur.execute("""
    SELECT Word, AvgStars, Occurences
    FROM AvgStuff
    WHERE Occurences > 40
    AND LENGTH(Word) >= 4
    ORDER BY AvgStars ASC
    LIMIT 20;
""")

rows = cur.fetchall()
cur.close()
conn.close()

df = pd.DataFrame(rows, columns=["Word", "AvgStars", "Occurrences"])

#Plot again
plt.figure(figsize=(12, 6))
plt.bar(df["Word"], df["AvgStars"], color="red")
plt.title("Bottom 20 Words with > 40 Occurrences vs Average Stars")
plt.xlabel("Word")
plt.ylabel("Average Stars")
plt.xticks(rotation=45)  
plt.grid(True)
plt.show()

