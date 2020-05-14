import requests
import urllib.request
import pandas as pd
import numpy as np
from LitFinderParameterFile import Discerning_User_Input, Filter_Option, Specifying_File_Location
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
#The file containing their respective gene list as a .txt file or a .py extension.
#The function takes a parameter from the parameter file which serves as an input
def Accessing_User_Input(User_Input):
    f=open(User_Input, "r")
    L=[]                        #Empty list L created to store the gene names as singular items in the list
    num_genes=1                 #Num_genes stores how many genes are being investigated for later use in construction of the data frame
    for line in f:              #For loop created to iterate over the file possessing gene names an insert each into list L
        line=line.rstrip()      #Strips line of whitespace
        line=line.split()       #Split Lines accordingly
        L+=line                 #Append gene item to list L
        num_genes+=1
    num_genes=str(num_genes)    #Num_genes must be in the form of a string for creating excel dataframe
    return L, num_genes

User_Input_Info=Accessing_User_Input(Discerning_User_Input())   #Serves as an execution variable, calling the parameter file function to access input
L=User_Input_Info[0]                                            #Accesses the gene listfor constructing the ESearchURLS
print(L)                                                        #Print the gene list visibly to user
num_genes=User_Input_Info[1]                                    #Provides access to the number of genes for later use in construction of the dataframe

#The MakingURL1 function generates an initial URL for each item in the gene list
#This novel URL specificies a location in the Entrez system for the gene item to be
#Searched for using the Esearch eutil provided for by NCBI. Access to this page specifies
#A webenvironment that must be collected in order to produce the second URL.
def Making_URL_1(Gene_List, FilterOption):
    ESearch_URL_List=[]
    db='pubmed'
    if FilterOption=='no' or FilterOption=='No' or FilterOption=='n' or FilterOption=='N':          #If filtering is not desired, a for loop is used to iterate through each item of the gene list
        for item in Gene_List:                                                                      #Specifies the object (Gene_List) to be iterated through
            base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'                                 #This is the base url for all pubmed Entrez databases
            url = base + "esearch.fcgi?db=" + db + "&term=" + item + "&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"
            print(url)
            ESearch_URL_List.append(url)                                                            #This function appends the newly generated URL to the URL1_List
    elif FilterOption=="yes" or FilterOption=="Yes" or FilterOption=='y':                           #If filtering is desired, the user is provided with input statements for their input
        Type=str(input("Is the desired filter a year, specific journal, or keyword? (Acceptable responses are 'year', 'journal', or 'keyword')")) 
        if Type=="journal":                                                                         #If the user filters for a journal
            Query1=str(input("What is the name of the journal?")) + "[journal]"                     #The journal is input to the URL with the tag [journal]
        elif Type=="year":                                                                          #If the user filters for a year
            Query1=str(input("What year is desired?")) + "[pdat]"                                   #The year is input to the URL with the tag pdat
        elif Type=="keyword":                                                                       #If the user filters for the keyword
            Query1=str(input("What keyword should papers be filtered for?"))                        #The keyword is input into the URL
        for item in Gene_List:                                                                      #This for loop is intended to iterate through each item in the protein lists
            base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'                                 #This is the base url for all pubmed Entrez databases
            url = base + "esearch.fcgi?db=" + db + "&term=" + item +"+AND+"+ Query1 + "&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"
            ESearch_URL_List.append(url)                                                            #This function appends the newly generated URL to the URL1_List
    print(ESearch_URL_List)
    return ESearch_URL_List
ESearch_URL_List = Making_URL_1(L, Filter_Option())                                                 #Stores the ESearch_URL_List by calling the Making_URL_1 function with gene list and filter option parameters

#The AccessingESearchDatabse function is used to obtain the information content specified in the ESearch
#Domain of the Entrez system. Because each gene items has its own URL, there is a unique domain for
#Each gene item as well, and the information therein must be accessed an stored for each gene item,
#In particular, the unique web environment created for each gene item
def AccessingEsearchDatabase(Esearch_URL_List):
    Content_Esearch_Database=[]                             #The Content_ESearch_Database list serves as a storage location to retain the contents of each databse for each gene item
    for item in ESearch_URL_List:                           #The for loop iterates over the ESearch URLs in URL1_List and requests access to their contents
        res=requests.get(item)                              #This function obtains access to the ESearch URL
        type(res)                                           #This function converts the URL content to an accessible type
        Content_List=[]                                     #This creates a list to put the data from the first database in
        for line in res:                                    #This for loop iterates through the content of the first database 
            Content_List.append(line)                       #This inserts each line of the first database into the list
        Content_Esearch_Database.append(str(Content_List))  #This converts the list to a string and appends it to the greater list
    print(Content_Esearch_Database)                         #The content of the database is visibly printed for the user to see
    return Content_Esearch_Database
