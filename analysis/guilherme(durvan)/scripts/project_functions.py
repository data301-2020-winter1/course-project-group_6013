{
 "cells": [],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 4
}
def load_and_process(address):
    import pandas as pd
    import csv
    import json
    import numpy as np
    import os
    #This loads the csv and json files for each country:
    countries = ["CA","DE","GB","FR","IN","JP","KR","MX","RU","US"]
    Countries = ["Canada","Germany","Great Britain","France","India","Japan","Korea","Mexico","Russia","USA"]
    data = []
    for i in range(0,10) :
        address_csv = address + countries[i] + "videos.csv"
        address_json = address + countries[i] + "_category_id.json"
        csvDF = pd.read_csv(address_csv)  #csv df created for each country
        jsonDF = pd.read_json(address_json)  #json df created for each country
        dataFrames = [csvDF,jsonDF]    #a list of csv and json df created for each country
        data.append(dataFrames) #A list of lists of csv and json df for each country 
     #   print("current length is {0}".format(len(data)))
    #print(len(data))
    DFs = {"CA" :data[0], "DE" :data[1], "GB" :data[2], "FR" :data[3],"IN" :data[4], "JP" :data[5], "KR" :data[6], "MX" :data[7], "RU" :data[8], "US" :data[9]} #A dictionary of countries and dfs
    def compileCsvDFs(DFs) :   #Chain 1
        DF = DFs["CA"][0].assign(Country='Canada') #A Canada df (csv only)
        for i in range(1,10):
            DF = DF.append(DFs[countries[i]][0].assign(Country=Countries[i]),ignore_index=True) #appends the other countries csv dfs to the canada csv df, creates new column for country name
        return DF
    def cleanItUp(DF) :      #Chain 2
        DF = (
        DF.replace(r'^\s*$', np.NaN, regex=True).replace("[none]",np.NaN).dropna(axis=0).drop(columns=["thumbnail_link"])
        )#method chaining used to replace empty strings with nan, [none] with nan, and to drop nan rows, and remove image column
        rawCatKey = "18 - Short Movies\n19 - Travel & Events\n20 - Gaming\n21 - Videoblogging\n22 - People & Blogs\n23 - Comedy\n24 - Entertainment\n25 - News & Politics\n26 - Howto & Style\n27 - Education\n28 - Science & Technology\n29 - Nonprofits & Activism\n30 - Movies\n31 - Anime/Animation\n32 - Action/Adventure\n33 - Classics\n34 - Comedy\n35 - Documentary\n36 - Drama\n37 - Family\n38 - Foreign\n39 - Horror\n40 - Sci-Fi/Fantasy\n41 - Thriller\n42 - Shorts\n43 - Shows\n44 - Trailers"
        key = {15:"Pets & Animals",17:"Sports",10:"Music"}
        fragments = rawCatKey.split("\n")
        for fragment in fragments :
            key[int(fragment[0:2])]=fragment[5:len(fragment)]      #adds all categories to key
        key[1] = "Film & Animation"
        key[2] = "Autos & Vehicles"
        print(DF["category_id"].dtypes)
        DF["category_id"] = DF["category_id"].astype(str)  #converting values in the column to strings
        print(DF["category_id"].dtypes)
        for category in key :      
            DF["category_id"] = DF["category_id"].str.replace(str(category),key[category])       #replacing numbers in key with matching categories
        return DF
    return cleanItUp(compileCsvDFs(DFs))
