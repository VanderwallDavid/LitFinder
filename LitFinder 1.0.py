import pip
import requests
from xml.etree import ElementTree
import pandas as pd
from bs4 import BeautifulSoup
import json
import urllib.request
import numpy as np

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


#The AccessInputFile function serves as an input statement provided to the user to specify
#The file containing their respective gene list as a .txt file or a .py extension
def AccessInputFile():
    filename = str(input("Type the name of the file possessing protein names"))       #filename input statement specifying gene list saved to filename variable
    f = open(filename, "r")         #Open and read input file
    global L
    L = []                          #Empty list L created to store the gene names as singular items in the list
    global num_genes
    num_genes=1
    for line in f:                  #For loop created to iterate over the file possessing gene names an insert each into list L
        line = line.rstrip()        #Strips line of whitespace
        line = line.split()         #Split Lines accordingly
        print(line) 
        L += line                   #Append gene item to list L
        num_genes+=1
    print(L)
    num_genes=str(num_genes)
AccessInputFile()


#The MakingURL1 function generates an initial URL for each item in the gene list
#This novel URL specificies a location in the Entrez system for the gene item to be
#Searched for using the Esearch eutil provided for by NCBI. Access to this page specifies
#A webenvironment that must be collected in order to produce the second URL.
def MakingURL1():
    global db
    db = 'pubmed'               #Database being accessed is pubmed
    global URL1_List
    URL1_List = []              #Empty list URL1_List used in order to collect the URLs generated for each gene item
    FilterOption=str(input("Would you like to filter the literature results? (Acceptable answers are 'y' or 'n'"))
    if FilterOption=="no" or FilterOption=="No" or FilterOption=='n':
        for item in L:              #This for loop is intended to iterate through each item in the protein lists
            query = item            #The query for the URL is the gene item from the list
            query = str(query)      #The query item is converted to string to insert into the URL
            global base
            base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'       #This is the base url for all pubmed Entrez databases
            url = base + "esearch.fcgi?db=" + db + "&term=" + query + "&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"    #This is the ESearch url which includes the database and query components
            #print(url)
            URL1_List.append(url)       #This function appends the newly generated URL to the URL1_List
    elif FilterOption=="yes" or FilterOption=="Yes" or FilterOption=='y':
        Type=str(input("Is the desired filter a year, specific journal, or keyword? (Acceptable responses are 'year', 'journal', or 'keyword')"))
        if Type=="journal":
            Query1=str(input("What is the name of the journal?")) + "[journal]"
        elif Type=="year":
            Query1=str(input("What year is desired?")) + "[pdat]"
        elif Type=="keyword":
            Query1=str(input("What keyword should papers be filtered for?"))
        
        for item in L:              #This for loop is intended to iterate through each item in the protein lists
            query = item            #The query for the URL is the gene item from the list
            query = str(query)      #The query item is converted to string to insert into the URL
                
            base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'       #This is the base url for all pubmed Entrez databases
            url = base + "esearch.fcgi?db=" + db + "&term=" + query +"+AND+"+ Query1 + "&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"    #This is the ESearch url which includes the database and query components
            #print(url)
            URL1_List.append(url)       #This function appends the newly generated URL to the URL1_List

    print(URL1_List)

MakingURL1()


#The AccessingDatabase1 function is used to obtain the information content specified in the ESearch
#Domain of the Entrez system. Because each gene items has its own URL, there is a unique domain for
#Each gene item as well, and the information therein must be accessed an stored for each gene item,
#In particular, the unique web environment created for each gene item
def AccessingDatabase1():
    
    global ContentDatabase1
    ContentDatabase1 = []           #The ContentDatabase1 list serves as a storage location to retain the contents of each databse for each gene item
    print(URL1_List)
    for URL in URL1_List:           #The for loop iterates over ESearch URLs in URL1_List to create the URL for the second database and insert each new URL into URL2_List
        #print(URL)
        res = requests.get(URL)     #This function obtains access to the ESearch URL
        type(res)
        print(res)
        lines = []                  #This creates a list to put the data from the first database in
        for line in res:            #This for loop iterates through the content of the first database 
            lines.append(line)      #This inserts each line of the first database into the list
        lines = str(lines)          #This converts the list to a string
        print(lines)
        ContentDatabase1.append(lines)  #This function appends the contents of each database to the ContentDatabase1

AccessingDatabase1()        



