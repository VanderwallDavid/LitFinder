import requests
import urllib.request

class Generating_URLs:
    def __init__(self, database='pubmed', base='https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'):
        self.database=database
        self.base=base
        self.url_list=[]

    def add_ons(self, entrez_location, iterable, other, terminator):
        self.iterable=iterable
        self.entrez_location=entrez_location
        self.other=other
        self.terminator=terminator
       
    def make_url(self):
        for item in self.iterable:
            self.url=self.base+self.entrez_location+self.database+self.other+item+self.terminator
            self.url_list.append(self.url)
        print(self.url_list)
        return(self.url_list)


class Accessing_URL(Generating_URLs):
    def __init__(self, url_list):
        self.url_list=url_list
        self.Stored_Content=[]
    def access_method_a(self):
        for item in self.url_list:
            res=requests.get(item)                              #This function obtains access to the ESearch URL
            type(res)                                           #This function converts the URL content to an accessible type
            Content_List=[]                                     #This creates a list to put the data from the first database in
            for line in res:                                    #This for loop iterates through the content of the first database 
                Content_List.append(line)                       #This inserts each line of the first database into the list
            self.Stored_Content.append(str(Content_List))  #This converts the list to a string and appends it to the greater list
        print(self.Stored_Content)                         #The content of the database is visibly printed for the user to see
        return self.Stored_Content
    def access_method_b(self):
        for item in self.url_list:
            request = urllib.request.Request(item)                   #The request function requests access to the contents of the EFetch domain
            result = urllib.request.urlopen(request)                #The urlopen function opens the URL specifying the EFetch domain content
            resulttext = result.read()                              #The read function iterates through the content of the EFetch domain
            resulttext = resulttext.decode("utf-8")                 #The EFetch domain is encoded in utf-8, so this is converted to a string
            resulttext = resulttext.split()                         #The split function converts the content into a list format so it can be properly indexed
            self.Stored_Content.append(resulttext)
        return self.Stored_Content
        


class Parsing_File(Accessing_URL):
    def __init__(self, iterable):
        self.iterable=iterable
        self.extract_list=[]
        self.ctr=0
        self.dataarray=[]
        
        

    def parse_method_a(self, start, end):
        self.start=start
        self.end=end
        for item in self.iterable:
            extract = item[item.index(self.start)+len(self.start):item.index(self.end)]
            self.extract_list.append(extract)
        print(self.extract_list)
        return self.extract_list

    def parse_method_b(self, ParseItem):
        self.ParseItem=ParseItem
        IndexPos1=0
        print(len(self.iterable))
        while IndexPos1<len(self.iterable):
            try:
                PosParseItem=self.iterable.index(self.ParseItem, IndexPos1)
                Item=self.iterable[PosParseItem+1]
                self.extract_list.append(item)
            except ValueError as e:
                break
        print(self.extract_list)
        return self.extract_list
            
                
            
        
            
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
        other="&id"
        terminator="&usehistory=y&api_key=bdffca2574be220a97265443eac517df0708"
    elif Entrez_Location=="ESummary" or Entrez_Location=="Esummary":
        entrez_location="esummary.fcgi?db="
        other="query_key=1&WebEnv="
        terminator="&rettype=abstract&retmode=text"
    return entrez_location, other, terminator




    
        
    
