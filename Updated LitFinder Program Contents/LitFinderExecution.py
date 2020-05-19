import requests
import urllib.request
import pandas as pd
import numpy as np
import LitFinderParamFile
import LitFinderUtilityFile

#Program Description:
#The program produced herein intends to utlize the gene identifier symbol of a given protein And subseequently extract literature with respect to the proteins of interest. The program
#Here has two basic properties, the first allows the user to input whether they are investigating A single protein or are importing a list of many proteins. If only a single protein
#Is desired, the program will produce as output the relevant literature for that protein in Particular. If, however, the user is importing a data file possessing multiple proteins
#The program will create a list out of these proteins, iterate through each one of them And deliver the relevant literature related to all of the proteins in the list. This
#Will be done in conjunction with the NCBI database and its associated EFetch tool which Allows for the importing of related literature for proteins within their database.

#The Accessing_User_Input Function takes parameters Input_Type, user_input_file, and user_input genes, all of which are specified by the
#LitFinderParamFile. The function uses the Input_Type to discern whether the genes to be inquired upon come in the form of a list or manual
#Input. If input is a file, then the Organizing_User_Input class is called from the LitFinderUtilityFile, which modifies the contents of the file
#Into a list format. IF the input is a manual input, Organizing_User_Input again is called, on the manual input and organizes the inputs into a
#List. The output of this function contains the iterable list of gene items and the number of genes to be investigated henceforth
def Accessing_User_Input(Input_Type, user_input_file = None, user_input_genes = None):
    if Input_Type == 0:                                                             #Verifies if the input type is a list based on the input of the parameter file
        items=LitFinderUtilityFile.Organizing_User_Input(user_input_file)           #If the input is a list, the Organizing_User_Input function from LitFinderUtilityFile is called on the input file specified by the parameter file     
        item_list=items.manipulating_list()[0]                                      #If the input is a list, the manipulatin_list function from Organizing_User_Input is called and indexed at position 0 to acquire the gene list
        item_number=items.manipulating_list()[1]                                    #If the input is a list, the manipulating_list function from Organizing_User_Input is called and indexed at position 1 to derive the number of genes to be investigated                                   
    elif Input_Type == '1':                                                         #Verifies if the input type is a manual input based on the input of the parameter file
        items=LitFinderUtilityFile.Organizing_User_Input(user_input_genes)          #If the input is a manual input, the Organizing_User_Input function from LitFinderUtilityFile is called on the input file specified by the parameter file
        item_list=items.manipulating_individuals()[0]                               #If the input is a manual input, the manipulating_individual function from Organizing_User_Input is called and indexed at position 0 to acquire the gene list
        item_number=items.manipulating_individual()[1]                              #If the input is a manual input, the manipulating_individual function from Organizing_User_Input is called and indexed at position 0 to derive the number of genes to be investigated
    return item_list, item_number                                                   #The function returns the list containing the genes to be investigated as well as the number of genes under investigation
