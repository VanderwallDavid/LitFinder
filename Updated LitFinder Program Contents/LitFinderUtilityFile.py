import requests
import urllib.request
import json
import LitFinderParamFile

#The Organizing_User_Input class serves to  take account of the input format specified by the user
#In the LitFinderParameterFile, whether that be in the form of a list input or manual input
class Organizing_User_Input():
    def __init__(self, user_input):                                         #The __init__method serves to initialize the input parameter, as well as provide a location for the list to be generated and an account of the number of input items
        self.user_input=user_input                                          #self.user_input serves as a reference to the input type specified via the LitFinderParameterFile
        self.item_list=[]                                                   #Self.item_list serves to collect the input items in a centralized location
        self.item_number=1                                                  #The self.item_number serves to store the number of inputs

    def manipulating_list(self):                                            #The manipulating_list function serves the operation of converting a user input file into a list
        f=open(self.user_input, "r")                                        #The function must first open the input file specified by the user in the LitFinderParameterFile
        for line in f:                                                      #The for loop iterates through each line of the input file
            line=line.rstrip()                                              #The input file is stripped             
            line=line.split()                                               #The lines are split accordingly             
            self.item_list+=line                                            #The item is appended to the list as astring             
            self.item_number+=1                                             #The value of the gene items increases by one
        self.item_number=str(self.item_number)                              #The self.item_number is converted to a string for use in the dataframe
        return self.item_list, self.item_number                             #The manipulating list function returns the input list and the number of items

    def manipulating_individual(self):                                      #The manipulating individual function serves to convert manual inputs into a centralized list                        
        for item in self.user_input:                                        #The for loop iterates through each item manually inserted by the user in the LitFinderParameterFile
            self.item_list+=str(item)                                       #The item is apended to the self.item_list as a string
            self.item_number+=1                                             #The value of the number of items increases by one
        return self.item_list, str(self.item_number)                        #The manipulating individual function returns the input list as well as number of items

