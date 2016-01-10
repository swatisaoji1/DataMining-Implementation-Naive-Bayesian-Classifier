
'''
======================================
Created on Mar 23, 2015
@author: Swati
======================================
'''

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from scipy import stats
import Globals


def readData(filename):
    '''
        takes the csv filename as input 
        replaces the missing values '?' to np.nan
        returns the pandas dataframe
        
    '''
    rawfile = pd.read_csv(filename, header=None, names=Globals.DATALABELS, sep=",", na_values=["?", " ?", "? ", " ? "], engine='python')
    rawfile['class'].apply(lambda x: x.strip())
    print "file read and missing '?' replaced with nan\n"
    return rawfile


def dealMissing(df, dataType, choice=1):
    while True:
        
        # drop values with NaN   
        if choice is 1: 
            dffinal = df.dropna() 
            dffinal.to_csv(Globals.MISSING_DROPPED_FILE)
            print "Missing Data Dropped File stores at:  " + Globals.MISSING_DROPPED_FILE
            return df.dropna(), Globals.MISSING_DROPPED_FILE  
        
        elif choice is 2:
            df, fpath = fillMissing1(df, dataType)
            return  df, fpath
        else:
            print "wrong choice try again"
        
                
def fillMissing1(df, dataType):
    '''
    Args:
        df ( 2d array/ Dict):
                             eg : ('attribute1': [12, 24, 25] , 'attribute2': ['good', 'bad'])
        dataTypes (dict): Dictionary of attribute names of df as keys and values 0/1 
                            indicating categorical/continuous variable eg:  ('attribute1':1, 'attribute2': 0)
                            
    Returns:
        writes a file with missing values replaces.    
    
    
    '''
    dataLabels = list(df.columns.values)
    for eachlabel in dataLabels:
        if dataType[eachlabel] is 1:
            
            # check if data is normal
            _,pval = stats.normaltest(df[eachlabel])
            if(pval < 0.5):
                # if the data is not normal use median of the group to replace the missing
                df[eachlabel]= df.groupby('class')[eachlabel].transform(lambda x : x.fillna(x.median()))
            else:
                # if the data is not normal use mean of the group to replace the missing
                df[eachlabel]= df.groupby('class')[eachlabel].transform(lambda x : x.fillna(x.mean()))
        else:
            #for categorical data use mode ( the most frequent value ) to replace the missing
            df[eachlabel]= df.groupby('class')[eachlabel].transform(lambda x : x.fillna(x.mode()[0]))
            
    df.to_csv(Globals.MISSING_REPLACED_FILE)
    return df, Globals.MISSING_REPLACED_FILE

def makediscrete2(df, dataType):
    dataLabels = list(df.columns.values)
    for eachLabel in dataLabels:
        if dataType[eachLabel] is 1: 
            choiceC = True
            bins = input('Enter bin size for ' + eachLabel + ": ")
            while choiceC is True:
                choice = input("Enter \n 1 - for equal size bins \n 2 - for custom range \n You Choice: "  )
                if choice == 1:    

                    df[eachLabel] = pd.cut(df[eachLabel], bins)
                    choiceC = False
                elif choice == 2:
                    print ("Enter " + str(bins+1) + " values for bin edges:")
                    binedges =[]
                    for x in range(bins+1):
                        value = input("" + str(x) + ": ")
                        binedges.append(value)

                    df[eachLabel] = pd.cut(df[eachLabel], binedges ) 
                    choiceC = False
                else:
                    print "Wrong choice Try Again!! "  
        
    df.to_csv(Globals.DISCRETIZED_FILE)
    print ("continuous data converted to discrete data stored : " + Globals.DISCRETIZED_FILE)
    return df, Globals.DISCRETIZED_FILE    
    
def makediscrete3(df, dataType):
    dataLabels = list(df.columns.values)
    for eachLabel in dataLabels:
        if dataType[eachLabel] is 1: 
            bins = input('Enter bin size for ' + eachLabel + ": ")
            df[eachLabel] = pd.cut(df[eachLabel], bins )    
            
    df.to_csv(Globals.DISCRETIZED_FILE)
    print ("continuous data converted to discrete data stored : " + Globals.DISCRETIZED_FILE)
    return df, Globals.DISCRETIZED_FILE    
   
       
def plotHistoBins(df, dataType):
    dataLabels = list(df.columns.values)
    binDivs = [10, 100, 200]
    for eachlabel in dataLabels:
        if dataType[eachlabel] == 1:            # if its a continuous variable 
            thisSer = df[eachlabel]             # get the series (array of values)
            for eachBin in binDivs:
                _, bins, _ = plt.hist(thisSer, eachBin, normed=1)
                mu = np.mean(thisSer)
                sigma = np.std(thisSer)
                plt.plot(bins, mlab.normpdf(bins, mu, sigma))
                plt.show()
                
                
def shuffle(df, n=1, axis=0):
        for _ in range(n):
            df.apply(np.random.shuffle, axis=axis)
        return df        
            
            

    
    
    