#The Making_URL_1 function takes arguments specifying the input list from the previous function, as well as whether the search is to be filtered,
#As specified by the user input from the LitFinderParameterFile. The function first discerns whether or not the search is to be filtered, and onces
#This has been verified, an ESearch URL is created for each item in the gene list
def Making_URL_1(Gene_List, FilterOption):
    if FilterOption == 0:                                                           #Verifies that no filtering is to be applied to the search, based upon the input via the LitFinderParameterFile
        x=LitFinderUtilityFile.Generating_URLs()                                    #If no filtering is to be applied, the LitFinderUtilityFile class GeneratingURLs is called which creates URLs for each gene item
        x.add_ons(LitFinderUtilityFile.calling_objects("ESearch")[0], Gene_List,    #To generate URLs, the add_on function of the Generating_URLs class is invoked, the first parameter it requires is the entrez_location, which is discerned from a separate function by including 'ESearch' as a call parameter
                  LitFinderUtilityFile.calling_objects("ESearch")[1],               #Each entrez url is associated with its own specialized url_base, specified here via the function from LitFinderUtilityFile
                  LitFinderUtilityFile.calling_objects("ESearch")[2])               #This parameter specifies the proper suffix for the url based on its destined Entrez location
        ESearch_URL_List=x.make_url()                                               #With url parameters specified, the make_url function from Generating_URLs creates URLs for each gene item and stores them in the ESearch_URL _List
    elif FilterOption == 1:                                                         #Verifies that filtering is to be applied to the search, based upon the input via the LitFinderParameterFile
        x=LitFinderUtilityFile.Generating_URLs()                                    #If filtering is to be applied, as with the no filtering option, the Generating_URL function from the utility file is called to create all urls for each gene item
        x.add_ons(LitFinderUtilityFile.calling_objects("ESearch")[0], Gene_List,    #The add_on function takes as the first parameter the entrez location (specified by the calling_object_function from the LitFinderUtilityFile), as well as the input list of gene items
                  LitFinderUtilityFile.calling_objects("ESearch")[1],               #This argument specifies the unique base of this particular entrez location
                  LitFinderUtilityFile.calling_objects("ESearch")[2])               #This argument specifies the unique terminator of this particular entrez location
        x.filter_items(LitFinderParamFile.keywords,                                 #Because this series is filtered, these are accounted for via the additional function filter_items, the first parameter takes account of filtered keywords specified in the LitFinderParameterFile
                       LitFinderParamFile.journals,                                 #The second filter option is to take account of journals, specified by the LitFinderParameterFile
                       LitFinderParamFile.year)                                     #The final filter option takes account of the year to be search, specified by the LitFinderParameterFile
        x.filter_components()                                                       #Calling the filter_components function converts the filter inputs into a format that can readily be appended to the url
        ESearch_URL_List=x.make_url_filtered()                                      #The make_url_filtered functions takes a specialized mechanism to include the filter components into the urls for the gene items      
    return ESearch_URL_List                                                         #The Making_URL_1 function returns the list of ESearch URLs, one for each gene item specified by the user
                                        
#The AccessingESearchDatabse function is used to obtain the information content specified in the ESearch Domain of the Entrez system. Because each gene
#Items has its own URL, there is a unique domain for each gene item as well, and the information therein must be accessed an stored for each gene item,
#In particular, the unique web environment created for each gene item. The function acquires all of the content specified by the ESearch url for each gene 
#In a nested list by calling the Accessing_URL class from the LitFinderUtilityFile, which uses the access_method_a function to open each url and acquire its content 
def AccessingEsearchDatabase(Esearch_URL_List):
    x=LitFinderUtilityFile.Accessing_URL(ESearch_URL_List)                          #The Accessing_URL class from LitFinderUtilityFile on the ESearch_URL_List
    ESearch_Content=x.access_method_a()                                             #The access_method_a function from the Accessing_URL class is called and generates content from each ESearch URL
    return ESearch_Content                                                          #The content of each ESearch_URL is returned as a nested list

#The MakingURL2 function iterates over the content from each ESearch URL (which specifies the domain content for each gene item from the first url)
#And searches for where the Web Environment is specified. Because the content Is stored as a list, acquiring the web environment for each gene item is as simple
#As splicing it out of the list for each item. With the web environment now accessed, A unique URL can be created for each gene item again which 
#Specifies the location in the EFetch domain of the Entrez system where the literature for each gene item can be acquired. The function first invokes
#The Parsing_File class from the LitFinderUtilityFile on the content from each ESearch URL. The parse_method_b function from the class is called, taking
#A parameter specifying the limit of the output (the maximum number to search for) and also the items to parse for. This extracts the webenvironment from each
#ESearch URL. The Generating URL class is then called from the UtilityFile, and because it does not need to be filtered, the make_url function is called 
def Making_EFetch_URL(ESearch_Content, outputlimit):
    x=LitFinderUtilityFile.Parsing_File(ESearch_Content, outputlimit)               #The Parsing_File class from the LitFinderUtilityFile is called on the content of the ESearch database and output limit is specified by the LitFinderParameterFile
    extract_list=x.parse_method_a('<WebEnv>','</WebEnv>')                           #The parse_method_a function from the Parsing_File class is called with parsers to extract the web environment from each ESearch url
    y=LitFinderUtilityFile.Generating_URLs()                                        #The Generating_URL class from the LitFinderUtilityFile is called to generate urls using the web environment
    y.add_ons(LitFinderUtilityFile.calling_objects("EFetch")[0], extract_list,      #The add_on function is invoked with the ESearch entrez location and the web environments are included
              LitFinderUtilityFile.calling_objects("EFetch")[1],                    #The specialized EFetch base is invoked
              LitFinderUtilityFile.calling_objects("EFetch")[2])                    #The specialized terminator for the EFetch location is specified
    EFetch_URL_List=y.make_url()                                                    #These urls do not need to be filtered as this is accomplished with the ESearch URLs so the make_url function is called
    return EFetch_URL_List                                                          #The Making_EFetch_URL function returns the list of EFetch_URLs for each gene item

