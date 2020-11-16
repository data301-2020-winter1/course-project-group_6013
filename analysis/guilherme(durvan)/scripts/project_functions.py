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
    #This loads the csv and json files for each country:
    countries = ["CA","DE","GB","FR","IN","JP","KR","MX","RU","US"]
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
        DF = DFs["CA"][0].assign(Country='CA') #A Canada df (csv only)
        for i in range(1,10):
            DF = DF.append(DFs[countries[i]][0].assign(Country=countries[i]),ignore_index=True) #appends the other countries csv dfs to the canada csv df, creates new column for country name
        return DF
    def cleanItUp(DF) :      #Chain 2
        DF = (
        DF.replace(r'^\s*$', np.NaN, regex=True).replace("[none]",np.NaN).dropna(axis=0).drop(columns=["thumbnail_link"])
        )#method chaining used to replace empty strings with nan, [none] with nan, and to drop nan rows, and remove image column
        return DF
    return cleanItUp(compileCsvDFs(DFs))
