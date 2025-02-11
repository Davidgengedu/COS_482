"""
David Geng
COS 482
12/20/2024
Final Project: Its just a file to compile all the csvs into one csv
"""

import psycopg2
import pandas as pd
import csv
import matplotlib.pyplot as plt
import os

dataframes = []
csvs = ["AmazonReviewsGlitter.csv","AmazonReviewsDental.csv","AmazonReviewsPaste.csv", 
"AmazonReviewsEcho.csv","AmazonReviewsShow.csv", "AmazonReviewsKids.csv", 
"AmazonReviewsMac.csv", "AmazonReviewsCre.csv", "AmazonReviewsPaw.csv", 
"AmazonReviewsDog.csv"]

#Looping through the csvs and cleaning them, its redundant with the FinalProject2_COS482.py file since I planned this out poorly
i = 0
for rev in csvs:
    with open(rev, "r", encoding="latin-1") as ff:
        df = pd.read_csv(ff, encoding="latin-1") 
        df["Month"] = df["Location/Date"].apply(lambda x: x.split("on")[1].rsplit(" ", 2)[0].strip() if "on" in x else x)
        df["Stars"] = df["Stars"].apply(lambda x: x.strip()[:3] if x else x)
        #Adding Product and Brand columns to organize them in a master list
        df["Product"] = (i) + 1
        df["Brand"] = (i//3) + 1
        dataframes.append(df)
        i += 1
        print(i)

# Combinining all dataframes
combined_df = pd.concat(dataframes, ignore_index=True)

# Save to a master list
combined_df.to_csv("CombinedReviews2.csv", index=False)

print("Combined")