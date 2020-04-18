import pip
import requests
from xml.etree import ElementTree
import pandas as pd
from bs4 import BeautifulSoup
import json
import urllib.request

#Program Description:
#The program produced herein intends to utlize the gene identifier symbol of a given protein
#And subseequently extract literature with respect to the proteins of interest. The program
#Here has two basic properties, the first allows the user to input whether they are investigating
#A single protein or are importing a list of many proteins. If only a single protein
#Is desired, the program will produce as output the relevant literature for that protein in
#Particular. If, however, the user is importing a data file possessing multiple proteins
#The program will create a list out of these proteins, iterate through each one of them
#And deliver the relevant literature related to all of the proteins in the list. This
#Will be done in conjunction with the NCBI database and its associated EFetch tool which
#Allows for the importing of related literature for proteins within their database.


#The Create function takes the input file and converts the UIDs into a list




#The MakingURL function is intended for creating the ESearch url which produces the WebEnv and Query keys
#Which then are implemented in creating the EFetch url




def AccessInputFile():
    filename=str(input("Type the name of the file possessing protein names")) ##Allows user to put in name of input file
    f=open(filename, "r") #Open and read input file
    global L
    L=[]
    for line in f:
        line=line.rstrip() #Strip line
        line=line.split() #Split Line
        print(line) 
        L+=line #Append line to list L
    print(L)
AccessInputFile()

def MakingURL1():
    db='pubmed'#Database being accessed is pubmed
    dictionary={}
    for item in L: #This for loop is intended to allow this entire sequence to iterate through each item in the protein lists
        query=item   #The query is set to be equal to the item in list L
        query=str(query) #The query is converted to string to fit the URL
        base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' #This is the base url for all pubmed Entrez databases
        url=base + "esearch.fcgi?db="+db+"&term="+query+"&usehistory=y" #This is the ESearch url which includes the database and query components
        print(url)
        res=requests.get(url) #This function obtains access to the ESearch URL
        type(res)
        lines=[] #This creates a list to put the data from the first database in
        for line in res: #This for loop iterates through the data 
            lines.append(line) #This inserts each line of the first database into the list
        lines=str(lines) #This converts the list to a string
        print(lines)

        start="<WebEnv>" #Now that the first database has been converted to a string, start and End represent the parts of this database we want to parse
        End="</WebEnv>"
        web=lines[lines.index(start)+len(start):lines.index(End)] #This function parses out the WebEnv from the first database
        print(web)
        web=str(web) #The WebEnv is converted to string so that it can be put into the URL for the second database
        for time in range(0,20):
            print(time)
    #web=lines[289:364]
        key="1"
        url2=base+"efetch.fcgi?db="+db+"&query_key="+key+"&WebEnv="+web+"&rettype=abstract&retmode=text" #This is the url for the second database
    #url2=base+"efetch.fcgi?db="+db+"&query_key="+key+"&WebEnv="+web+"&rettype=fasta&retmode=text"
        #print(url2)
        res2=requests.get(url2) #This function grants access to the contents received in the second database
        type(res2)
        #data=urllib.request.urlopen(url2)
        #print(data)
        #JSON=res2.json()
        #print(JSON)
        soup=BeautifulSoup(res2.text, "html.parser")
        print(soup.get_text())
        outputs=[]
        for line1 in soup: #This forloop is used to iterate through each item of the the second database
            DOI=line1[line1.index("DOI: ")+len("DOI: "):line1.index('/n')] #This is to parse the DOI from the text
            #PMID=PMID.string.strip()
            outputs.append(DOI) #Once in a string, this functon adds the string to the empty output string
            dictionary.update({item:outputs})
        print(outputs)

        
        #item=str(item) #This makes every item in the list a string
         #This dictionary is created to develop the pandas Dataframe. Each item in the protein list needs each output associated with it in the table, but the number of outputs for each item may vary
    df=pd.DataFrame.from_dict(dictionary) #This function creates the dataframe based upon the dictionary
    print(df) #This function prints the dataframe
    df.to_csv (r'C:\Users\VanderwallDavid\Desktop\export_dataframe.csv', index = False, header=True) #This function exports the dataframe as a csv file to excel
        #print(outputs)
MakingURL1()    
    #refined=[]
    #for item in outputs:
     #   item=str(item, "utf-8")
      #  refined+=item
        
        #print("PMID is", line2)
    #lines2=str(lines2)
    #lines2.rstrip()
    
    #lines2=str(lines2)
    #PMIDList=[]
    #for item in lines2:
     #   PMIDList.append(item)
    #print(PMIDList)
     
    
        
        
    


          
    