#The Generating_Literature_Data function is used to access the content from the EFetch database for each gene and subsequently extract the DOI number and
#PMID number associated with each Paper. This is then compiled into a data array for the purpose of creating a dataframe specifying the total literature existing with regards to a 
#Specific gene. This is accomplished by accessing the EFetch URL and parsing the locations of DOI and PMID using the Accessing_URL and Parsing_File classes
def Generating_Literature_Data(EFetch_URL_List, outputlimit):
    w=LitFinderUtilityFile.Accessing_URL(EFetch_URL_List)                           #The Accessing_URL class from LitFinderUtilityFile is called on the list of EFetch_URLs
    content=w.access_method_b()                                                     #The content of each EFetch URL is acquired and stored using the access_method_b function from the Accessing_URL class
    x=LitFinderUtilityFile.Parsing_File(content, outputlimit)                       #The Parsing_File class is called on the content of the EFetch database and specifies the output limit, same as previous
    DOI_Data=x.parse_method_b("DOI:")                                               #The parse_method_b function is called from the Parsing_File class and specifies the DOI to be acquired
    Flat_DOI_List=DOI_Data[0]                                                       #The output at position 0 specifies the comprehensive flat list of DOIs
    Nested_DOI_List=DOI_Data[1]                                                     #The output at position 1 specifies the nested list of DOIs associated with each gene item
    DOI_Num=DOI_Data[2]                                                             #The output at position 2 specifies the number of DOIs associated with each gene item
    y=LitFinderUtilityFile.Parsing_File(content, outputlimit)                       #The Parsing_File class is called again from the LitFinderUtilityFile on the content of the ESearch database
    PMID_Data=y.parse_method_b("PMID:")                                             #The parse_method_b function is called from the Parsing_File class and specifies the PMID to be acquired
    Flat_PMID_List=PMID_Data[0]                                                     #The output at position 0 specifies the comprehensive flat list of PMIDs
    Nested_PMID_List=PMID_Data[1]                                                   #The output at position 1 specifies the nested list of PMIDs associated with each gene item
    PMID_Num=PMID_Data[2]                                                           #The output at position 2 specifies the number of PMIDs associated with each gene item
    z=LitFinderUtilityFile.BuildingDataFrame(Nested_DOI_List, Nested_PMID_List[:])  #The dataframe is constructed by calling the BuildingDataFrame class from LitFinderUtilityFile with the two nested lists
    dataarray = z.list_conversion()                                                 #The list_conversion function zips the nested lists together alternating DOI and PMID
    return Nested_PMID_List, Nested_DOI_List, Flat_PMID_List, dataarray, DOI_Num, Flat_PMID_List
    
#The GeneratingDataFrame function serves to compile the DOIs and PMIDs into A user friendly format, and associate these values with their respective genes
#From which they derive.This function also creates a collective array possessing The gene names and also associating with each of these genes their own respective value
def GeneratingDataFrame(Gene_List, dataarray, DOI_Num):
    new_gene_list=[]                                                                #This serves as an empty list to create a gene list where each gene is doubly present to associate it with both DOI and PMID
    for gene in Gene_List:                                                          #This for loop is created to double every item in the list
        new_gene_list.append(gene)                                                  #These functions append the new item to the  list
        new_gene_list.append(gene)                                                  #This function ensures that the gene is represented twice each time in the list
    ctr=0                                                                           #Ctr serves to account for the number of genes in constructing the dataframe
    for item in Gene_List:                                                          #For each gene, the ctr is increased
        ctr+=1                                                                      #Each gene increases the value of counter by one
    Header=(['DOI']+['PMID'])*ctr                                                   #The header is the number of genes and attaches to each gene the label "DOI" and "PMID"
    arrays=[np.array(new_gene_list),                                                #This creates the array to serves as the index for the dataframe. The indexes are based off of the gene item and its respective DOI/PMID
            np.array(Header)]                                                       #The arrays utilizes the numpy library to construct the values in proper format
    df=pd.DataFrame(dataarray, index=arrays)                                        #This function creates the panda dataframe with the DOIs & PMIDs specifying the data while the dataarray specifies the index
    return df                                                                       #The GeneratingDataFrame function returns the constructed dataframe                                             
