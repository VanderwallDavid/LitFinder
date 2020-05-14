


def Discerning_User_Input():
    Single_or_List=str(input("Will the user be searching a single gene or a gene list (Input 'single' or 'list')"))
    if Single_or_List=="list" or Single_or_List=="List":
        Input = str(input("Type the name of the file possessing protein names"))
    
    elif Single_or_List=="single" or Single_or_List=="Single":
        Input=str(input("Input the name of a gene, its four character identifier, Entrez ID, or acession ID"))
    
    return Input
def Filter_Option():
    FilterOption=str(input("Would you like to filter the literature results? (Acceptable answers are 'y' or 'n'"))
    return FilterOption

def Specifying_File_Location():
    UserFile=str(input("""The dataframe has successfully been created! We will now export the file to the location you specify. Please type the name of your user file"""))     #Filename asks the user to input their user file
    File2=str(input("Now, give the file a name of your choosing"))
    return UserFile, File2

if __name__ == '__main__':
    Discerning_User_Input()
    Filter_Option()


    


