from .valueParser import getValue

def groupObjects(objectList,groupselector):
    """
    Grouping a list of json objects by the provided groupselector
    source: [{},{},{},{},{},...]
    result: [[{},{},...],[{},...],...]
    """
    retValue = []
    groupIDs = []
    for entry in objectList:
        groupVal = getValue(groupselector,entry)
        groupIndex = -1
        for index in range(len(groupIDs)):
            groupid = groupIDs[index]
            if groupid == groupVal:
                groupIndex = index
        if groupIndex == -1:
            groupIndex = len(groupIDs)
            groupIDs.append(groupVal)
            retValue.append([])
        #print(groupVal + str(groupIndex))
        retValue[groupIndex].append(entry)
    return retValue
