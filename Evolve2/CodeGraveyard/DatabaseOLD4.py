
#--- OLD
def get_results(self):
    """Assembles a table from the results table, by inserting the proper variable values
    Returns column names, and variable values
    """
    # --- Variables
    # Get the variable names from DB:
    varTable = util_sa.getTableObject(self.metadata, "variables")
    s = sa.select([varTable.c.name])
    varNames = [varName[0] for varName in self.engine.execute(s)]

    # Get the actual table objects for each variable
    varTables = list()
    for tabName in varNames:
        varTables.append(util_sa.getTableObject(self.metadata, "vector_" + tabName))

    # --- Objectives
    # Get the objective column names
    objTable = util_sa.getTableObject(self.metadata, "objectives")
    s = sa.select([objTable.c.description])
    objNames = [objName[0] for objName in self.engine.execute(s)]

    # Get the actual table objects for each variable
    varTables = list()
    for tabName in varNames:
        varTables.append(util_sa.getTableObject(self.metadata, "vector_" + tabName))

    variableValueCols = [vecTable.c.value for vecTable in varTables]

    resultsTable = util_sa.getTableObject(self.metadata, "results")

    childJoins = resultsTable
    for table in varTables:
        childJoins = childJoins.join(table)

    qry = sa.select(variableValueCols + objNames, from_obj=childJoins)

    #print type(variableValueCols[0].table.name)
    #print variableValueCols[0].table.name

    columnNames = [col.table.name for col in variableValueCols]
    columnNames = columnNames + ["obj_" + name for name in  objNames]

    rows = self.engine.execute(qry)

    return columnNames, rows

def print_results_table(self):
    util_sa.printOnePrettyTable(self.engine, "results")


def plotGens(self):

    results = self.get_run_stats()

    print(results)

    Graphics.plotAllGens(results)

def printResultsTab(self):
    """Call get_run_stats, present table"""
    columnNames, rows = self.get_results()
    printTable(columnNames, rows)
