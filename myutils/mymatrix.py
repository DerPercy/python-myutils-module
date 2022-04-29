from .valueParser import getValue

def buildMatrix(data,options):
    matrix = {}
    matrix["rows"] = []
    columnLabels = []
    for entry in data:
        colLabel = getValue(options["columns"],entry,options["methods"])
        addColLab(columnLabels,colLabel)
    matrix["columnHeader"] = columnLabels
    #print(columnLabels)
    for entry in data:
        colLabel = getValue(options["columns"],entry,options["methods"])
        rowLabel = getValue(options["rows"],entry,options["methods"])
        foundRow = None
        for row in matrix["rows"]:
            if row["rowLabel"] == rowLabel:
                foundRow = row
        if foundRow == None:
            foundRow = initRowdefinition(rowLabel,columnLabels)
            matrix["rows"].append(foundRow)
        entryAdded = False
        for column in foundRow["columns"]:
            if colLabel == column["columnLabel"]:
                entryAdded = True
                column["values"].append(entry)

        if entryAdded == False:
            print("Entry not added")

    return matrix

def initRowdefinition(rowLabel,colLabelArray):
    row = {}
    row["rowLabel"] = rowLabel
    row["columns"] = []
    for colLabel in colLabelArray:
        row["columns"].append(initColumnDefinition(colLabel))
    return row

def initColumnDefinition(colLabel):
    column = {}
    column["columnLabel"] = colLabel
    column["values"] = []
    return column

def addColLab(colLabArray, columnLabel):
    found = False
    for colLab in colLabArray:
        if colLab == columnLabel:
            found = True
    if found == False:
        colLabArray.append(columnLabel)