def Generating_Bar_Graph(Gene_List, dataarray, DOI_Num):                            #The GeneratingBarGraph function operates similarly but rather, produces bar graph rather than general frame
    bar_graph=pd.DataFrame({"Genes":Gene_List, "Number of Papers":DOI_Num})         #The barplot utilizes the data held in the gene list and uses the number of papers for each gene
    ax=bar_graph.plot.bar(x="Genes", y="Number of Papers", rot=0)                   #The x axis is constituted by the genes while the y axis is constituted by the number of papers
    return bar_graph                                                                #The Generating_Bar_Graph function returns a bar graph of the data, the number of papers per gene item    
#In order to generate citation data, new databases needed to be accessed in order to acquire the citation numbers for each paper. For this reason, each paper was
#Compiled into a list, and this list was then iterated through to develop the ESearch URL. The content of each URL was then stored in a separate list. This comprehensive
#List of PMIDs was then used to create batches, a maximum of 189 PMIDs in each (as permitted by Entrez in a given search) and joined together. The Generating_URL class
#From the LitFinderUtilityFile then creates a EPost URL for each Batch
def Accessing_PMID_File(Flat_PMID_List):                                                                          
    Batch_List=[Flat_PMID_List[PMID:PMID+189] for PMID in                           #List comprehension takes items from the flat list and converts them into batches of 189 
                range(0, len(Flat_PMID_List), 189)]                                 #The use of the list comprehension rather than a for-loop increases the efficiency of the program
    NewBatchList=[]                                                                 #The NewBatchList serves as a list of the batches, but with the items being joined together in a string
    for item in Batch_List:                                                         #The for loop iterates through each batch in the list and joins its contents together in a single string so it can be used to generate the urls
        NewBatchList.append(",".join(item))                                         #The join function joins the items together at commas
    x=LitFinderUtilityFile.Generating_URLs()                                        #The Generating_URL class is called from the LitFinderUtilityFile on the NewBatchList to generate the EPost URLs
    x.add_ons(LitFinderUtilityFile.calling_objects("Epost")[0], NewBatchList,       #The add_on function is called from the Generating_URL class and takes parameters specifying the location as EPost
              LitFinderUtilityFile.calling_objects("Epost")[1],                     #The unique base of the EPost URL os specified
              LitFinderUtilityFile.calling_objects("Epost")[2])                     #The unique suffix of the EPost url is also specified
    EPost_URLs=x.make_url()                                                         #The make_url function from the Generating_URL class then generates a new url for each batch
    y=LitFinderUtilityFile.Accessing_URL(EPost_URLs)                                #The Accessing_URL class is called from the LitFinderUtilityFile and requests access to the content of each EPost URL
    Content_Citation_Data=y.access_method_a()                                       #The content of each EPost URL is acquired and stored using the access_method_a function from the Accessing_URL class
    return Content_Citation_Data                                                    #The content of each EPost URL is returned as a nested list

#With the contents of the first database compiled, the WebEnvironment was parsed Out of the content of the first URL. Once the WebENvironment was acquired, it is
#Inserted into the URL generator for the ESummary URL, and those URLs are compiled. These URLs are generated first by accessing the webenvironment by parsing the
#Result of the EPost URLs (using the Parsing_File class in LitFinderUtilityFile) and then generating the ESummary URLs with the Generating_URL class
def Generating_Esummary_URLs(Content_EPost_Data, output_limit):
    x=LitFinderUtilityFile.Parsing_File(Content_EPost_Data, output_limit)           #The Parsing_File class from the LitFinderUtilityFile is called on the content of the EPost URL and specifies the output limit
    extract_list=x.parse_method_a("<WebEnv>", "</WebEnv>")                          #The parse_method_a function from the Parsing_File class specifies the Webenvironment to be parsed out
    y=LitFinderUtilityFile.Generating_URLs()                                        #The Generating_URL class is then called to produce ESummary URLs using the web environment
    y.add_ons(LitFinderUtilityFile.calling_objects("ESummary")[0], extract_list,    #The add_on function from the Generating_URL class is called and ESummary location is specified, and webenvs specified as iterable item
              LitFinderUtilityFile.calling_objects("ESummary")[1],                  #The unique ESummary base is specified
              LitFinderUtilityFile.calling_objects("ESummary")[2])                  #the unique ESummary suffix is specified
    ESummary_URL_List=y.make_url()                                                  #The make_url function from the Generating_URL class is called to produce the ESummary URLs
    return ESummary_URL_List                                                        #The Generating_ESummary_URL function returns the list of ESummary URLs

