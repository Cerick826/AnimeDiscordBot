async def sortWatchList(wString):
    delim = ", "
    result = delim.join(sorted(wString.split(", ")))
    return result

#function to check special characters from database
async def check_format(formatString):
    #('',)
    if len(formatString) == 5 or len(formatString) == 0:
        return True
    #(' ',) 
    elif len(formatString) == 6 and formatString[4] == ',':
        return True
    else:
        return False   
