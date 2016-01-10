'''
Created on Apr 6, 2015

@author: Swati
'''
SOURCEFILE = "..\\Data\\allrawdata.csv"
OUTPUTFILE = "..\\Data\\Results.txt"
SUMMARY = "..\\Data\\SummaryResult.txt"
DATALABELS =["age", "workclass", "fnlwgt", "education", "education-num", "marital-status",
               "occupation", "relationship", "race", "sex", "capital-gain",
               "capital-loss", "hours-per-week", "native-country", "class"] 
MISSING_DROPPED_FILE = "..\\Data\\missingDropped.csv"
MISSING_REPLACED_FILE = "..\\Data\\missingReplaced.csv"
DISCRETIZED_FILE ="..\\Data\\discretized.csv"
DATATYPE = {"age": 1, "workclass": 0, "fnlwgt":1, "education":0 , "education-num":1, "marital-status" : 0,
                   "occupation": 0, "relationship": 0, "race" : 0, "sex" :0, "capital-gain": 1,
                   "capital-loss" : 1, "hours-per-week": 1, "native-country": 0, "class": 0}