#The Accessing Citation Data function iterates through each item of the Esummary URL list and subsequently requests access to each of these ESummary URLs
#To access the citation numbers for each of the papers, a while loop is used To index for the position where 'Name=PMCRefCount' is present. This is
#Accomplished by calling the Access_Parse class from the LitFinderUtilityFile module
def Accessing_Citation_Data(ESummary_URL_List):
    x=LitFinderUtilityFile.Access_Parse(ESummary_URL_List, 'Name="PmcRefCount"')    #The Access_Parse class is called from the LitFinderUtilityFile and specifies the Esummary List as iterable and to parse for Name="PmcRefCount" 
    content=x.manipulate()                                                          #The manipulate function from the Access_Parse class is called to return the location of the PmcRefCount
    return content                                                                  #The Accessing_Citation_Data returns a nested list of the location of the citation data in the ESummary content

#The position of the item from the PMCRefCount list is then iterated Through. Because the content of the URL is stored in a list,
#In order to access the Citation number, the position +1 relative to the PMCRefCount is indexed for. The citation number is then stored in its own list
#This is accomplished by using the Parsing_File class specifying location of citation information then generating the panda dataframe
def Generating_Citation_Data(PMID_Citation_List, PMID_List, output_limit):
    y=LitFinderUtilityFile.Parsing_File(PMID_Citation_List, output_limit)           #The Parsing_File class from the LitFinderUtilityFile is called specifying the citation data to be iterated over
    List=y.parse_method_a('Type="Integer">', '</Item>', "yes")                      #The parse_method_a function from the Parsing_File class is called and specifies the location where citation data is stored
    citation_ctr=str(len(List))                                                     #The number of citations found is procured by accounting for the length of the citation list and is converted to a string for export
    PMID_df = pd.DataFrame({"Citation_Number_List":List}, index=PMID_List)          #The dataframe is produced using the citation list and indexing in accordance with the list of PMIDs       
    PMID_bar_graph=pd.DataFrame({"Citation_Number_List":List}, index=PMID_List)     #The bar graph of citation data is also procured in accordance with the list of PMIDs 
    return List, PMID_df, PMID_bar_graph, citation_ctr                              #The GeneratingCitationData function returns the list of citations, as well as the data frames and number of citations


#The MetaAnalysis function serves an analytical purpose in that it returns the most cited papers, the maximum number being specified
#In the LitFinderParameter File. This is accomplished using the BuildingDataFrame class from the LitFinderUtilityFile
def MetaAnalysis(Citation_Number_List, Flat_PMID_List, Large_PMID_List, citation_limit):
    x=LitFinderUtilityFile.BuildingDataFrame(Citation_Number_List, Flat_PMID_List)  #The BuildingDataFrame class from the LitFinderUtilityFile is called on the citation and PMID lists 
    PMIDs=x.top_ten(Large_PMID_List, citation_limit)                                #The top_ten function from the BuildingDataFrame class returns the top citations for each gene
    New_Citation_DataFrames=pd.DataFrame({"Top Ten Most Cited PMIDs":PMIDs},        #The dataframe is constructed based upon each PMID
                                         index=L)                                   #The dataframe is made in accordance with each gene item specified by the user input in the LitFinderParameterFile
    return New_Citation_DataFrames                                                  #The MetaAnalysis function returns the citation dataframe

          
        
