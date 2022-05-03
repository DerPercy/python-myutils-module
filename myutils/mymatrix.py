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
            foundRow = initRowdefinition(rowLabel,columnLabels,options["columnAggregator"])
            matrix["rows"].append(foundRow)
        entryAdded = False
        for column in foundRow["columns"]:
            if colLabel == column["columnLabel"]:
                entryAdded = True
                column["values"].append(entry)
                for colAgr in options["columnAggregator"]:
                    column["columnAggregator"][colAgr["value"]] += entry[colAgr["value"]]

        if entryAdded == False:
            print("Entry not added")

    # columnAggregator
    matrix["columnAggregator"] = []
    colIndex = 0
    for colLab in  columnLabels:
        colAgrObj = {}
        for colAgr in options["columnAggregator"]:
            colAgrObj[colAgr["value"]] = calcAggregatedColumnValue(matrix,colAgr,colIndex)
        matrix["columnAggregator"].append(colAgrObj)
        colIndex += 1
    return matrix

def calcAggregatedColumnValue(matrix,aggregatoroption,columnIndex):
    val = 0
    for row in matrix["rows"]:
        val += row["columns"][columnIndex]["columnAggregator"][aggregatoroption["value"]]
    return val

def initRowdefinition(rowLabel,colLabelArray,columnAggregatorOptions):
    row = {}
    row["rowLabel"] = rowLabel
    row["columns"] = []
    for colLabel in colLabelArray:
        row["columns"].append(initColumnDefinition(colLabel,columnAggregatorOptions))
    return row

def initColumnDefinition(colLabel,columnAggregatorOptions):
    column = {}
    column["columnLabel"] = colLabel
    column["values"] = []
    column["columnAggregator"] = {}
    # Init columnAggregator
    for colAgr in columnAggregatorOptions:
        column["columnAggregator"][colAgr["value"]] = 0.0
    return column

def addColLab(colLabArray, columnLabel):
    found = False
    for colLab in colLabArray:
        if colLab == columnLabel:
            found = True
    if found == False:
        colLabArray.append(columnLabel)
