'''
Created on Mar 23, 2015

@author: Swati
'''

from preprocess import readData, makediscrete3, makediscrete2, dealMissing
from KfoldEval import evaluateNB
import Globals




def main():
    # 0 indicates categorical , 1 indicates continuous scale
    dataType = Globals.DATATYPE
    
    # raw file is stored in Data folder in the project
    df = readData(Globals.SOURCEFILE)
    for x in range(2):
        if x+1 == 1:
            print ("MISSING VALUES DROPPED !!")
            add = "(MISSING VALUES DROPPED )"
            
            # output file will be stored in Data folder
            with open(Globals.OUTPUTFILE, 'w') as outfile:
                outfile.write("Missing Value Strategy : Drop the rows with Missing Values\n")
                outfile.write("============================================================\n")
            outfile.close()
            
            with open(Globals.SUMMARY, 'w') as summaryF:
                summaryF.write("Missing Value Strategy : Drop the rows with Missing Values\n")
                summaryF.write("============================================================\n")
            summaryF.close()
            dm, missingFile = dealMissing(df, dataType, 1)
        else:
            print (" MISSING VALUES REPLACED !! with central tendencies")
            add = "( MISSING VALUES REPLACED  )"
            with open(Globals.OUTPUTFILE, 'a') as outfile:
                outfile.write("Missing Value Strategy : Replace continuous Variable with mean/median and categorical with mode\n")
                outfile.write("================================================================================================\n")
            outfile.close()
            with open(Globals.SUMMARY, 'a') as summaryF:
                summaryF.write("Missing Value Strategy : Replace continuous Variable with mean/median and categorical with mode\n")
                summaryF.write("================================================================================================\n")
            summaryF.close()
            dm, missingFile = dealMissing(df, dataType, 2)

        for choice in range(2):
            choice = choice +1
            if choice == 1:
                print ("\nRunning Discrete Naive Bayesian {}".format(add))
                print ("-----------------------------------------------------------------\n")
                # discretize the data and pass all categorial data file to evaluateNB , last parameter 1 = call categoricalNB
                print ("Discretizing of continuous Data:")
                print ("-------------------------------")
                
                
                DisChoise = input( "Do you want to give custom range for one or more attributes ??\n"
                                    + "   Enter 1 for Yes\n   Any other value will be considered no\n"
                                    + "Please Enter your Choice: ")
                
                
                if DisChoise == 1:
                    _, filePath = makediscrete2(dm, dataType)
                else: 
                    _, filePath = makediscrete3(dm, dataType)
                
                   
                evaluateNB(filePath, dataType, 1)
            else:
                print (" Running Guassian Naive Bayesian {}".format(add))
                print (" -----------------------------------------------------------------\n")
                # last parameter 2 = call GuassianNB
                evaluateNB(missingFile, dataType, 2)
    

    
if __name__ == "__main__":
    main()