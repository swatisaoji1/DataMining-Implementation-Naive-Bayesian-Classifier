'''
Created on Mar 21, 2015
@author: Swati
==========================================================================
MiniProject 2 -Step-1 : Data Visualization 
1-Pie Charts of Categorical Data
=============================================================================


'''
import csv
import matplotlib.pyplot as plt
import matplotlib.colors as cols
import numpy as np


    

def makeData(filename1, filename2):
    
    #Dictionaries for categorical data
    
    workClass_2 = {"Total":[0,0,0]}
    education_4 = {"Total":[0,0,0]}
    maritalStatus_6 = {"Total":[0,0,0]}
    occupation_7= {"Total":[0,0,0]}
    relationship_8 ={"Total":[0,0,0]}
    race_9 = {"Total":[0,0,0]}
    sex_10 = {"Total":[0,0,0]}
    nativeCountry_14 ={"Total":[0,0,0]}
    class_15 = {"Total":[0,0,0]}
   
    AllDict = [workClass_2, education_4, maritalStatus_6, occupation_7,relationship_8, race_9, sex_10, nativeCountry_14, class_15  ]
    
    myfile1  = open(filename1, "rb")
    reader = csv.reader(myfile1)
    for oneline in reader:
        makeDict(oneline, AllDict)
    
    myfile2  = open(filename2, "rb")
    reader = csv.reader(myfile2)
    for oneline in reader:
        makeDict(oneline, AllDict)

                
    # the function takes the dictionary and makes the pie chart
    makePie(workClass_2, 'workClass_2.png', "Work Class")
    makePie(education_4, 'education_4.png', "Education")
    makePie(maritalStatus_6, 'maritalStatus_6.png', "Marital Status")
    makePie(occupation_7,'occupation_7.png', "Occupation")
    makePie(relationship_8, 'relationship_8.png', "Relationship")
    makePie(race_9,'race_9.png', "Race")
    makePie(sex_10,'sex_10.png', "Sex")
    makePie(nativeCountry_14, 'nativeCountry_14.png', "Native Country")
    makePie(class_15, 'class_15.png', "Class")

    # make component bar chart 
    makeStackedBar(workClass_2, "workClassBar.txt", "Work Class")
    makeStackedBar(education_4, 'education_4Bar.png', "Education")
    makeStackedBar(maritalStatus_6, 'maritalStatus_6Bar.png', "Marital Status")
    makeStackedBar(occupation_7,'occupation_7Bar.png', "Occupation")
    makeStackedBar(relationship_8, 'relationship_8Bar.png', "Relationship")
    makeStackedBar(race_9,'race_9Bar.png', "Race")
    makeStackedBar(sex_10,'sex_10Bar.png', "Sex")
    makeStackedBar(nativeCountry_14, 'nativeCountry_14Bar.png', "Native Country")
    
                   
    #output files for each dictionary
    writeDictionary("workClass_2", workClass_2)
    
    
                
def writeDictionary(filename, myDict):
    outfile = open(filename, 'w')
    for key in myDict:
        outfile.write(key
                      + ": "
                      + str(myDict[key])
                      + "\n")
    outfile.close()
def makeStackedBar(mDict, filename, title): 
    lessClass = []
    moreClass = []
    labels = []
    totalCount =[]
    
    for key in mDict:
        if not key == "Total" :
            labels.append(key)
            totalCount.append(mDict[key][0])
            lessClass.append(mDict[key][1])
            moreClass.append(mDict[key][2])
        
    # no of keys
    count = len(labels)
    one = np.arange(count)  # x location of each group
    width = 0.8            # width of the bar
   
    p1 = plt.bar(one, lessClass, width, color='cyan',align='center')
    p2 = plt.bar(one, moreClass, width, color='lightsalmon', bottom=lessClass, align='center')
    
    plt.ylabel('Class Count')
    plt.title('Class Distribution in ' + title, y = 1.1, fontsize = 14 )
   
    plt.xticks(one, labels, rotation=45)
    
    plt.legend( (p1[0], p2[0]), ('<=50K', '>50K'), bbox_to_anchor=(0., 1., 1., .102), loc=9,
          ncol=3, fancybox=True, shadow=True , prop={})
    plt.show()
    
    
def makePie(MyDict, filename, mytitle):
    labels = makeLabels(MyDict)
    
    colors = makeColorList(len(labels))
    
    #===========================================================================
    # patches, = plt.pie(MyDict.values(), colors=colors, startangle=90)
    # plt.legend(patches, labels, loc="lower left")     
    #===========================================================================
            
    patches = plt.pie(MyDict.values(), None, None , colors, 
             autopct='%1.1f%%', pctdistance=1.05, shadow=True, labeldistance=1.1,
             startangle=None, radius=None, counterclock=False, wedgeprops=None, 
             textprops=None, hold=None)
    plt.legend(patches[0], labels, loc="lower left", prop={'size':8})  
     
    plt.axis('equal')
    plt.title(mytitle)
    plt.show()
    plt.savefig(filename, bbox_inches='tight')
    
def makeLabels(MyDict):
    label =[]
    for key in MyDict:
        mylabel = key + "( " + str(MyDict[key]) + " )"
        label.append(mylabel)
    return label


def makeDict(myList, DictList):
    item = 0
    dCount = 0
    for eachitem in myList:
        if item not in [0, 2, 4, 10, 11, 12 ]:
            makeListCount(eachitem, DictList[dCount])
            DictList[dCount]["Total"][0]+=1
            
            # get class and add count to the key for stacked bar
            if myList[14].strip().rstrip('.') == "<=50K":
                DictList[dCount][eachitem][1]+=1
                DictList[dCount]["Total"][1]+=1
            elif myList[14].strip().rstrip('.') == ">50K":
                DictList[dCount][eachitem][2]+=1
                DictList[dCount]["Total"][2]+=1
            
            dCount += 1
        else:
            print item
            print eachitem
            print "i am in else"
        item +=1
        
        
        
def makeListCount(key,myDict):
    if key in myDict:
        myDict[key][0]+=1
    else:
        myDict[key]= [0,0,0]
        myDict[key][0]+=1
        
        
def updateCount(myClass, dList):
    for everyDict in dList:
        for key in everyDict:
            # add counts for classes if not already added
            if len(everyDict[key]) == 1:
                everyDict[key].append(0) # count of <=50k
                everyDict[key].append(0) # count of >50k
            
            #increment count
            if myClass.strip() == "<=50K":
                everyDict[key][1]+=1
            elif myClass.strip() == ">50K":
                everyDict[key][2]+=1
                
                
        
def increaseKeyCount(key, myDict): 
    if key in myDict:
        myDict[key]+=1
    else:
        myDict[key]=0
        myDict[key]+=1
    
def makeColorList(mylength):
    colorfile = open("color.txt", 'r')
    colors =[]
    cc = cols.ColorConverter()
    for eachcolor in colorfile:
        eachcolor= eachcolor.strip()
        colors.append(cc.to_rgb(eachcolor))   
    colorCount = len(colors)
    if mylength < len(colors):
        finalcolors = colors[:mylength]
    else:
        i = 0
        finalcolors =[]
        index = 0
        while i < mylength:
            finalcolors.append(colors[(index % colorCount)])
            i+=1
            index+=1
    return finalcolors
            
