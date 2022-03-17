async def sortWatchList(wString):
    delim = ", "
    result = delim.join(sorted(wString.split(", ")))
    return result