#The MakingURL2 function iterates over each item of the ContentDatabase1 list
#(which specifies the domain content for each gene item from the first url)
#And searches for where the Web Environment is specified. Because the content
#Is stored as a list, acquiring the web environment for each gene item is as simple
#As splicing it out of the list for each item. With the web environment now accessed,
#A unique URL can be created for each gene item again which specifies the location in the
#EFetch domain of the Entrez system where the literature for each gene item can be acquired
def MakingURL2():
    
    global URL2_List
    URL2_List = []                          #Empty list URL2_List serves to store all of the URLs for the second database
    for item in ContentDatabase1:           #The for loop iterates over the entirety of ESearch content for each item in ContentDatabase1
        start = "<WebEnv>"                  #Now that the first database has been converted to a list, start and End represent the parts of this database we want to parse
        End = "</WebEnv>"
        web = item[item.index(start)+len(start):item.index(End)]      #This function parses out the WebEnv from the first database
        print(web)
        web = str(web)                      #The WebEnv is converted to string so that it can be put into the URL for the second database
        key = "1"
        url2 = base + "efetch.fcgi?db=" + db + "&query_key=" + key + "&WebEnv=" + web + "&rettype=abstract&retmode=text" #This is the url for the second database
        URL2_List.append(url2)              #This function appends the second URL to URL2_List to store the EFetch URLs for each gene item
        print(URL2_List)
MakingURL2()



#The GeneratingData function is used to access the content from the EFetch database for
#Each gene and subsequently extract the DOI number and PMID number associated with each
#Paper. This is then compiled into a data array for the purpose of creating a dataframe
#Specifying the total literature existing with regards to a specific gene
def GeneratingData():
    global PMID_List
    PMID_List=[]
    global dataarray
    dataarray = []                                      #The emmpty dataarray list serves to compile the DOIs and PMIDs lists for each gene
    global DOI_Num
    DOI_Num=[]
    distract=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for URL in URL2_List:                               #This for loop iterates over every EFetch URL that has been acquired for each gene and obtains access to its contents
        request = urllib.request.Request(URL)           #The request function requests access to the contents of the EFetch domain       
        result = urllib.request.urlopen(request)        #The urlopen function opens the URL specifying the EFetch domain content
        resulttext = result.read()                      #The read function iterates through the content of the EFetch domain
        resulttext = resulttext.decode("utf-8")         #The EFetch domain is encoded in utf-8, so this is converted to a string
        resulttext = resulttext.split()                 #The split function converts the content into a list format so it can be properly indexed

        indexPosList1 = []                              #This serves as an empty list to acquire the index position for every location where "DOI" is specified
        indexPos1 = 0
        while True:                                     #A while loop is used to iterate over every item of the list
            try:
                # Search for item in list from indexPos to the end of list
                indexPos1 = resulttext.index("DOI:", indexPos1)     #This function indexes  the position where "DOI" is specified
                # Add the index position in list
                indexPosList1.append(indexPos1)                     #This function appends the index position of DOI to the lst
                indexPos1 += 1                                      #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
            except ValueError as e:                                 #If no other DOIs are found, the while loop ceases
                break

        x = []                                          #The x list serves as a location to compile all the DOI numbers for the literature associated with a given protein
        DOI_Ctr=0
        for pos1 in indexPosList1:                      #The for loop is used to iterate over all the index positions where "DOI" is found     
            x.append(resulttext[pos1 + 1])              #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
            DOI_Ctr+=1
        print(x)
        dataarray.append(x)                             #The DOI list is then appended to the dataarray
        DOI_Num.append(DOI_Ctr)

        indexPosList2 = []                              #This serves as an empty list to acquire the index position for every location where "PMID" is specified
        indexPos2 = 0
        while True:                                     #A while loop is used to iterate over every item of the list
            try:
                # Search for item in list from indexPos to the end of list
                indexPos2 = resulttext.index("PMID:", indexPos2)    #This function indexes  the position where "PMID" is specified
                # Add the index position in list
                indexPosList2.append(indexPos2)                     #This function appends the index position of PMID to the list
                indexPos2 += 1                                      #Because the PMID number is specified at the index following where PMID is specified, 1 is added to the index
            except ValueError as e:                                 #If no other PMIDs are found, the while loop ceases
                break
        
        y=[]                                            #The x list serves as a location to compile all the PMID numbers for the literature associated with a given protein
        for pos2 in indexPosList2:                      #The for loop is used to iterate over all the index positions where "PMID" is found     
            PMID_List.append(resulttext[pos2+1])
            y.append(resulttext[pos2+1])                #Because the PMID number is is specified at the index following where PMID is specified, 1 is added to the index
        dataarray.append(y)                             #The PMID list is then appended to the dataarray
GeneratingData()




