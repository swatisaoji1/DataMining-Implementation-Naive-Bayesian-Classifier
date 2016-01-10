'''
Created on Mar 25, 2015
@author: Swati
'''


import operator
from collections import Counter
import Globals
  

def naiveBaysianClassifier(training, test, dalaLabels):   
    '''
    
    '''
    probDict, classCount = trainingNBcat(training, dalaLabels)
    confusionmat, myaccuracy = testNB(test,probDict, classCount, dalaLabels )
    
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
    
        
 
 
def trainingNBcat(newData, dataTypes):
    '''
        args
            newData : pandas df or an ndarray 
        returns :
            Dictionary of probabilitites   
    '''
   
   
    dataLabels = list(newData.columns.values)
    
    # create an empty dictionary with default count as 1  for correction
    classseries = newData['class']
    classList = classseries.unique()
    classDict ={}
    for one in classList:
        classDict[one] = {}
        for label in dataLabels:
            classDict[one][label]={}
            valuesU = newData[label].unique()
            for v in valuesU:
                classDict[one][label][v] = 1
                   

    # counting the class probabilitites
    #=========================================
    classCount = newData['class'].value_counts().to_dict()
    total = newData['class'].count()
    for oneKey in classCount:
        classCount[oneKey] = float(classCount[oneKey])/float(total)
       
    
    groupedData = newData.groupby('class')
    for k, group in groupedData:
        for eachlabel in dataLabels:
            if eachlabel != 'class':
                myobj = group[eachlabel].value_counts()             # get the frequency of each distinct value
                thisd = myobj.to_dict()
                total = group[eachlabel].count()
                for onekey in thisd:
                    classDict[k][eachlabel][onekey] += thisd[onekey]                                
                    classDict[k][eachlabel][onekey] = float(classDict[k][eachlabel][onekey])/float(total)   # get prob

    return classDict, classCount    




        

def classify(onedata, prob_list, classCount, labels):
    '''
    prob_list : dictionary of probabilitites returned from the training
    
    '''
    postPrioriDict = dict.fromkeys(classCount.keys(), 1) 
    for label in labels:
        v = onedata[label]
        for dkey in postPrioriDict:
            if v in prob_list[dkey][label]:
                prob = prob_list[dkey][label][v]
            else:
                prob = 1    # would not affect multiplication
            postPrioriDict[dkey] *= prob      
              
    
    for dictKey in classCount:
            postPrioriDict[dictKey] *= classCount[dictKey]
    mylabel = max(postPrioriDict.iteritems(), key=operator.itemgetter(1))[0] 
    return mylabel

def testNB(newData, probDict, classCount, classLabels,  myclass='class'):
    '''
   
    '''
    labels = list(newData.columns.values)
    labels.remove(myclass)

    confusionMatrix = {}
    counter = 0
    for _, onerow in newData.iterrows():        # iterate through each row of data
        counter += 1
        mylabel = classify(onerow, probDict,classCount, classLabels)
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
    return confusionMatrix, myaccuracy   



    
            
                