AccessingEsearchDatabase(ESearch_URL_List)
ESearch_Content=AccessingEsearchDatabase(ESearch_URL_List)

#The MakingURL2 function iterates over each item of the ContentDatabase1 list
#(which specifies the domain content for each gene item from the first url)
#And searches for where the Web Environment is specified. Because the content
#Is stored as a list, acquiring the web environment for each gene item is as simple
#As splicing it out of the list for each item. With the web environment now accessed,
#A unique URL can be created for each gene item again which specifies the location in the
#EFetch domain of the Entrez system where the literature for each gene item can be acquired    
def Making_EFetch_URL(ESearch_Content):
    EFetch_URL_List=[]                                                          #Empty list URL2_List serves to store all of the URLs for the second database
    for item in ESearch_Content:                                                #The for loop iterates over the entirety of ESearch content for each item in ESearch_Content
        start = "<WebEnv>"                                                      #Now that the first database has been converted to a list, start and End represent the parts of this database we want to parse
        End = "</WebEnv>"                                                       #The end position will exhibit the WebEnv in between the start and end
        web = item[item.index(start)+len(start):item.index(End)]                #This function parses out the WebEnv from the first database
        web = str(web)                                                          #The WebEnv is converted to string so that it can be put into the URL for the second database
        base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'                 #This is the base url for all pubmed Entrez databases
        db='pubmed'                                                             #The Entrez Database being accessed is pubmed
        url2 = base + "efetch.fcgi?db=" + db + "&query_key=1&WebEnv=" + web + "&rettype=abstract&retmode=text"
        EFetch_URL_List.append(url2)                                            #This appends each EFetch URL to the EFetch URL List
    return EFetch_URL_List
EFetch_URL_List = Making_EFetch_URL(ESearch_Content)