#The GeneratingDataFrame function serves to compile the DOIs and PMIDs into
#A user friendly format, and associate these values with their respective genes
#From which they derive.This function also creates a collective array possessing
#The gene names and also associating with each of these genes their own respective
#DOI and PMID list
def GeneratingDataFrame():
    
    newL = []                           #This serves as an empty list to create a gene list where each gene is doubly present to associate it with both DOI and PMID
    for item in L:                      #This for loop is created to double every item in the list
        newL.append(item)               #These functions append the new item to the double list
        newL.append(item)
    print(newL)

    DOI = "DOI"                         #This variable is used to specify the DOI index for the dataframe
    PMID = "PMID"                       #This variable is used to specify the PMID index for the dataframe
    X = []                              #X serves as an empty list combining DOI and PMID indices together
    ctr = 0
    for item in L:                      #This for loop is used to take into account the number of items in the list to normalize the indices of the dataframe
        ctr += 1
    X=([DOI] + [PMID]) * ctr            #This function adds the proper number of DOI and PMID labels to the list
    print(X)
    global arrays
    arrays=[np.array(newL),             #This creates the array to serves as the index for the dataframe. The indexes are based off of the gene item and its respective DOI/PMID
            np.array(X)]
    global df
    df = pd.DataFrame(dataarray, index=arrays)        #This function creates the panda dataframe with the DOIs & PMIDs specifying the data while the dataarray specifies the index
    print(df)
    
GeneratingDataFrame()
       
def GeneratingBarGraph():
    global bar_graph
    bar_graph=pd.DataFrame({"Genes":L, "Number of Papers":DOI_Num})
    ax=bar_graph.plot.bar(x="Genes", y="Number of Papers", rot=0)
    
GeneratingBarGraph()   
    

#The exporting dataframe function serves to export the dataframe which has now
#Been generated into an excel file
#def ExportingDataFrame():
    
    #UserFile=str(input("""The dataframe has successfully been created! We will now export the file to the location you specify. Please type the name of your user file"""))
    #File1=str(input("Now, give the file a name of your choosing"))
    #FileName1='C:\\Users\\' + UserFile + '\\Desktop\\'+File1+'.xlsx'
    #writer=pd.ExcelWriter(FileName1, engine='xlsxwriter')
    
    #df.to_excel(writer, sheet_name='ComprehensiveData', index = True, header=True) #This function exports the dataframe as a csv file to excel
    #bar_graph.to_excel(writer, sheet_name="GraphicalModel", index = True, header=True)
    
    #workbook=writer.book
    #worksheet=writer.sheets['GraphicalModel']
    #chart=workbook.add_chart({"type":"column"})
    #chart.add_series({"categories":"=GraphicalModel!$B$2:$B$" + num_genes, "values":"=GraphicalModel!$C$2:$C$"+num_genes})

    #chart.set_title({'name':'Number of Published Papers With Respect To A Specific Gene'})
    #chart.set_x_axis({"name":"Gene Names"})
    #chart.set_y_axis({"name":"Number of DOIs"})
    #worksheet.insert_chart("F2", chart)

    #writer.save()
    
#ExportingDataFrame()
     

def AccessingPMIDFile():
    global ContentCitationData
    ContentCitationData = []  
    for PMID in PMID_List:
        PMID_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="+ PMID + "&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"

        res2 = requests.get(PMID_URL)     #This function obtains access to the ESearch URL
        type(res2)
        print(res2)
        lines2 = []                  #This creates a list to put the data from the first database in
        for line2 in res2:            #This for loop iterates through the content of the first database 
            lines2.append(line2)      #This inserts each line of the first database into the list
        lines2 = str(lines2)          #This converts the list to a string
        print(lines2)
        ContentCitationData.append(lines2)  #This function appends the contents of each database to the ContentDatabase1
        print(ContentCitationData)
AccessingPMIDFile()


def Generating_PMID_URLs():        
    global URL2_PMID_List
    URL2_PMID_List = []                          #Empty list URL2_List serves to store all of the URLs for the second database
    for item in ContentCitationData:           #The for loop iterates over the entirety of ESearch content for each item in ContentDatabase1
        start = "<WebEnv>"                  #Now that the first database has been converted to a list, start and End represent the parts of this database we want to parse
        End = "</WebEnv>"
        web = item[item.index(start)+len(start):item.index(End)]      #This function parses out the WebEnv from the first database
        #print(web)
        web = str(web)                      #The WebEnv is converted to string so that it can be put into the URL for the second database
        key = "1"
        url2_PMID = base + "esummary.fcgi?db=" + db + "&query_key=" + key + "&WebEnv=" + web + "&rettype=abstract&retmode=text" #This is the url for the second database
        URL2_PMID_List.append(url2_PMID)              #This function appends the second URL to URL2_List to store the EFetch URLs for each gene item
        #print(URL2_PMID_List)
Generating_PMID_URLs()


