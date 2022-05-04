async def sortWatchList(wString):
    delim = ", "
    result = delim.join(sorted(wString.split(", ")))
    return result

async def sortWatchListEp(list, sortedlist, eplist):
    counter = 0
    result = ""
    for i in sortedlist.split(","):
        for j in list.split(","):
            if i in j or j in i:
                counter1 = 0
                for k in eplist.split(","):
                    if counter == counter1:
                        ep = ''.join([x for x in k if x.isdigit()])
                        delim = ", "
                        result1 = ep + delim
                        result += result1
                        break
                    counter1 += 1
                break
            counter += 1
        counter = 0
    
    return result
            


# function to check special characters from database


async def check_format(formatString):
    # ('',)
    if len(formatString) == 5 or len(formatString) == 0:
        return True
    # (' ',)
    elif len(formatString) == 6 and formatString[4] == ",":
        return True
    else:
        return False


async def check_ep_format(formatString):
    # ('',)

    # (' ',)
    if formatString == "('',)":
        return True
    elif len(formatString) == 6 and formatString[4] == ",":
        if (
            formatString[2] == "0"
            or formatString[2] == "1"
            or formatString[2] == "2"
            or formatString[2] == "3"
            or formatString[2] == "4"
            or formatString[2] == "5"
            or formatString[2] == "6"
            or formatString[2] == "7"
            or formatString[2] == "8"
            or formatString[2] == "9"
        ):
            return False
        else:
            return True

    else:
        return False