#The Generating_Literature_Data function is used to access the content from the EFetch database for
#Each gene and subsequently extract the DOI number and PMID number associated with each
#Paper. This is then compiled into a data array for the purpose of creating a dataframe
#Specifying the total literature existing with regards to a specific gene
def Generating_Literature_Data(EFetch_URL_List):
    Large_PMID_List=[]                                          #Stores all PMIDs in nested PMID_List
    Large_DOI_List=[]                                           #Stores all DOIs in nested DOI_List
    PMID_List=[]                                                #Stores all PMIDs in a comprehensive PMID_List, not nested
    dataarray=[]                                                #Serves as the dataarray header for the dataframe
    DOI_Num=[]                                                  #Specifies the number of DOIs encountered
    Flat_PMID_List=[]                                           #Specifies the PMIDs in a flat, unnested list
    for URL in EFetch_URL_List:                                 #This for loop iterates over every EFetch URL that has been acquired for each gene and obtains access to its contents
        request = urllib.request.Request(URL)                   #The request function requests access to the contents of the EFetch domain
        result = urllib.request.urlopen(request)                #The urlopen function opens the URL specifying the EFetch domain content
        resulttext = result.read()                              #The read function iterates through the content of the EFetch domain
        resulttext = resulttext.decode("utf-8")                 #The EFetch domain is encoded in utf-8, so this is converted to a string
        resulttext = resulttext.split()                         #The split function converts the content into a list format so it can be properly indexed

        indexPosList1 = []                                      #Serves as a list comprised of the index positions where 'DOI' is specified 
        indexPos1 = 0                                           #Initial amount in indexed positions
        while True:                                             #USes a while loop to iterate over all items from the stored EFetch content
            try:                                                #Specifies the route
                indexPos1 = resulttext.index("DOI:", indexPos1) #This function indexes  the position where "DOI" is specified
                indexPosList1.append(indexPos1)                 #This function appends the index position of DOI to the lst
                indexPos1 += 1                                  #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
            except ValueError as e:                             #If no other DOIs are found, the while loop ceases
                break                                           #While loop terminates

        DOI_List=[]                                             #Serves as a list accessing the DOIs for each EFetch URL
        x = []                                                  #Stores each DOI
        DOI_Ctr=0                                               #Counts the number of DOIs in the URL
        for pos1 in indexPosList1:                              #The for loop is used to iterate over all the index positions where "DOI" is found
            DOIs=resulttext[pos1 + 1]                           #Accesses the position +1 relative to where DOI is specified
            x.append(DOIs)                                      #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
            DOI_List.append(DOIs)                               #DOI_List is nested and specifies all DOIs where as x specifies only the DOIs for one EFetch URL      
            DOI_Ctr+=1                                          #The value of the number of DOIs increases by one for each DOI found
        print(x)                                                #The DOIs are visible for each EFetch URL
        dataarray.append(x)                                     #The DOI list is appended as its own set into the dataarray
        DOI_Num.append(DOI_Ctr)                                 #The number of DOIs in the EFetch URL is placed into its own set
        Large_DOI_List.append(DOI_List)                         #The DOIs are appended as a set to the nested DOI list

        indexPosList2 = []                                      #This serves as an empty list to acquire the index position for every location where "PMID" is specified
        indexPos2 = 0                                           #Initial amount in indexed positions
        while True:                                             #A while loop is used to iterate over every item of the list
            try:                                                #Specifies the route
                indexPos2 = resulttext.index("PMID:", indexPos2)#This function indexes  the position where "PMID" is specified
                indexPosList2.append(indexPos2)                 #This function appends the index position of PMID to the list
                indexPos2 += 1                                  #Because the PMID number is specified at the index following where PMID is specified, 1 is added to the index
            except ValueError as e:                             #If no other PMIDs are found, the while loop ceases
                break                                           #While loop terminates
        y=[]                                                    #The y list serves as a location to compile all the PMID numbers for the literature associated with a given protein
        for pos2 in indexPosList2:                              #The for loop is used to iterate over all the index positions where "PMID" is found  
            PMIDs=resulttext[pos2+1]                            #Accesses the position +1 relative to where PMID is specified
            PMID_List.append(PMIDs)                             #The PMID value is acquired by indexing the position +1 relative to the index position where "PMID:" is specified
            y.append(resulttext[pos2+1])                        #Because the PMID number is is specified at the index following where PMID is specified, 1 is added to the index
        dataarray.append(y)                                     #The PMID list is then appended to the dataarray
        Large_PMID_List.append(y)                               #The PMID_list is appended as a set to the nested Large_PMID_List
    
    Flat_PMID_List=[item for elem in Large_PMID_List for item in elem]
    return Large_PMID_List, Large_DOI_List, PMID_List, dataarray, DOI_Num, Flat_PMID_List
All_Content=Generating_Literature_Data(EFetch_URL_List) 


#The GeneratingDataFrame function serves to compile the DOIs and PMIDs into
#A user friendly format, and associate these values with their respective genes
#From which they derive.This function also creates a collective array possessing
#The gene names and also associating with each of these genes their own respective
def GeneratingDataFrame(Gene_List, dataarray, DOI_Num):
    new_gene_list=[]                                            #This serves as an empty list to create a gene list where each gene is doubly present to associate it with both DOI and PMID
    for gene in Gene_List:                                      #This for loop is created to double every item in the list
        new_gene_list.append(gene)                              #These functions append the new item to the  list
        new_gene_list.append(gene)                              #This function ensures that the gene is represented twice each time in the list
    ctr=0                                                       #Ctr serves to account for the number of genes in constructing the dataframe
    for item in Gene_List:                                      #For each gene, the ctr is increased
        ctr+=1                                                  #Each gene increases the value of counter by one
    Header=(['DOI']+['PMID'])*ctr                               #The header is the number of genes and attaches to each gene the label "DOI" and "PMID"
    arrays=[np.array(new_gene_list),                            #This creates the array to serves as the index for the dataframe. The indexes are based off of the gene item and its respective DOI/PMID
            np.array(Header)]
    df=pd.DataFrame(dataarray, index=arrays)                    #This function creates the panda dataframe with the DOIs & PMIDs specifying the data while the dataarray specifies the index
    print(df)
    return df
df=GeneratingDataFrame(L, All_Content[3], All_Content[4])
def Generating_Bar_Graph(Gene_List, dataarray, DOI_Num):
    bar_graph=pd.DataFrame({"Genes":Gene_List, "Number of Papers":DOI_Num}) #The barplot utilizes the data held in the gene list and uses the number of papers for each gene
    ax=bar_graph.plot.bar(x="Genes", y="Number of Papers", rot=0)           #The x axis is constituted by the genes while the y axis is constituted by the number of papers
    print(bar_graph)
    return bar_graph
