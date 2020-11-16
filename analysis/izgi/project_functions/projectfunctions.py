{
    "cells" : [],
    "metadata" : {},
    "nbformat" : 4,
    "nbformat_minor" :4


}
def load(address):
    import pandas as pd
    import csv
    import json
    import numpy as np
    countries = ["CA", "DE","FR","GB","IN", "JP", "KR", "MX","RU", "US"]
    data = []
    for i in range(0,10):
        address_csv = address + countries[i] + "videos.csv"
        address_json= address + countries[i] + "_category_id.json"
        csvDf = pd.read_csv(address_csv)
        jsonDf = pd.read_json(address_json)
        dataFrames = [csvDf, jsonDf]
        data.append(dataFrames)
    DFs = {"CA": data[0], "DE": data [1],"FR": data[2],"GB": data[3],"IN": data[4],"JP": data[5],"KR": data[6],"MX": data[7],"RU": data[8],"US": data[9]}

    def compileCountryDFs(DFs) :
        aDF = DFs["CA"][0].assign(Country = 'CA')
        for i in range(1,10):
            aDF = aDF.append(DFs[countries[i]][0].assign(Country = countries[i]),ignore_index = True)
        return aDF

    def cleanDFs(aDF) :
        aDF = (
        aDF.replace(r'^\s*$',np.NaN, regex = True).replace("[none]", np.NaN).dropna().dropna(axis=0)
        )
        return aDF
    
    return cleanDFs(compileCountryDFs(DFs))
        
  