def Accessing_Citation_Data():          
                                  #This serves as an empty list to acquire the index position for every location where "DOI" is specified
    
    global PMC_pos_List
    PMC_pos_List = []  
    for url2_PMID in URL2_PMID_List:                               #This for loop iterates over every EFetch URL that has been acquired for each gene and obtains access to its contents
        request2 = urllib.request.Request(url2_PMID)           #The request function requests access to the contents of the EFetch domain               
        result2 = urllib.request.urlopen(request2)        #The urlopen function opens the URL specifying the EFetch domain content        
        resulttext2 = result2.read()                      #The read function iterates through the content of the EFetch domain        
        resulttext2 = resulttext2.decode("utf-8")         #The EFetch domain is encoded in utf-8, so this is converted to a string        
        resulttext2 = resulttext2.split()
        print("This is resulttext2", resulttext2)
        indexPosList3 = []
        indexPos3=0
        while True:                                     #A while loop is used to iterate over every item of the list
            try:
                # Search for item in list from indexPos to the end of list
                indexPos3 = resulttext2.index('Name="PmcRefCount"', indexPos3)     #This function indexes  the position where "DOI" is specified
                # Add the index position in list
                indexPosList3.append(indexPos3)                     #This function appends the index position of DOI to the lst
                indexPos3 += 1                                      #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
            except ValueError as e:                                 #If no other DOIs are found, the while loop ceases
                break
                                                #The x list serves as a location to compile all the DOI numbers for the literature associated with a given protein       
        for pos3 in indexPosList3:                      #The for loop is used to iterate over all the index positions where "DOI" is found     
            PMC_pos_List.append(resulttext2[pos3 + 1])              #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
            
            
Accessing_Citation_Data()

def Generating_Citation_Data():        
    global Citation_Number_List
    Citation_Number_List=[]
    start='Type="Integer">'
    end='</Item>'
    for item in PMC_pos_List:
        CitationCount=item[item.index(start)+len(start):item.index(end)]
        CitationCount=int(CitationCount)
        Citation_Number_List.append(CitationCount)
    print(Citation_Number_List)
    global citation_ctr
    citation_ctr=1
    for item in PMID_List:
        citation_ctr+=1
    citation_ctr=str(citation_ctr)
    #Citation_Dictionary={"Citation Numbers":Citation_Number_List}
    global PMID_df
    PMID_df = pd.DataFrame({"Citation_Number_List":Citation_Number_List}, index=PMID_List)
    print(PMID_df)
    global PMID_bar_graph
    PMID_bar_graph=pd.DataFrame({"Citation_Number_List":Citation_Number_List}, index=PMID_List)
    #ax=PMID_bar_graph.plot.bar(x="PMIDs", y="Citation Numbers", rot=0)
Generating_Citation_Data()

def Citation_Data_Frame():
    UserFile=str(input("""The dataframe has successfully been created! We will now export the file to the location you specify. Please type the name of your user file"""))
    File2=str(input("Now, give the file a name of your choosing"))
    FileName2='C:\\Users\\' + UserFile + '\\Desktop\\'+File2+'.xlsx'
    writer=pd.ExcelWriter(FileName2, engine='xlsxwriter')

    df.to_excel(writer, sheet_name='ComprehensiveData', index = True, header=True)
    bar_graph.to_excel(writer, sheet_name="GraphicalModel", index = True, header=True)
    
    PMID_df.to_excel(writer, sheet_name='ComprehensiveCitationData', index = True, header=True) #This function exports the dataframe as a csv file to excel
    PMID_bar_graph.to_excel(writer, sheet_name="CitationModel", index = True, header=True)
    
    workbook=writer.book
    worksheet=writer.sheets['GraphicalModel']
    chart1=workbook.add_chart({"type":"column"})
    chart1.add_series({"categories":"=GraphicalModel!$B$2:$B$" + num_genes, "values":"=GraphicalModel!$C$2:$C$"+num_genes})

    chart1.set_title({'name':'Number of Published Papers With Respect To A Specific Gene'})
    chart1.set_x_axis({"name":"Gene Names"})
    chart1.set_y_axis({"name":"Number of DOIs"})
    worksheet.insert_chart("F2", chart1)


    workbook=writer.book
    worksheet2=writer.sheets['CitationModel']
    chart2=workbook.add_chart({"type":"column"})
    chart2.add_series({"categories":"=CitationModel!$A$2:$A$" + citation_ctr, "values":"=CitationModel!$B$2:$B$"+citation_ctr})

    chart2.set_title({'name':'Number of Citations with Respect to a Specific Gene'})
    chart2.set_x_axis({"name":"PMIDs"})
    chart2.set_y_axis({"name":"Number of Citations"})
    worksheet2.insert_chart("F2", chart2)


    writer.save()

Citation_Data_Frame()        