bar_graph=Generating_Bar_Graph(L, All_Content[3], All_Content[4])
    
#In order to generate citation data, new databases needed to be accessed in order
#To acquire the citation numbers for each paper. For this reason, each paper was
#Compiled into a list, and this paper list was then iterated through to develop
#The ESearch URL. The content of each URL was then stored in a separate list
def Accessing_PMID_File(Flat_PMID_List):
    ContentCitationData=[]                                                                          #The content of the ESearch database will be stored as an item in the list in the
    Batch_List=[Flat_PMID_List[PMID:PMID+199] for PMID in range(0, len(Flat_PMID_List), 199)]       #List comprehension to generate sublists that constitute batches to be sent to EPost
    print(Batch_List)   
    for Batch in Batch_List:                                                                        #For loop iterates through each batch and constructs a URL for each batch
        Batch=",".join(Batch)                                                                       #The PMIDs in the batch must be joined together for insertion into the URL
        PMID_URL="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=pubmed&id=" + Batch + "&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"
        request2 = urllib.request.Request(PMID_URL)                                                 #The request function requests access to the contents of the EFetch domain               
        result2 = urllib.request.urlopen(request2)                                                  #The urlopen function opens the URL specifying the EFetch domain content        
        resulttext2 = result2.read()                                                                #The read function iterates through the content of the EFetch domain        
        resulttext2 = resulttext2.decode("utf-8")                                                   #The EFetch domain is encoded in utf-8, so this is converted to a string        
        resulttext2 = resulttext2.split()                                                           #Function splits components of the database accordingly
        ContentCitationData.append(resulttext2)                                                     #This function appends the contents of each database to the ContentDatabase1
    print(ContentCitationData)
    return ContentCitationData
Content_EFetch_Data=Accessing_PMID_File(All_Content[5])

#With the contents of the first database compiled, the WebEnvironment was parsed
#Out of the content of the first URL. Once the WebENvironment was acquired, it is
#Inserted into the URL generator for the ESummary URL, and those URLs are compiled
def Generating_Esummary_URLs(Content_EFetch_Data):
    ESummary_URL_List=[]                                                #Empty list ESummary_URL_List serves to store all of the URLs for the ESummary database
    for item in Content_EFetch_Data:                                    #The for loop iterates over the entirety of ESearch content for each item in ContentDatabase1
        for pos in item:
            if item.index(pos)==12:
                start = pos.find('<WebEnv>')+8                          #Now that the first database has been converted to a list, start and End represent the parts of this database we want to parse
                End = pos.find("</WebEnv>", start)                      #The region between the start and end exhibits the WebEnv
                web = pos[start:End]                                    #This function parses out the WebEnv from the first database
                web = str(web)                                          #Converts the webenvironment to a string for insertion into the url
                db='pubmed'                                             #Entrez Database to be accessed is pubmed
                base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/' #This serves as the base URL for all Entrez databases
                ESummary_URL = base + "esummary.fcgi?db=" + db + "&query_key=1&WebEnv=" + web + "&rettype=abstract&retmode=text" #This is the url for the second database
                ESummary_URL_List.append(ESummary_URL)                  #The URL constructed is appended to the ESummary URL List
    print(ESummary_URL_List)
    return ESummary_URL_List
ESummary_List=Generating_Esummary_URLs(Content_EFetch_Data)

#The Accessing Citation Data function iterates through each item of the Esummary
#URL list and subsequently requests access to each of these ESummary URLs.
#To access the citation numbers for each of the papers, a while loop is used
#To index for the position where 'Name=PMCRefCount' is present
def Accessing_Citation_Data(ESummary_URL_List):
    PMID_Pos_List=[]                                                            #Serves as a list to store the positions of the PMIDs in the list
    for url2_PMID in ESummary_URL_List:                                         #This for loop iterates over every EFetch URL that has been acquired for each gene and obtains access to its contents
        request2 = urllib.request.Request(url2_PMID)                            #The request function requests access to the contents of the EFetch domain               
        result2 = urllib.request.urlopen(request2)                              #The urlopen function opens the URL specifying the EFetch domain content        
        resulttext2 = result2.read()                                            #The read function iterates through the content of the EFetch domain        
        resulttext2 = resulttext2.decode("utf-8")                               #The EFetch domain is encoded in utf-8, so this is converted to a string        
        resulttext2 = resulttext2.split()
        
        indexPosList3 = []                                                      #List storing the positions where PMCRefCount is specified
        indexPos3=0                                                             #Initial Index position is zero
        while True:                                                             #A while loop is used to iterate over every item of the list
            try:                                                                #'try' searches for the subsequent expressions
                indexPos3 = resulttext2.index('Name="PmcRefCount"', indexPos3)  #This function indexes  the position where "Name=PmcRefCount" is specified
                indexPosList3.append(indexPos3)                                 #This function appends the index position of Name=PmcRefCount to the lst
                indexPos3 += 1                                                  #Because the Name=PmcRefCount number is is specified at the index following where DOI is specified, 1 is added to the index
            except ValueError as e:                                             #If no other Name=PmcRefCount are found, the while loop ceases
                break                                                           #While loop terminates

        for pos3 in indexPosList3:                                              #The for loop is used to iterate over all the index positions where "DOI" is found     
            PMID_Pos_List.append(resulttext2[pos3 + 1])                         #Because the DOI number is is specified at the index following where DOI is specified, 1 is added to the index
    print(PMID_Pos_List)
    return PMID_Pos_List