#The Generating_URLs class serves as a class for producing a list of url's dependent upon input options of
#The user specified in the LitFinderParameterFile, as well as iterable item specified 
class Generating_URLs:
    def __init__(self, database='pubmed',                                   #The __init__ method initializes parameters for the generation of url's, one of these automatically included is the database
                 base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'):    #The base of the entrez system is also included
        self.database=database                                              #Self.databse specifies the database being searched through for data
        self.base=base                                                      #The self.base value serves as the typical base of every entrez url
        self.unfiltered_url_list=[]                                         #The unfiltered list serves as a centralized location for storing urls produced under unfiltered conditions, specified in LitFinderParameterFile
        self.filtered_list=[]                                               #The filtered list serves as a centralized location for storing urls produced under filtered conditions, specified in LitFinderParameterFile
        
    def add_ons(self, entrez_location, iterable, other, terminator):        #The add_on function serves to stipulate url dependent parameters which will be specified in the execution file
        self.iterable=iterable                                              #Self.iterable refers to the iterable item which will be used in the creation of the url
        self.entrez_location=entrez_location                                #The self.entrez_location indicates the portion of the entrez system which will be searched
        self.other=other                                                    #Self.other refers to the unique portion of the url specific to the entrez location
        self.terminator=terminator                                          #The self.terminator refers to the unique suffix of the url which is also dependent on the entrez location being searched
                
    def make_url(self):                                                                                 #The make_url function generates the urls using the above parameters, only under unfiltered conditions
        for item in self.iterable:                                                                      #For every item in the iterable unit (such that a url is produced for each item)..
            if self.entrez_location=="ESearch":                                                         #An alternative option is provided for ESearch urls as an organism needs to be specified                                                         
                self.url=self.base+self.entrez_location+self.database+self.other+item+self.terminator   #The unfiltered ESearch url utilizes all of the above parameters as well as the organism searched
                self.unfiltered_url_list.append(self.url)                                               #Each url procured is appended to the self.unfiltered_url_list
            else:                                                                                       #If the location specified is not ESearch and filtering is not required
                self.url=self.base+self.entrez_location+self.database+self.other+item+self.terminator   #The url consists only of the above parameters, does not include an organism search
                self.unfiltered_url_list.append(self.url)                                               #Each url is still appended to the unfiltered list as the filter option was not specified
        return self.unfiltered_url_list                                                                 #The make_url function returns the unfiltered list as all of these are used for unfiltered urls
    
    def filter_items(self, keyword=None, journal=None, year=None):          #The filter_items functions specify the filter options stipulated by the LitFinderParameterFile
        self.keyword=keyword                                                #Self.keyword refers to the available keyword filters applied by the LitFinderParameterFile
        self.journal=journal                                                #Self.journal refers to the available journal filters applied by the LitFinderParameterFile
        self.year=year                                                      #Self.year refers to the available year filters applied by the LitFinderParameterFile
        self.filtered_url_list=[]                                           #The self.filtered_url list serves as a centralized location for the storage of urls which have been filtered
    def filter_components(self):                                            #The filter_components function serves the role of converting the keywords into a format which may be applied to the producing urls
        filter_list=[]                                                      #Filter_list serves as an initial location to store the filter components as strings
        if LitFinderParamFile.filter_keyword==1:                            #If the filtering of a keyword is specified by the LitFinderParameterFile...
            filter_list.append(self.keyword)                                #Those keywords are appended to the filter_list
        if LitFinderParamFile.filter_journal==1:                            #If the filtering of a journal is specified by the LitFinderParameterFile...
            filter_list.append(self.journal+"[journal]")                    #Those journals are appended to the filter_list with the suffix [journal]
        if LitFinderParamFile.filter_year==1:                               #If the filtering of a year is specified by the LitFinderParameterFile...
            filter_list.append(self.year+"[pdat]")                          #Those years are appended to the filter_list with the suffix [pdat]
        self.new_filter_list=''                                             #The self.new_filter_list serves as an empty string to store filter parameters in a format that can be appended to the url
        if filter_list!=[]:                                                 #This stipulates a circumstance wherein the filter list is not empty
            for item in filter_list[:-1]:                                   #For every item in the list except for the last one
                self.new_filter_list+=item+"+AND+"                          #An '+AND+" must be inserted between each
            self.new_filter_list+=filter_list[-1]                           #The final item of the filter_list is then appended to the new_filter_list string
        else:                                                               #If the filter list is however empty, in circumstances wherein no filters have been added
            self.new_filter_list=''                                         #Then the self.new_filter_list will be an empty string
    def make_url_filtered(self):                                            #The make_url_filtered function serves for the generation of filtered urls and stores them in a centralized list
        for item in self.iterable:                                          #The for loop iterates through each item of the iterable list
            self.url=self.base+self.entrez_location+self.database+self.other+LitFinderParamFile.organism_name+"[orgn]+AND+"+item+self.new_filter_list+self.terminator
            self.filtered_url_list.append(self.url)                         #Each url produced is appended to the self.filtered_url_list
        return self.filtered_url_list

#The Accessing_URL class serves as a subclass to the Generating_URL class, and provides methods for accessing
#The contents of the urls produced by the above class
class Accessing_URL(Generating_URLs):
    def __init__(self, url_list):                                           #The __init__ method serves to initialize the url_list provided as an input
        self.url_list=url_list                                              #Self.url_list serves as the source of content to be procured

    def access_method_a(self):                                              #The access_method_a function serves to yield contents of the url as a json file
        json_obj_list=[]                                                    #The json_obj_list serves to store the content of each url in a nested list
        for item in self.url_list:                                          #Each available url is iterated through
            resp_text = urllib.request.urlopen(item).read().decode('utf-8') #A request is made to open, read, and decode the url content
            json_obj_dict=json.loads(json.dumps(resp_text))                 #The content is then converted to dictionary format for easy parsing
            json_obj_list.append(json_obj_dict)                             #The dictionary is then appended to the nested list
        return json_obj_list                                                #The access_method_a function returns the dictionary list

    def access_method_b(self, parse='no'):                                  #The access_method_b provides an alternative, using urllib reques to obtain the content
        object_list=[]                                                      #The content is stored directly as a list in object_list
        for item in self.url_list:                                          #The for loop iterates through each available url specified in the input
            request = urllib.request.Request(item)                          #A request is made for each url                
            result = urllib.request.urlopen(request)                        #The text is stored in an extraneous location            
            resulttext = result.read()                                      #The content is then read through               
            resulttext = resulttext.decode("utf-8")                         #The content must be decoded from utf-8              
            resulttext = resulttext.split()                                 #The content is split
            object_list.append(resulttext)                                  #The content of each url is then appended to the object_list
        return object_list                                                  #The access_method_b function returns the object_list containing the content of each url
        
#The Parsing_File class provides several methods for extracting information from the contents of various urls.
#Because the contents being parsed are dervied from the urls being accessed, this class is a subclass of Accessing_URL
class Parsing_File(Accessing_URL):
    def __init__(self, iterable, outputlimit):                              #The __init__ method serves to initialize parameters for the execution of the inherent functions
        self.iterable=iterable                                              #self.iterable serves as the content list do be iterated through
        self.outputlimit=outputlimit                                        #The self.output_limit parameter, when used, places an upper limit on the number of items to be parsed
               
    def parse_method_a(self, start, end, num="no"):                         #The parse_method_a function takes a start and stopping point and extracts the item between these locations, useful for obtaining items within strings
        self.num=num                                                        #self.num provides an option for when numbers are being extracted, if they are, they are converted from string to int
        self.start=start                                                    #self.start serves as the initial location to commence parse
        self.end=end                                                        #self.end serves as the final location for executing parse
        extract_list=[]                                                     #Extract_list serves as the centralized location for yielding output of the parse
        for item in self.iterable:                                          #For every item within the iterable list      
            extract = item[item.index(self.start)+len(self.start):          #Index the iterm and account for the start
                           item.index(self.end)]                            #Additionally account for the end with self.end
            if self.num=="yes":                                             #In the event that the item being parsed is in fact a number
                extract_list.append(int(extract))                           #Parse out the number, convert it to integer and append it to the extract list
            elif self.num=="no":                                            #If, however, the parsed value is not an integers
                extract_list.append(extract)                                #Then simply append the item to the extract_list
        return extract_list                                                 #The parse_method_a function returns the list containing parsed out items

    def parse_method_b(self, ParseItem):                                    #The parse_method_b provides an additional option, specifying only a single parse location, useful for when items are in a list
        self.ParseItem=ParseItem                                            #Self.ParseItem specifies the object being searched for
        nested_list=[]                                                      #The nested list returns each of the parsed out items for each url
        number_of_items=[]                                                  #Number of items stores a list that specifies the number of items parsed out for each url
        flat_list=[]                                                        #flat_list converts the nested list to a flat list
        for item in self.iterable:                                          #The for loop iterates through each item of the nested content
            IndexPos=0                                                      #Serves as the position to index
            IndexPosList=[]                                                 #Stores the parsed out item for each in its own list
            ctr=0                                                           #Takes out the number of items parsed out for each
            while IndexPos<len(item) and len(IndexPosList)< self.outputlimit: #Proceeds to iterate when the index position has not reached the end of the item and the output limit has not been reached
                try:                                                        #Attempt:
                    if item[IndexPos]==self.ParseItem:                      #If the indexed item at the given location is in fact the parse item specified
                        PosParseItem=item.index(self.ParseItem, IndexPos)   #Then index the contents of the item at the location specified by indexpos and store it
                        IndexPosList.append(item[PosParseItem+1])           #Then append the item to the index pos list which serves as its own list for each item
                        flat_list.append(item[PosParseItem+1])              #Then also append to the flat list
                        ctr+=1                                              #The number of parsed out values has now increased by one
                        IndexPos+=1                                         #And it is indicated that the loop must now move to the next position and check
                    else:                                                   #If the item at the index position is not the same as the parse item being searched
                        IndexPos+=1                                         #The loop then simply moves on to the next location
                except ValueError as e:                                     #When the loop has reached its terminus
                    break                                                   #It shall terminate   
            nested_list.append(IndexPosList)                                #For each item, the unique list is appended to the nested list
            number_of_items.append(ctr)                                     #The number of parsed out items is also appended to the number of items list
        return flat_list, nested_list, number_of_items                      #The parse_method_b function returns the flat list, the nested list, and nuber of items

#The Access_Parse class is a dual method function which both obtains access to urls and iterates through them, parsing out items
class Access_Parse:
    def __init__(self, url_list, ParseItem):                                #The __init__ method initializes essential parameters for the functions including the url_list to be used and the item to be parsed
        self.url_list=url_list                                              #The self.url_list specifies the urls to be iterated through and accessed
        self.ParseItem=ParseItem                                            #When access has been obtained, the self.ParseItem specifies what item will be parsed out
    def manipulate(self):                                                   #The manipulate function requests access to the url and simultaneously parse
        component_list=[]                                                   #Serves as a list to store the positions of the parse items in the list
        for url in self.url_list:                                           #This for loop iterates over every content URL that has been acquired for each gene and obtains access to its contents
            request2 = urllib.request.Request(url)                          #The request function requests access to the contents of the EFetch domain               
            result2 = urllib.request.urlopen(request2)                      #The urlopen function opens the URL specifying the EFetch domain content        
            resulttext2 = result2.read()                                    #The read function iterates through the content of the EFetch domain        
            resulttext2 = resulttext2.decode("utf-8")                       #The content domain is encoded in utf-8, so this is converted to a string        
            resulttext2 = resulttext2.split()                               #The content is split accordingly
            indexPosList3 = []                                              #List storing the positions where output parse is specified
            indexPos3=0                                                     #Initial Index position is zero
            while True:                                                     #A while loop is used to iterate over every item of the list
                try:                                                        #'try' searches for the subsequent expressions
                    indexPos3 = resulttext2.index(self.ParseItem, indexPos3)#This function indexes  the position where the parse item is specified
                    indexPosList3.append(indexPos3)                         #This function appends the index position of parse item to the lst
                    indexPos3 += 1                                          #Because the parse item number is is specified at the index following where parse item is specified, 1 is added to the index
                except ValueError as e:                                     #If no other parse item are found, the while loop ceases
                    break                                                   #While loop terminates
            for pos3 in indexPosList3:                                      #The for loop is used to iterate over all the index positions where "parse item" is found     
                component_list.append(resulttext2[pos3 + 1])                #Because the DOI number is is specified at the index following where parse item is specified, 1 is added to the index      
        return component_list                                               #The manipulate function returns the parse items as a nested list
        
#The BuildingDataFrame class provides methods for converting raw data into usable content
class BuildingDataFrame:
    def __init__(self, iterableA, iterableB):                               #The __init__ method initializes the lists that will be used in constructing the dataframe
        self.iterableA=iterableA                                            #Self.iterableA specifies the first list to be used
        self.iterableB=iterableB                                            #Self.iterbaleB specifies the second list to be used
        self.dataarray=[]                                                   #Self.dataarray serves as the lcoation of the generated dara-array

    def list_conversion(self):                                              #The list conversion converts two nested lists into a single alternating list
        while True:                                                         #For the entirety of both lists
            try:                                                            #Execute
                self.dataarray.append(self.iterableA.pop(0))                #Extract the  item of the first list and append to dataarray
                self.dataarray.append(self.iterableB.pop(0))                #Extract the  item of the second list and append to data array
            except IndexError:                                              #Continue until the end of the first list has been reached
                break                                                       #Terminate the while_loop
        return self.dataarray                                               #This list conversion function returns the dataarray produced

    def top_ten(self, indexes, limit):                                      #The top_ten function returns the top number of citations for each gene listed
        self.limit=limit                                                    #The self.limit serves to specify the number of citation statistics permitted
        self.indexes=indexes                                                #self.indexes serves as a container for which to controlthe output data
        Zipped_Lists=([x for _,x in sorted(zip(self.iterableA, self.iterableB), reverse=True)]) #The two lists are combined together
        Which_Sublist=[]                                                    #Stores each PMID with its particular sublist together
        for PMID in Zipped_Lists:                                           #Because there are two lists, the first for loop calls the PMID from the Zipped_List (so as to go through every paper)
            for sublist in self.indexes:                                    #The second for loop then calls the sublist of the index
                if PMID in sublist:                                         #This logical input essentially searches for the sublist where that PMID can be found
                    pos=self.indexes.index(sublist)                         #pos provides the location of the sublist
                    Which_Sublist.append((PMID,pos))                        #The PMID and its respective sublist are appended to which sublist
        ctrlist=[]                                                          #ctr_list accounts for how many sublists are present in the index
        ctr=0                                                               #The initial sublist is sublist 0
        for sublist in self.indexes:                                        #For loop iterates through each sublist of the index
            ctrlist.append(ctr)                                             #The sublist position is then appended to the ctrlist
            ctr+=1                                                          #The value of the counter then increases by one
        Ordered_List=[]                                                     #The ordered list combines the duos for each sublist into one list
        for number in ctrlist:                                              #For each value of the sublist
            Refined_List=[]                                                 #The refined list stores the PMID sublist duo for each sublist
            for PMID, sublist in Which_Sublist:                             #For the combination fo PMIDs and their sublist in the list Which_Sublist
                if sublist==number:                                         #If the sublist is the same as the sublist in the counter
                    Refined_List.append((PMID, sublist))                    #Then append the PMID sublist duo to the refined list
            Ordered_List.append(Refined_List)                               #Each PMID sublist duo is appended to the larger ordered list
        Filtered_List=[]                                                    #The Filtered_List stores the PMIDs with the highest citations for each gene
        for sublist in Ordered_List:                                        #For each sublist specified in the Ordered_List
            Filtered_List.append(sublist[:self.limit])                      #The top citations for each sublist are appended to the filtered list
        Just_PMIDs=[]                                                       #Just PMIDs stores the list of highest cited papers in order of magnitude
        for sublist in Filtered_List:                                       #For every sublist in the filtered list
            The_PMIDs=[]                                                    #Flat list for PMIDs
            for PMID, pos in sublist:                                       #For each PMID and position duo in the sublist
                The_PMIDs.append(PMID)                                      #Append only the PMID to the PMID list
            Just_PMIDs.append(The_PMIDs)                                    #Each item gets its own list appended to JustPMIDs
        return Just_PMIDs                                                   #The top ten function returns the most cited pmids and associates them with their citation number
 
       
def calling_objects(Entrez_Location):
    if Entrez_Location=="ESearch" or  Entrez_Location=="Esearch":
        entrez_location="esearch.fcgi?db="
        other="&term="
        terminator="&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"
    elif Entrez_Location=="EFetch" or Entrez_Location=="Efetch":
        entrez_location="efetch.fcgi?db="
        other="&query_key=1&WebEnv="
        terminator="&rettype=abstract&retmode=text"
    elif Entrez_Location=="EPost" or Entrez_Location=="Epost":
        entrez_location="epost.fcgi?db="
        other="&id="
        terminator="&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"
    elif Entrez_Location=="ESummary" or Entrez_Location=="Esummary":
        entrez_location="esummary.fcgi?db="
        other="&query_key=1&WebEnv="
        terminator="&rettype=abstract&retmode=text"
    return entrez_location, other, terminator




    
        
    