#Using the lists from the citation number and the list of the PMIDs A data frame was generated using pandas to correlate the PMID paper
#Number to the number of times it was cited. This was then used to create A second data frame which was then applied to create the bar plot. The various
#Plots created were then modified using xlsx writer and exported as an excel file
def Citation_Data_Frame(FileName2, df, bar_graph, PMID_df, PMID_bar_graph, New_Citation_DataFrame, citation_ctr, num_genes):
    writer=pd.ExcelWriter(FileName2, engine='xlsxwriter')
    #The following functions export the respective dataframes to excel using xlsx writer
    df.to_excel(writer, sheet_name='ComprehensiveData',                             #This function exports the DOI/PMID dataframe
                index = True, header=True)                                          #The index must be true and a header must be included
    bar_graph.to_excel(writer, sheet_name="GraphicalModel",                         #This function exports the DOI bargraph
                       index = True, header=True)                                   #The index must be true and a header must be included   
    PMID_df.to_excel(writer, sheet_name='ComprehensiveCitationData',                #This function exports the citation dataframe as a csv file to excel
                     index = True, header=True)                                     #The index must be true and a header must be included
    PMID_bar_graph.to_excel(writer, sheet_name="CitationModel",                     #This function exports the citation bargraph
                            index = True, header=True)                              #The index must be true and a header must be included
    New_Citation_DataFrame.to_excel(writer, sheet_name="CitationsSorted",           #This function exports the citation dataframe
                                    index=True, header=True)      
    #These functions are used for modifying the data so that the bar plot may correctly interpret values
    workbook=writer.book                                                            #The workbook is created
    worksheet=writer.sheets['GraphicalModel']                                       #The sheet is specified
    chart1=workbook.add_chart({"type":"column"})                                    #The chart-type is specified as a bar graph
    chart1.add_series({"categories":"=GraphicalModel!$B$2:$B$" + num_genes,         #Genes serve as the category while the number of papers serves as the value. The offset is accounted for
                       "values":"=GraphicalModel!$C$2:$C$"+num_genes})     
    #The following functions format the chart for the number of papers
    chart1.set_title({'name':'Number of Published Papers With Respect To A Specific Gene'})     
    chart1.set_x_axis({"name":"Gene Names"})                                        #This function specifies the x axis
    chart1.set_y_axis({"name":"Number of DOIs"})                                    #This function specifies the y axis
    worksheet.insert_chart("F2", chart1)                                            #This function specifies the location of the chart in excel
    #These functions are used for modifying the data so that the bar plot May interpret the values and indices correctly
    workbook=writer.book                                                            #The workbook is created
    worksheet2=writer.sheets['CitationModel']                                       #The sheet is specified
    chart2=workbook.add_chart({"type":"column"})                                    #The chart-type is specified as a bar graph
    chart2.add_series({"categories":"=CitationModel!$A$2:$A$" + citation_ctr,       #Genes serve as the category while the number of papers serves as the value. The offset is accounted for
                       "values":"=CitationModel!$B$2:$B$"+citation_ctr})            #Genes serve as the category while the number of papers serves as the value. The offset is accounted for   
    #The following functions format the chart for the number of papers
    #For each specific genes. This includes the specification of paper title
    #The axes, and specifies the location of the chart in Excel
    chart2.set_title({'name':'Number of Citations with Respect to a Specific Gene'})    #This function specifies the chart title
    chart2.set_x_axis({"name":"PMIDs"})                                             #This function specifies the x axis
    chart2.set_y_axis({"name":"Number of Citations"})                               #This function specifies the y axis
    worksheet2.insert_chart("F2", chart2)                                           #This function specifies the location of the chart in excel

    writer.save()                                                                   #This saves the data to the Excel File specified

