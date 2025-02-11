"""
David Geng
COS 482
12/20/2024
Final Project: SQL/Data Cleaning Stuff
"""

import psycopg2
import pandas as pd
import csv
import matplotlib.pyplot as plt

#Initializing Stuff
Word_Stars = {}

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres password=test")
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Reviews CASCADE;")
cur.execute("DROP TABLE IF EXISTS AvgStuff CASCADE;")
cur.execute("""
    CREATE TABLE IF NOT EXISTS Reviews(
        idNo text PRIMARY KEY,
        Text text,
        Datea text,
        Stars numeric,
        WordCount numeric);
            
    CREATE TABLE IF NOT EXISTS AvgStuff(
        Word text PRIMARY KEY,
        AvgStars numeric,
        Occurences numeric
    );
""")
conn.commit()

#List of the csvs to be read
csvs = ["AmazonReviewsGlitter.csv","AmazonReviewsDental.csv","AmazonReviewsPaste.csv", 
"AmazonReviewsEcho.csv","AmazonReviewsShow.csv", "AmazonReviewsKids.csv", 
"AmazonReviewsMac.csv", "AmazonReviewsCre.csv", "AmazonReviewsPaw.csv", 
"AmazonReviewsDog.csv"]
i = 0

#Looping throught he csvs
for link in csvs:
    with open(link, "r", encoding="latin-1") as file:
        next(file)
        for line in file:
            Splitter = line
            #Stripping and splitting data
            try:
                idNi = i
                #print(idNi)
                hold = Splitter.rsplit(",", 4)
                Text = hold[0].strip()
                #print(Text)
                #Targeting only the date
                Date = str(hold[1].strip() + ", " + hold[2].strip()[:4])
                part = Date.split("on")
                Datea = part[1].rsplit(" ", 2)[0]
                Datea = Datea.strip()
                #print(Datea)
                #Targeting only the number of stars
                Stars = hold[3].strip()[:3]
                #print(Stars)
                WordCount = hold[4].strip()
                #print(WordCount)
                
                #Setting up to count occurances of words
                words = Text.split()  

                #Loop to count the occurances of words
                for word in words:
                    cword = word.lower().strip(',.?!"')  
                    #print(f"Processing word: {cword}")
                    if cword not in Word_Stars:
                        Word_Stars[cword] = [] 
                
                    Word_Stars[cword].append(Stars)
            except:
                print("Error", i)

            #Inserting data into the Reviews table 
            try:
                cur.execute("INSERT INTO Reviews VALUES (%s, %s, %s, %s, %s);",
                    (idNi, Text, str(Datea), float(Stars), float(WordCount)))
                conn.commit()
            except psycopg2.Error as e:
                print("Error inserting data:", e)
                conn.rollback()
            i += 1

#Calculating the average rating associated for each word
word_avg_stars = {
    word: {"count": len(stars),"avg_stars": round(sum(float(star) for star in stars) / len(stars), 2)} 
    for word, stars in Word_Stars.items()
}

#Creating a dataframe to store the data
df = pd.DataFrame(
    [(word, data["avg_stars"], data["count"]) for word, data in word_avg_stars.items()],
    columns=["Word", "AvgStars", "Occurences"]
)
df.to_csv("Avg.csv", index=False)

#Inserting data into the AvgStuff table
with open("Avg.csv", "r", encoding="latin-1") as something:
    next(something)
    for line2 in something:
        Splitter2 = line2
        hold2 = Splitter2.rsplit(",",2)
        Word2 = hold2[0].strip()
        AvgStars2 = hold2[1].strip()
        Occurences2 = hold2[2].strip()
        try:
            cur.execute("INSERT INTO AvgStuff VALUES (%s, %s, %s);",
                (Word2, float(AvgStars2), float(Occurences2)))
            conn.commit()
        except psycopg2.Error as e:
            print("Error inserting data:", e)
            conn.rollback()

cur.close()
conn.close()
