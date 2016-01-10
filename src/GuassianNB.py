'''
Created on Apr 3, 2015
@author: Swati
'''

import pandas as pd 
import operator
from collections import Counter
import math
import Globals
pd.options.mode.chained_assignment = None  # default='warn'


def NBGuassian(training, test, dalaLabels):   
    '''
    
    '''
    probDict, classCount = trainingNBcon(training)
    confusionmat, myaccuracy = testGuassNB(test,probDict, classCount, dalaLabels )
   
    with open(Globals.OUTPUTFILE, 'a') as outfile:    
        outfile.write ("\nAccuracy = " + str(myaccuracy) + " %\n")

        keyl = list(confusionmat.keys())
        outfile.write  ("{:<8} | {:<15} {:<15} \n".format("", keyl[0], keyl[1]))
        outfile.write  ("--------------------------------------\n")
        for k, v in confusionmat.iteritems():
            outfile.write  ("{:<8} | {:<15} {:<15} \n".format(k, v[keyl[0]], v[keyl[1]]))
        outfile.write  ("--------------------------------------\n")
    outfile.close()
    return myaccuracy

def trainingNBcon(newData):
    # 0 indicates categorical , 1 indicates continuous scale
    dataType = {"age": 1, "workclass": 0, "fnlwgt":1, "education":0 , "education-num":1, "marital-status" : 0,
                   "occupation": 0, "relationship": 0, "race" : 0, "sex" :0, "capital-gain": 1,
                   "capital-loss" : 1, "hours-per-week": 1, "native-country": 0, "class": 0}
    
    dataLabels = list(newData.columns.values)
    
    # create an empty dictionary with default count as 1  for "LAPLACIAN correction"
    classseries = newData['class']
    classList = classseries.unique()
    classDict ={}
    for one in classList:
        classDict[one] = {}
        for label in dataLabels:
            if dataType[label] == 0:
                classDict[one][label]={}
                valuesU = newData[label].unique()
                for v in valuesU:
                    classDict[one][label][v] = 1 # only for categorical
            else:
                classDict[one][label]={}         # this dict will later hold, mean and standard dev
                
                
    # counting the class probabilitites
    #=========================================
    classCount = newData['class'].value_counts().to_dict()
    total = newData['class'].count()
    for oneKey in classCount:
        classCount[oneKey] = float(classCount[oneKey])/float(total)
                
    # group the data by class and count ptobability
    #==============================================
                
    groupedData = newData.groupby('class')
    for k, group in groupedData:
        for eachlabel in dataLabels:
            # if categorical ==========================
            if dataType[eachlabel] == 0 and eachlabel != 'class':
                myobj = group[eachlabel].value_counts()             # get the frequency of each distinct value
                thisd = myobj.to_dict()
                total = group[eachlabel].count()
                for onekey in thisd:
                    classDict[k][eachlabel][onekey] += thisd[onekey]                                
                    classDict[k][eachlabel][onekey] = float(classDict[k][eachlabel][onekey])/float(total)   # get prob
            elif dataType[eachlabel] == 1 and eachlabel != 'class':
            # if continuous ==========================
                classDict[k][eachlabel]['mean'] = group[eachlabel].mean()                # get mean of the group
                classDict[k][eachlabel]['std'] = group[eachlabel].std()                  # get standard deviation
     
    return classDict,  classCount          

def GuassClassify(onedata, prob_list, classCount, labels):
    '''
    prob_list : dictionary of probabilitites returned from the training
    
    '''
    postPrioriDict = dict.fromkeys(classCount.keys(), 1) 
    for label in labels:
        if labels[label]==0:
            v = onedata[label]
            for dkey in postPrioriDict:
                if v in prob_list[dkey][label]:
                    prob = prob_list[dkey][label][v]
                else:
                    prob = 1    # would not affect multiplication
                postPrioriDict[dkey] *= prob      
        else:
            x = onedata[label]
            for dkey in postPrioriDict:
                postPrioriDict[dkey] *= calculateProb(x, prob_list[dkey][label]['mean'], prob_list[dkey][label]['std']) 
                 
            
    # multiply the resultant product with Ci
    #---------------------------------------             
    for dictKey in classCount:
            postPrioriDict[dictKey] *= classCount[dictKey]
    mylabel = max(postPrioriDict.iteritems(), key=operator.itemgetter(1))[0] 
    return mylabel                
                
def calculateProb(x, mean, stdev):
    powerComp = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
    return (1 / (math.sqrt(2*math.pi) * stdev)) * powerComp           
            
def testGuassNB(newData, probDict, classCount, classLabels,  myclass='class'):
    '''
   
    '''
    labels = list(newData.columns.values)
    labels.remove(myclass)

    confusionMatrix = {}
    counter = 0
    for _, onerow in newData.iterrows():        # iterate through each row of data
        counter += 1
        mylabel = GuassClassify(onerow, probDict,classCount, classLabels)
        trueLabel = onerow[myclass]               # last col is the true class label
        if trueLabel in confusionMatrix:
            confusionMatrix[trueLabel][mylabel] += 1
        else:
            confusionMatrix[trueLabel] = Counter()
            confusionMatrix[trueLabel][mylabel] += 1
        # print ("mylabel :" + mylabel + "; True :" + trueLabel)
        
    #========================================    
    mysum = 0      
    for k in confusionMatrix:
        mysum += confusionMatrix[k][k]
    myaccuracy = (float(mysum)/float(counter)) * 100
    # print ("counter = " + str(counter) )
    
    return confusionMatrix, myaccuracy   