PMID_Pos_List=Accessing_Citation_Data(ESummary_List)

#The position of the item from the PMCRefCount list is then iterated
#Through. Because the content of the URL is stored in a list,
#In order to access the Citation number, the position +1 relative to the
#PMCRefCount is indexed for. The citation number is then stored in its own list
def Generating_Citation_Data(PMID_Citation_List, PMID_List):
    Citation_Number_List=[]                                                 #Stores the number of citations for each PMID in the list
    start='Type="Integer">'                                                 #Start is the position coming before the citation number
    end='</Item>'                                                           #End is the position coming after the citation number
    for item in PMID_Citation_List:                                         #For loop iterates through each position, acquires the citation number, and appends it to the list
        CitationCount=item[item.index(start)+len(start):item.index(end)]    #This function indexes for the position between start and stop
        CitationCount=int(CitationCount)                                    #The CitationNumber must be converted to an integer to be in a usable data format
        Citation_Number_List.append(CitationCount)                          #Appends the number of citations for the respective PMID in the list

    citation_ctr=1                                                          #Citation ctr is given a value of 1 because the dataframe in excel begins with 1 rather than zero
    for item in PMID_List:                                                  #The for loop accounts for the number of items in the PMID list
        citation_ctr+=1                                                     #For each item in the PMID list, a value of 1 is added to the citation counter
    citation_ctr=str(citation_ctr)                                          #The citation counter is converted to a string in order to be used in the data frame

    PMID_df = pd.DataFrame({"Citation_Number_List":Citation_Number_List}, index=PMID_List)          #Panda dataframe constructs PMID data set with PMIDs as index and CitationNumber as value
    PMID_bar_graph=pd.DataFrame({"Citation_Number_List":Citation_Number_List}, index=PMID_List) 
    print(PMID_df)
    return Citation_Number_List, citation_ctr, PMID_df, PMID_bar_graph
Citation_Number_List=Generating_Citation_Data(PMID_Pos_List, All_Content[2])[0]
citation_ctr=Generating_Citation_Data(PMID_Pos_List, All_Content[2])[1]
PMID_df=Generating_Citation_Data(PMID_Pos_List, All_Content[2])[2]
PMID_bar_graph=Generating_Citation_Data(PMID_Pos_List, All_Content[2])[3]
Flat_PMID_List=All_Content[5]
Large_PMID_List=All_Content[0]


def MetaAnalysis(Citation_Number_List, Flat_PMID_List, Large_PMID_List):
    print(Flat_PMID_List)
    print(Large_PMID_List)
    Zipped_Lists=([x for _,x in sorted(zip(Citation_Number_List, Flat_PMID_List), reverse=True)])

    Which_Sublist=[]
    for PMID in Zipped_Lists:
        for sublist in Large_PMID_List:
            if PMID in sublist:
                pos=Large_PMID_List.index(sublist)
                Which_Sublist.append((PMID,pos))
    ctrlist=[]
    ctr=0
    for sublist in Large_PMID_List:
        ctrlist.append(ctr)
        ctr+=1

    Ordered_List=[]
    for number in ctrlist:
        Refined_List=[]
        for PMID, sublist in Which_Sublist:
            if sublist==number:
                Refined_List.append((PMID, sublist))
        Ordered_List.append(Refined_List)

    Filtered_List=[]
    for sublist in Ordered_List:
        Filtered_List.append(sublist[:10])

    Just_PMIDs=[]
    for sublist in Filtered_List:
        The_PMIDs=[]
        for PMID, pos in sublist:
            The_PMIDs.append(PMID)
        Just_PMIDs.append(The_PMIDs)

    New_Citation_DataFrame=pd.DataFrame({"Top Ten Most Cited PMIDs":Just_PMIDs}, index=L)
    return New_Citation_DataFrame