##########################################################################################################
############################ Execution of the Program ####################################################
##########################################################################################################
maxima=9999999999999999                                                                                 #Maxima serves as an automatic input for the output limit
User_Input_Info=Accessing_User_Input(LitFinderParamFile.input_type, LitFinderParamFile.user_input_file) #This calls the Accessing_User_Input function above, specifying the input type from the parameter file 
L=User_Input_Info[0]                                                                                    #The L variable stores the list of gene items                                                                                       
num_genes=User_Input_Info[1]                                                                            #The num_genes variable stores the number of genes being investigated
ESearch_URL_List = Making_URL_1(L, LitFinderParamFile.filter_option)                                    #The Making_URL_1 function is called using the gene list and includes the option for filtering as stipulated by the LitFinderParameterFile
ESearch_Content=AccessingEsearchDatabase(ESearch_URL_List)                                              #The Accessing_ESearch_Database function is called based upon the ESearch_URL_List and stores the content of each ESearch URL
EFetch_URL_List = Making_EFetch_URL(ESearch_Content, maxima)                                            #The Making_EFetch_URL is called on the content of the ESearch database, parses out the webenv, and creates the EFetch URL
if LitFinderParamFile.output_limit==0:                                                                  #In the event that the user does not impose an output limit via the LitFinderParameter file...
    All_Content=Generating_Literature_Data(EFetch_URL_List, maxima)                                     #The Generating_Literature_Data function is called on the EFetch_URL_List without limitations to parse
elif LitFinderParamFile.output_limit==1:                                                                #In the event that the user imposes an output limit via the LitFinderParameterFile... 
    All_Content=Generating_Literature_Data(EFetch_URL_List, LitFinderParamFile.output_limits)           #The Generating_URL_Function is called on the list of EFetch URLs and imposes a limit on output
df=GeneratingDataFrame(L, All_Content[3], All_Content[4])                                               #The GeneratingDataFrame function is called on the gene list, includes DOIs and PMIDs to produce df
bar_graph=Generating_Bar_Graph(L, All_Content[3], All_Content[4])                                       #The GeneratingBarGraph function is called including the gene list, includes DOIs and PMIDs
if LitFinderParamFile.citation_data == 0:                                                               #If the user elects to receive citation data on the papers procured
    Content_EPost_Data=Accessing_PMID_File(All_Content[2])                                              #The Accessing_PMID_File is called on the flat list of PMIDs generated
    ESummary_List=Generating_Esummary_URLs(Content_EPost_Data, LitFinderParamFile.output_limits)        #The Generating_ESummary_URLs function is called on the output of the EPost URLs and imposes a limit specified via the LitFinderParameterFile
    PMID_Pos_List=Accessing_Citation_Data(ESummary_List)                                                #The Accessing Citation_Data function is called on the ESummary_List and acquires content of each and stores locaion where citation data is specified
    Citation_Number_List=Generating_Citation_Data(PMID_Pos_List, All_Content[2], maxima)[0]             #The Generating_Citation_Data function is called on the positions of the citation data and parses it out, returning citation data for each PMID
    citation_ctr=Generating_Citation_Data(PMID_Pos_List, All_Content[2], maxima)[3]                     #The Generating_Citation_Data function is called on the positions of the citation data and returns the number of citations procured              
    PMID_df=Generating_Citation_Data(PMID_Pos_List, All_Content[2], maxima)[1]                          #The Generating_Citation_Data function is called on the positions of the citation data and produces the dataframe
    PMID_bar_graph=Generating_Citation_Data(PMID_Pos_List, All_Content[2], maxima)[2]                   #The Generating_Citation_Data function is called on the positions of the citation data and yields the bar graph
    Flat_PMID_List=All_Content[5]                                                                       #The list of all PMIDs is procured
    Large_PMID_List=All_Content[0]                                                                      #The nested list of PMIDs is procured
    New_Content_Citation_Data= MetaAnalysis(Citation_Number_List, Flat_PMID_List,                       #The MetaAnalysis function is called to yield the most cited papers, it requires the citation list and PMIDs
                                            Large_PMID_List, LitFinderParamFile.citation_limit)         #The function also requires the nested PMID list to serve as an index and the limit specifying how many of each to yield
    Citation_Data_Frame(LitFinderParamFile.output_file, df, bar_graph, PMID_df, PMID_bar_graph,         #The Citation_Data_Frame function is called on the comprehensive list of data and exports the data
                        New_Content_Citation_Data, citation_ctr, num_genes)                             #The Citation_Data_Frame function is called on the comprehensive list of data and exports the data
elif LitFinderParamFile.citation_data==1:                                                               #If, however, the user elects to skip citation data...
    Citation_Data_Frame(LitFinderParamFile.output_file, df, bar_graph, citation_ctr, num_genes)         #The program ends prematurely, exporting only the raw data 
##########################################################################################################
############################### End of Program Execution #################################################
##########################################################################################################
