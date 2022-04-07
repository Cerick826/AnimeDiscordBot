async def sortWatchList(wString):
    delim = ", "
    result = delim.join(sorted(wString.split(", ")))
    return result

# function to check special characters from database

async def check_format(formatString):
    #('',)
    if len(formatString) == 5 or len(formatString) == 0:
        return True
    #(' ',) 
    elif len(formatString) == 6 and formatString[4] == ',':
        return True
    else:
        return False   

async def check_ep_format(formatString):
    #('',)
   
    #(' ',)
    if formatString == "('',)":
        return True
    elif len(formatString) == 6 and formatString[4] == ',':
        if formatString[2] == '0' or formatString[2] == '1' or formatString[2] == '2' or formatString[2] == '3' or formatString[2] == '4' or formatString[2] == '5' or formatString[2] == '6' or formatString[2] == '7' or formatString[2] == '8' or formatString[2] == '9':
            return False
        else:
            return True
    
        
    else:
        return False   