New_Content_Citation_Data= MetaAnalysis(Citation_Number_List, Flat_PMID_List, Large_PMID_List)            
        
#Using the lists from the citation number and the list of the PMIDs
#A data frame was generated using pandas to correlate the PMID paper
#Number to the number of times it was cited. This was then used to create
#A second data frame which was then applied to create the bar plot. The various
#Plots created were then modified using xlsx writer and exported as an excel file
File_Inputs=Specifying_File_Location()
UserFile=File_Inputs[0]
File2=File_Inputs[1]
def Citation_Data_Frame(UserFile, File2, df, bar_graph, PMID_df, PMID_bar_graph, New_Citation_DataFrame, citation_ctr, num_genes):
    FileName2='C:\\Users\\' + UserFile + '\\Desktop\\'+File2+'.xlsx'    #Creation of the .xlsx file using the Filename and File user inputs
    writer=pd.ExcelWriter(FileName2, engine='xlsxwriter')

    #The following functions export the respective dataframes to excel using xlsx writer
    df.to_excel(writer, sheet_name='ComprehensiveData', index = True, header=True)                      #This function exports the DOI/PMID dataframe
    bar_graph.to_excel(writer, sheet_name="GraphicalModel", index = True, header=True)                  #This function exports the DOI bargraph
    PMID_df.to_excel(writer, sheet_name='ComprehensiveCitationData', index = True, header=True)         #This function exports the citation dataframe as a csv file to excel
    PMID_bar_graph.to_excel(writer, sheet_name="CitationModel", index = True, header=True)              #This function exports the citation bargraph
    New_Citation_DataFrame.to_excel(writer, sheet_name="CitationsSorted", index=True, header=True)      #This function exports the citation dataframe

    #These functions are used for modifying the data so that the bar plot may correctly interpret values
    workbook=writer.book
    worksheet=writer.sheets['GraphicalModel']                                                                                   #The sheet is specified
    chart1=workbook.add_chart({"type":"column"})                                                                                #The chart-type is specified as a bar graph
    chart1.add_series({"categories":"=GraphicalModel!$B$2:$B$" + num_genes, "values":"=GraphicalModel!$C$2:$C$"+num_genes})     #Genes serve as the category while the number of papers serves as the value. The offset is accounted for

    #The following functions format the chart for the number of papers
    chart1.set_title({'name':'Number of Published Papers With Respect To A Specific Gene'})     #This function specifies the chart title
    chart1.set_x_axis({"name":"Gene Names"})                                                    #This function specifies the x axis
    chart1.set_y_axis({"name":"Number of DOIs"})                                                #This function specifies the y axis
    worksheet.insert_chart("F2", chart1)                                                        #This function specifies the location of the chart in excel

    #These functions are used for modifying the data so that the bar plot
    #May interpret the values and indices correctly
    workbook=writer.book
    worksheet2=writer.sheets['CitationModel']                                                                                       #The sheet is specified
    chart2=workbook.add_chart({"type":"column"})                                                                                    #The chart-type is specified as a bar graph
    chart2.add_series({"categories":"=CitationModel!$A$2:$A$" + citation_ctr, "values":"=CitationModel!$B$2:$B$"+citation_ctr})     #Genes serve as the category while the number of papers serves as the value. The offset is accounted for
    
    #The following functions format the chart for the number of papers
    #For each specific genes. This includes the specification of paper title
    #The axes, and specifies the location of the chart in Excel
    chart2.set_title({'name':'Number of Citations with Respect to a Specific Gene'})    #This function specifies the chart title
    chart2.set_x_axis({"name":"PMIDs"})                                                 #This function specifies the x axis
    chart2.set_y_axis({"name":"Number of Citations"})                                   #This function specifies the y axis
    worksheet2.insert_chart("F2", chart2)                                               #This function specifies the location of the chart in excel

    writer.save()           #This saves the data to the Excel File specified

Citation_Data_Frame(UserFile, File2, df, bar_graph, PMID_df, PMID_bar_graph, New_Content_Citation_Data, citation_ctr, num_genes)    

    




        
