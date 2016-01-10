'''
Created on Apr 3, 2015

@author: Swati
'''

import numpy as np
import pandas as pd 
from naiveBayesianClassi import naiveBaysianClassifier
from GuassianNB import NBGuassian
import Globals
from cmath import sqrt
K_FOLD = 10


def evaluateNB(labeledDataF, dalaLabels, choice=1):
    df = readProcessedFiles(labeledDataF)
    
    if choice == 1:

        with open(Globals.OUTPUTFILE, 'a') as outfile:
            outfile.write("==========================================\n")
            outfile.write ("Evaluating Naive Bayesian (Categorical): \n")
            outfile.write("==========================================\n")
        outfile.close()
        avgAccuracy, stdeva, stderror = kfoldEvaluation(df,dalaLabels,naiveBaysianClassifier, K_FOLD)
        
        with open(Globals.OUTPUTFILE, 'a') as outfile:
            outfile.write("======================================================================\n")
            outfile.write ("ACCURACY OF {} FOLD EVALUATION IS: \nmean : {}\nStandard Dev: {}\nStandard Error: {} \n".format(K_FOLD, avgAccuracy, stdeva, stderror))
            outfile.write("======================================================================\n")
        outfile.close()
        
        with open(Globals.SUMMARY, 'a') as summaryF:
            summaryF.write("======================================================================\n")
            summaryF.write ("ACCURACY OF {} FOLD EVALUATION OF NB (Categorical) IS: \nmean : {}\nStandard Dev: {}\nStandard Error: {} \n".format(K_FOLD, avgAccuracy, stdeva, stderror))
            summaryF.write("======================================================================\n")
        summaryF.close()
        
    else:

        with open(Globals.OUTPUTFILE, 'a') as outfile:
            outfile.write("==========================================\n")
            outfile.write( "Evaluating Naive Baysian (Guassian): \n")
            outfile.write("==========================================\n")
        outfile.close()
        avgAccuracy, stdeva, stderror= kfoldEvaluation(df,dalaLabels,NBGuassian, 10)
        with open(Globals.OUTPUTFILE, 'a') as outfile:
            outfile.write("======================================================================\n")
            outfile.write ("ACCURACY OF {} FOLD EVALUATION IS: \nmean : {}\nStandard Dev: {}\nStandard Error: {} \n".format(K_FOLD, avgAccuracy, stdeva, stderror))
            outfile.write("======================================================================\n")
        outfile.close()
        
        with open(Globals.SUMMARY, 'a') as summaryF:
            summaryF.write("======================================================================\n")
            summaryF.write ("ACCURACY OF {} FOLD EVALUATION OF NB (Guassian) IS: \nmean : {}\nStandard Dev: {}\nStandard Error: {} \n".format(K_FOLD, avgAccuracy, stdeva, stderror))
            summaryF.write("======================================================================\n")
        summaryF.close()

def readProcessedFiles(filename):
    '''
    args :
            filename : path of the csv file that contains comma seperated data. 
            Data should be categorical type as this trainer does not handle continuos data.
            if your data has coninuous attributes, consider discretization.
            the 0th coulmn should be index 
    returns :
            pandas df or an ndarray 
    '''
    newData = pd.read_csv(filename, index_col =0, na_values=["?"], engine='python')
    return newData




def kfoldEvaluation(df,dalaLabels, classifier, k=10):
    '''
    
    '''
    dfList = np.array_split(df, k)
    averageList = []
    for x in range(k):
        trainList = []
        for y in range(k):
            if y == x :
                testdf = dfList[y]
            else:
                trainList.append(dfList[y])
        traindf = pd.concat(trainList)
        with open(Globals.OUTPUTFILE, 'a') as outfile:
            outfile.write ("Run " + str(x+1) + ": out of " + str(k) + "\n")
        outfile.close()
        print "*",
       
        accuracy = classifier(traindf, testdf, dalaLabels)  # returns accuracy of this run
        averageList.append(accuracy)
        mymean = np.mean(averageList, dtype=np.float64)
        stde = np.std(averageList, dtype=np.float64)
        standardErr = stde/ sqrt(float(k))
    
    print "\n"
    return mymean, stde, standardErr