#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B.
Etc.
metadata sqlalchemy.schema.MetaData
engine acts as an interface
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division

from config import *

import logging.config
import unittest
from utility_excel import ExcelBookAPI

from utility_inspect import whoami, whosdaddy
import datetime
from utility_path import get_new_file_rev_path
from UtilityPrintTable import PrettyTable
import pandas as pd
from exergyframes import exergy_frame as xrg

import sqlalchemy as sa
#from sqlalchemy import Table, Column, Integer, String, ForeignKey,DateTime, Boolean, MetaData

import datetime

ECHO_ON = False

from sqlalchemy.interfaces import PoolListener

VECTOR_SET = [
              (('KeyValue','Environment'),('VariableName','Site Outdoor Air Drybulb Temperature'),('ReportingFrequency','Hourly')),
              (('KeyValue','Environment'),('VariableName','Site Outdoor Air Dewpoint Temperature'),('ReportingFrequency','Hourly')),
              (('KeyValue','AIR LOOP DEMAND SIDE INLET 1'),('VariableName','System Node Temperature'),('ReportingFrequency','Hourly')),
              ]

VECTOR_SET1 = [
              (('KeyValue','Environment'),('ReportingFrequency','Hourly')),
              ]


#===============================================================================
# Code
#===============================================================================


class ForeignKeysListener(sa.interfaces.PoolListener):
    def connect(self, dbapi_con, con_record):
        db_cursor = dbapi_con.execute('pragma foreign_keys=ON')

# NOTES
def NOTESONLY_JOINING():
    # This is an easy way to join tables!
    qry = sa.select(['*']).where(tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex)
    # The 'where' method overrides the __eq__ operator to produce an SQL statement
    print users.c.name == None

#--- Utilities
def get_metadata(engine):
    metadata = sa.MetaData()
    metadata.reflect(engine)    
    return metadata

#---Query the DB-------------------------


def getTableObject(metadata, tableName):
    """ DOC """
    return metadata.tables[tableName]


def getTableNames(engine):
    """ DOC """
    metadata= get_metadata(engine)
    
    return metadata.tables.keys()

def getNumberRecordsInTable(engine,tableObj):
    s = sa.select([sa.func.count(tableObj)])
    return engine.execute(s).fetchone()[0]

#---Update table-------------------------

def insertRows(engine, tableObject, rows):
    """ Uses the transaction design to only commit after transactions ready """
    #logging.info("Inserting {} rows into {}".format(len(rows),tableObject))

    engine.echo = False

    connection = engine.connect()

    #engine
    trans = connection.begin()

    assert not isinstance(rows[0], basestring)

    for row in rows:
        connection.execute(tableObject.insert().values(row))

    trans.commit()
    engine.echo = False

    logging.info("Inserted {} rows into {}".format(len(rows),tableObject))

#---Pretty print tables-------------------------

def count_rows(engine,tableObj):
    """Just count"""
    s = sa.select([tableObj])
    result = engine.execute(s)

    idx_row = 0
    for row in result:
        idx_row += 1

    return idx_row


def get_dict(engine, table_object):
    "Given a table object, return all rows of the table as a dictionary"
    column_names = [col.name for col in table_object.c]

    rows = list()

    for row in engine.execute(table_object.select()):
        rows.append(dict(zip(column_names,row)))

    return rows




def get_rows(engine,tableObj,maxRows = None):
    """Given a table object, return rows as a list of tuples"""
    s = sa.select([tableObj])
    result = engine.execute(s)

    rows = list()
    idx_row = 1
    for row in result:
        rows.append(row)
        idx_row += 1
        if maxRows and idx_row > maxRows:
            break

    logging.debug("Returned {} rows from {}".format(len(rows),tableObj.name))

    return rows

def get_pretty_table(engine,tableObj,maxRows = None):
    """Get a PP table given a <sqlalchemy.schema.Table> object
    Return a tuple containing the table name, and the PP rows"""
    columnNames = tableObj.columns.keys()
    myTable = PrettyTable(columnNames)

    s = sa.select([tableObj])
    result = engine.execute(s)



    idx_row = 1
    for row in result:
        myTable.add_row(row)
        idx_row += 1
        if maxRows and idx_row > maxRows:
            break

    logging.info("Created pretty table {}".format(tableObj.name))

    return (tableObj.name, myTable)



def get_all_pretty_tables(engine,maxRows = None):
    """Call get_pretty_table() for all tables in engine"""
    metadata = sa.MetaData()
    metadata.reflect(engine)
    tables = list()
    for table in metadata.sorted_tables:
        tables.append(get_pretty_table(engine, table,maxRows))
    logging.info("Created {} pretty tables".format(len(tables)))

    return tables

def print_all_pretty_tables(engine,maxRows = None):
    """Call get_all_pretty_tables(), and print all to screen"""
    for thisTable in get_all_pretty_tables(engine,maxRows):
        print "***" + thisTable[0] + "***"
        print thisTable[1]

def printOnePrettyTable(engine, tableName,maxRows = None):
    """Call get_pretty_table(), and print to screen"""
    metadata = sa.MetaData()
    metadata.reflect(engine)
    thisTable = getTableObject(metadata, tableName)
    #print thisTable
    #raise
    thisTableData =  get_pretty_table(engine,thisTable,maxRows)
    print "***" + thisTableData[0] + "***"
    print thisTableData[1]

def sa_join_select():

    s = select([users.c.fullname]).select_from(
                       users.join(addresses,
               addresses.c.email_address.like(users.c.name + '%'))
                                               )

def get_column(table,col_name):
    for col in table.c:
        #print type(col)
        #print "Name",col.name
        #print col.name,col_name
        if col.name == col_name:
            #print "Yes,"
            return col
    raise
        #print "Col",col



def get_variable_vector(engine, metadata, criteria_list):
    """ Pass in a list of criteria to match, i.e.
    criteria_list = (('KeyValue','3NP:CORR1'),
                        ('VariableName','Zone People Sensible Heating Rate'),
                        ('ReportingFrequency','Monthly'),
                        )
    Possible criteria are taken from the respective tables:
    TimeIndex    ReportVariableDataDictionaryIndex    VariableValue    ReportVariableExtendedDataIndex    TimeIndex    Month    Day    Hour    Minute    Dst    Interval    IntervalType    SimulationDays    DayType    EnvironmentPeriodIndex    WarmupFlag    ReportVariableDataDictionaryIndex    VariableType    IndexGroup    TimestepType    KeyValue    VariableName    ReportingFrequency    ScheduleName    VariableUnits    ReportVariableExtendedDataIndex    MaxValue    MaxMonth    MaxDay    MaxHour    MaxStartMinute    MaxMinute    MinValue    MinMonth    MinDay    MinHour    MinStartMinute    MinMinute

    This function then returns all rows which match these criteria
    Returns the columns from the selection_list
     """
    #===========================================================================
    # Create the query
    #===========================================================================
    # The tables;
    tab_RVdata = getTableObject(metadata, "ReportVariableData")
    tab_time = getTableObject(metadata, "Time")
    tab_RVdata_dictonary = getTableObject(metadata, "ReportVariableDataDictionary")
    tab_RV_extended = getTableObject(metadata, "ReportVariableExtendedData")

    # Join Time and Data
    selection_list = ['Month','Day','Hour','Minute','ReportingFrequency','VariableName','KeyValue','VariableUnits','VariableValue']
    qry = sa.select(selection_list).where(tab_RVdata.c.TimeIndex  == tab_time.c.TimeIndex)

    # Join (Time and Data) with the Dictionary
    qry = qry.where(tab_RVdata.c.ReportVariableDataDictionaryIndex == tab_RVdata_dictonary.c.ReportVariableDataDictionaryIndex)

    #TODO: DO NOT JOIN EXTENDED DATA - It only joins on daily values?
    # Join (Time and Data and Dictionary) with Extended Data
    #qry = qry.where(tab_RVdata.c.ReportVariableExtendedDataIndex == tab_RV_extended.c.ReportVariableExtendedDataIndex)

    #===========================================================================
    # Interim testing
    #===========================================================================
    if 0:
        connection = engine.connect()
        result_iterator = connection.execute(qry)#.fetchall()

        column_headers = result_iterator.keys()

        myTable = PrettyTable(column_headers)

        idx_row = 1
        maxRows = 2000
        for row in result_iterator:
            myTable.add_row(row)
            idx_row += 1
            if maxRows and idx_row > maxRows:
                break

        print myTable
        raise

    #===========================================================================
    # Build the filter criteria
    #===========================================================================
    for criteria in criteria_list:
        qry = qry.where(get_column(tab_RVdata_dictonary,criteria[0]) == criteria[1])

    tabbed_qry = "\n\t\t".join(qry.__str__().split("\n"))

    logging.debug("Running query \n\t\t{}".format(tabbed_qry))

    #===========================================================================
    # Get the results
    #===========================================================================

    connection = engine.connect()
    results = connection.execute(qry).fetchall()
    print results
    raise

    column_headers = result_iterator.keys()

    result_vector = list()
    unit = set()
    name = set()
    key = set()

    for row in result_iterator:
        result_vector.append(row['VariableValue'])
        unit.add(row['VariableUnits'])
        name.add(row['VariableName'])
        key.add(row['KeyValue'])

    connection.close()

    assert(len(unit)==1), "Too many columns returned, unit: {}".format(unit)
    assert(len(name)==1), "Too many columns returned, name: {}".format(name)
    assert(len(key)==1), "Too many columns returned, key: {}".format(key)

    result = [[name.pop(),key.pop(),unit.pop()],result_vector]

    logging.info("Returning a vector length {} over {}".format(len(result[1]), result[0]))


    return result

def OLD_FROM_SUPER_TABLE():
    raise

    # For testing
    if 0:
        one_row = result_iterator.fetchone()
        for item in zip(column_headers,one_row):
            print item

    result = result_iterator.fetchall()


    connection.close()

    logging.info("Matching {} criteria to return {} data rows".format(len(criteria_list), len(result)))
    print result
    raise

    result = zip(*result)
    result_dict = dict(zip(column_headers,result))
    df = pd.DataFrame(result_dict)

    #===========================================================================
    # Convert to a datetime series
    #===========================================================================


    time_cols = df[['Month','Day','Hour','Minute']]
    new_time_col = list()

    for row in time_cols.values:
        #print row.tolist()
        this_datevec = [2013] + [int(item) for item in row.tolist()]
        #print this_datevec
        this_datevec[3] = this_datevec[3] - 1
        #print this_datevec
        #Y, M,D H,M,S
        new_time_col.append( pd.datetime(*this_datevec) )
    df['datetime'] = new_time_col
    df = df.set_index('datetime')

    df = df.drop(['Month','Day','Hour','Minute'],1)

    logging.info("Created a frame of shape {}".format(df.shape))

    return df



def get_variable_def_from_RVDD(engine, metadata, varName, key_val,interval = "Hourly"):
    logging.info("Selecting {} = {}, {}".format(varName, key_val,interval))

    tReportVariableDataDictionary = getTableObject(metadata, "ReportVariableDataDictionary")
    #s = sa.select([tReportVariableDataDictionary.c.KeyValue])

    #
    #qry = sa.select(["ReportVariableDataDictionaryIndex","VariableUnits"], from_obj=tReportVariableDataDictionary )

    # Get all columns from table
    qry = sa.select(["*"], from_obj=tReportVariableDataDictionary )
    # Match variable name
    qry = qry.where(tReportVariableDataDictionary.c.VariableName == varName)
    # Match key value
    qry = qry.where(tReportVariableDataDictionary.c.KeyValue == key_val)

    # Get results
    results = engine.execute(qry)
    #print qry
    count = 0
    for res in results:
        this_res = res
        count += 1

    assert count == 1

    # Get the column names
    col_names = [c.name for c in tReportVariableDataDictionary.c]

    return dict(zip(col_names, this_res))

def idf_var_names_RVDD(engine, metadata):
    "Gets all variable names from the RVDD"
    tReportVariableDataDictionary = getTableObject(metadata, "ReportVariableDataDictionary")
    #print tReportVariableDataDictionary.columns
    #raise
    s = sa.select([tReportVariableDataDictionary.c.VariableName])

    var_names = ['{}'.format(objName[0]) for objName in engine.execute(s)]

    s = sa.select([tReportVariableDataDictionary.c.KeyValue])

    var_keys = ['{}'.format(objName[0]) for objName in engine.execute(s)]

    return zip(var_names,var_keys)

def get_frame_simple(engine,metadata,table_name,maxRows = None):
    # Table to query

    #tbl = sa.Table(table_name, metadata)
    #tbl.create(checkfirst=True)

    # Select all
    #sql = tbl.select()

    # run sql code
    #result = engine.execute(sql)

    #print result
    #print result[:]
    #raise
    tableObj = getTableObject(metadata, table_name)
    rows = get_rows(engine,tableObj,maxRows)
    #print tbl.keys()
    columnNames = tableObj.columns.keys()

    # Insert to a dataframe
    if len(rows) == 0:
        df = pd.DataFrame(data=[["EMPTY" for col in columnNames]], columns=columnNames)

    elif len(rows) > 0:
        df = pd.DataFrame(data=rows, columns=columnNames)

    logging.info("Returned a dataframe of shape {}".format(df.shape))


    # Close connection
    #conn.close()
    return df

def get_frame(engine,metadata):


    """
    ***ReportVariableData***
    +-----------+-----------------------------------+------------------+---------------------------------+
    | TimeIndex | ReportVariableDataDictionaryIndex |  VariableValue   | ReportVariableExtendedDataIndex |
    +-----------+-----------------------------------+------------------+---------------------------------+
    |     1     |                 6                 | -0.0583333333333 |               None              |
    |     1     |                 7                 |      -1.95       |               None              |
    """

    """
    ***Time***
    +-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
    | TimeIndex | Month | Day | Hour | Minute | Dst | Interval | IntervalType | SimulationDays | DayType | EnvironmentPeriodIndex | WarmupFlag |
    +-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
    |     1     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |
    |     2     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |

    """


    """
    ***ReportVariableDataDictionary***
    +-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
    | ReportVariableDataDictionaryIndex | VariableType | IndexGroup | TimestepType |          KeyValue         |             VariableName            | ReportingFrequency | ScheduleName | VariableUnits |
    +-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
    |                 6                 |     Avg      |    Zone    |     Zone     |        Environment        |           Outdoor Dry Bulb          |       Hourly       |     None     |       C       |
    """

    #tab_RVD.TimeIndex = tab_time.TimeIndex
    #tab

    # Join Time and RVD
    tab_RVD = getTableObject(metadata, "ReportVariableData")
    tab_time = getTableObject(metadata, "Time")
    tab_RVDD = getTableObject(metadata, "ReportVariableDataDictionary")
    #qry = sa.join(tab_RVD,tab_time,tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex)
    #qry = qry.select("VariableValue")
    #qry = qry.select("ReportVariableData"."VariableValue")


    qry = sa.select([tab_RVD.c.VariableValue]).select_from(
                       sa.join(tab_RVD,tab_time,tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex))



    rvd_time = sa.join(tab_RVD,tab_time,tab_RVD.c.TimeIndex  == tab_time.c.TimeIndex)
    #ReportVariableDataDictionaryIndex
    # Merge it with the RVDD
    rvd_time_rvdd = sa.join(rvd_time,tab_RVDD,tab_RVD.c.ReportVariableDataDictionaryIndex  == tab_RVDD.c.ReportVariableDataDictionaryIndex)




    #childJoins = childJoins.join(child)

    #print type(qry)
    #qry = qry.select(["VariableValue"])
    #qry = qry.select('"ReportVariableData"."VariableValue"')
    print rvd_time_rvdd
    qry = sa.select(["*"]).select_from(rvd_time_rvdd)
    #print qry
    #sa.select()
    #raise
    #qry = qry.where(tab_RVD.c.ReportVariableDataDictionaryIndex == var_idx)
    #print qry
    #print type(qry)
    #print qry.columns

    #qry = qry.where( == var_idx)

    key = "Environment"
    var_name = "Outdoor Dry Bulb"

    qry = qry.where(tab_RVDD.c.VariableName== var_name)
    qry = qry.where(tab_RVDD.c.KeyValue == key)


    #print qry
    #raise
    connection = engine.connect()
    results = connection.execute(qry)
    connection.close()

    print results
    print results.keys
    #print results["Interval"]
    #raise
    for k in results.keys():
        print k
    #for item in dir(results):
    #    print item


    #raise

def get_zone_names(engine,metadata):

    fr_zones = get_frame_simple(engine,metadata,"Zones")

    zone_name_list = fr_zones['ZoneName'].values
    logging.debug("Got {} zone names".format(len(zone_name_list)))

    return zone_name_list


def get_frame_OLD(engine, metadata):
    tab_RVDD = getTableObject(metadata, "ReportVariableDataDictionary")
    #tReportVariableDataDictionary
    qry = sa.select([tab_RVDD])
    qry = qry.where(tab_RVDD.c.ReportingFrequency == "Hourly")
    result = engine.execute(qry)
    for item in result:
        #print type(item)
        this_key = item["KeyValue"]
        this_name = item["VariableName"]
        this_idx = item["ReportVariableDataDictionaryIndex"]
        this_unit = item["VariableUnits"]
        #this_vec = get_variable_vector(engine, metadata, this_idx)
        print this_key, this_name

def load_database(fullPath):
    """Given a database path, open it and extract information to create the DesignSpace object

    """
    logging.info("Loading a database from {} ".format(fullPath))

    ECHO_ON = 0
    # Create the connection to the databse
    engine = sa.create_engine('sqlite:///{}'.format(fullPath), echo=ECHO_ON, listeners=[ForeignKeysListener()])
    logging.info("Connected: {} ".format(engine))

    # Create an inspector
    insp = sa.engine.reflection.Inspector.from_engine(engine)
    logging.info("Found tables: {} ".format(", ".join(insp.get_table_names())))

    metadata = sa.MetaData()
    metadata.reflect(bind=engine)

    


def run_project(database_path, output_path):

    engine = sa.create_engine('sqlite:///{}'.format(database_path), echo=ECHO_ON, listeners=[ForeignKeysListener()])
    logging.info("Connected to {} ".format(database_path))

    metadata = sa.MetaData()
    metadata.reflect(engine)

    criteria_list = list()

    zone_name_list = get_zone_names(engine,metadata)

    print zone_name_list

    criteria_zone_temp =  [(('KeyValue',zone_name),('VariableName','Zone Mean Air Temperature'),('ReportingFrequency','Hourly')) for zone_name in zone_name_list]
    criteria_list = criteria_list + criteria_zone_temp

    vector_list = list()

    # Get the raw vectors
    for criteria in VECTOR_SET:

        vector = get_variable_vector(engine, metadata,criteria)
        #print vector
        vector_list.append(vector)

    # Assemble the data
    headers = list()
    data = list()
    for vector in vector_list:
        data.append(vector.pop())
        headers.append(vector.pop())

    #print data
    #print zip(*data)
    #raise
    header_def = ["name","key","units"]

    this_frame = xrg.ExergyFrame(
            name="Test",
            dataArray = zip(*data),
            timeArray=None,
            headersArray = zip(*headers),

            headersDef= header_def,
            )
    this_frame = xrg.add_simple_time(this_frame)
    print this_frame.checkTimeExists()
    xrg.displayFrame(this_frame)

    xl = ExcelBookAPI(output_path)

    this_frame.saveToExcelAPI(xl,'Comparison')
    xl.saveAndClose()
    xl.closeAll()




#        pass
    #print dir(item)
    #print item.items():

    #for k in item:
    #    print k
    #    print dir(item)

#===============================================================================
#---TESTING---------------------------------------------------------------------
#===============================================================================
@unittest.skipIf(1,"")
class testIdfSQL(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        #fullPath = r"C:\Users\PC1\Desktop\TCJ_A4_ehb.sql"

        self.excel_path_all_tables = os.path.join(SAMPLE_SQL,"test_all_tables.xlsx")
        self.excel_path_vector_table = os.path.join(SAMPLE_SQL,"test_vectors.xlsx")

        self.RVDD_path = os.path.join(SAMPLE_SQL,"rvdd.xlsx")

        fullPath = os.path.join(SAMPLE_SQL,"Proposed2.sql")

        #\MyUtilities
        #fullPath = r"C:\Projects\Simulation\TCJ_A3_ene v8.sql"
        self.engine = sa.create_engine('sqlite:///{}'.format(fullPath), echo=ECHO_ON, listeners=[ForeignKeysListener()])
        logging.info("Connected to {} ".format(fullPath))

        self.metadata = sa.MetaData()
        self.metadata.reflect(self.engine)

    @unittest.skipIf(0,"")
    def test010_get_column(self):
        print "**** TEST {} ****".format(whoami())
        table_name = u'ReportVariableDataDictionary'
        table_obj = getTableObject(self.metadata, table_name)
        column_name = "VariableType"
        col = get_column(table_obj,column_name)
        print "Returned column {} from table {}".format(column_name,table_name)
        print col

    @unittest.skipIf(1,"")
    def test020_pretty_print(self):
        #printOnePrettyTable(self.engine,"ReportVariableData",maxRows = 200)
        #printOnePrettyTable(self.engine,"Time",maxRows = 200)
        printOnePrettyTable(self.engine,"ReportVariableDataDictionary",maxRows = 200)
        #printOnePrettyTable(self.engine,"ReportVariableExtendedData",maxRows = 200)


    @unittest.skipIf(1,"")
    def test020_frame(self):
        print "**** TEST {} ****".format(whoami())

        #ReportVariableDataDictionary
        #get_frame(self.engine,self.metadata)

        fr_zones = get_frame_simple(self.engine,self.metadata,"Zones")
        #print(fr_zones)
        print("First 3 zone names : \n{} ".format(fr_zones['ZoneName'][:3]))

        #print(fr_zones[:3, 'ZoneName'])
        fr_zones.to_excel(r"C:\temp\tes.xls")


    @unittest.skipIf(0,"")
    def test010_printTables(self):
        print "**** TEST {} ****".format(whoami())

        print("\nTables")
        print("---------")
        print([table for table in getTableNames(self.metadata)])
        #for table in getTableNames(self.metadata):
        #    print table,


        print("\nRVDD")
        print("---------")
        t_RVDD = getTableObject(self.metadata, u'ReportVariableDataDictionary')
        print("Report dictionary table object: {} , {}".format(t_RVDD, type(t_RVDD)))
        print("Report dictionary table columns: {}".format(t_RVDD.c))
        var_names = idf_var_names_RVDD(self.engine,self.metadata)
        print("{} Variables in RVDD, from {} to {}".format(len(var_names), var_names[0], var_names[-1] ))

        print("\nZones")
        print("---------")
        t_zones = getTableObject(self.metadata, u'Zones')
        print("Zones: {} , {}".format(t_zones, type(t_zones)))
        print("Zones columns: {}".format(t_zones.c))

        print("Zones count: {}".format(count_rows(self.engine,t_zones)))
        print("Zones rows: {}".format(get_rows(self.engine,t_zones)[0]))



        #var_names = idf_var_names_RVDD(self.engine,self.metadata)
        #print("{} Variables in RVDD, from {} to {}".format(len(var_names), var_names[0], var_names[-1] ))


        #printOnePrettyTable(self.engine, u'ReportVariableDataDictionary')

        #for item in t_RVDD:
        #    print item

        #printOnePrettyTable(self.engine, "Constructions")
        #printOnePrettyTable(self.engine, "Surfaces",100)

        #print_all_pretty_tables(self.engine,maxRows = 10)
        #print("---------")

        #print("{}".format(len(var_names))
        #for v_name in var_names:
        #    print v_name






    @unittest.skipIf(1,"")
    def test100_get_vectors(self):
        print "**** TEST {} ****".format(whoami())
        """VariableType    IndexGroup    TimestepType    KeyValue    VariableName    ReportingFrequency    ScheduleName    VariableUnits"""

        #tbl_rvdd = getTableObject(self.metadata, "ReportVariableDataDictionary")

        #printOnePrettyTable(self.engine,"ReportVariableDataDictionary",maxRows = 200)

        vector_list = list()
        # Get the raw vectors
        for criteria in VECTOR_SET:

            vector = get_variable_vector(self.engine, self.metadata,criteria)
            #print vector
            vector_list.append(vector)

        # Assemble the data
        headers = list()
        data = list()
        for vector in vector_list:
            data.append(vector.pop())
            headers.append(vector.pop())

        #print data
        #print zip(*data)
        #raise
        header_def = ["name","key","units"]

        this_frame = xrg.ExergyFrame(
                name="Test",
                dataArray = zip(*data),
                timeArray=None,
                headersArray = zip(*headers),

                headersDef= header_def,
                )
        this_frame = xrg.add_simple_time(this_frame)
        print this_frame.checkTimeExists()
        xrg.displayFrame(this_frame)


    @unittest.skipIf(1,"")
    def test100_get_vectorsOLD(self):

        assert(df.shape[1] == 1), "Too many columns returned from criteria:{}".format(criteria)
        df_list.append(df)



        header_def = ["name","key","units"]

        frame_list = list()
        for df in df_list:
            variable_names = df["VariableName"][0]
            variable_units = df["VariableUnits"][0]
            variable_keys = df["KeyValue"][0]

            header = [variable_names, variable_units, variable_keys]
            #df.pop('VariableName')
            #df.pop('VariableUnits')
            #df.pop('KeyValue')
            #df.pop('ReportingFrequency')
            print header
            raise
            this_frame = xrg.ExergyFrame(
                name="Test",
                dataArray = df["VariableValue"].values,
                timeArray=df.index,
                headersArray=header,

                headersDef= header_def,
                )
            frame_list.append(this_frame)


        for frame in frame_list:
            frame.checkShapes()
            #xrg.displayFrame(frame)
            #print xrg.displayFrame(frame)
            #checkShapes

        new_frame = xrg.mergeFrames("results", frame_list, flgMergeHeads = False)
        new_frame = xrg.add_simple_time(new_frame)
        xl = ExcelBookAPI(self.excel_path_vector_table)

        new_frame.saveToExcelAPI(xl,'Comparison')
        xl.saveAndClose()
        xl.closeAll()


    @unittest.skipIf(1,"")
    def test010_cycleAll(self):
        print "**** TEST {} ****".format(whoami())

        #ReportVariableDataDictionary
        get_frame(self.engine,self.metadata)

    @unittest.skipIf(1,"")
    def test010_getVectorOLD(self):
        print "**** TEST {} ****".format(whoami())

        var_name = "Zone Infiltration Sensible Heat Loss"

        key_value = "A4%3NP:3NP%OFFICE%NORTH"

        print get_variable_def_from_RVDD(self.engine,self.metadata,var_name,key_value)
        get_variable_vector(self.engine,self.metadata,6)
        #, varName, key_val


    @unittest.skipIf(1,"")
    def test300_write_RVDD(self):
        print "**** TEST {} ****".format(whoami())
        max_rows = None
        writer = pd.ExcelWriter(self.RVDD_path)
        fr = get_frame_simple(self.engine,self.metadata,"ReportVariableDataDictionary",max_rows)

        print("Writing {}, {} rows".format("ReportVariableDataDictionary", len(fr)))

        #print(fr_zones[:3, 'ZoneName'])
        fr.to_excel(writer,"ReportVariableDataDictionary")

        writer.save()



    @unittest.skipIf(1,"")
    def test300_export_all_to_excel(self):
        print "**** TEST {} ****".format(whoami())
        max_rows = 1000
        writer = pd.ExcelWriter(self.excel_path_all_tables)
        for table_name in [table for table in getTableNames(self.metadata)]:
            fr = get_frame_simple(self.engine,self.metadata,table_name,max_rows)

            print("Writing {}, {} rows".format(table_name, len(fr)))

            #print(fr_zones[:3, 'ZoneName'])
            fr.to_excel(writer,table_name)

        writer.save()

    @unittest.skipIf(1,"")
    def test010_printResults(self):
        print "**** TEST {} ****".format(whoami())
        printOnePrettyTable(self.engine, "ReportVariableData",100)
        #printOnePrettyTable(self.engine, "ReportVariableDataDictionary",10)

        #printOnePrettyTable(self.engine, "Time",100)


        #thisTable = getTableObject(self.metadata, "ReportVariableDataDictionary")

        tReportVariableData = getTableObject(self.metadata, "ReportVariableData")
        tReportVariableDataDictionary = getTableObject(self.metadata, "ReportVariableDataDictionary")
        tTime = getTableObject(self.metadata, "Time")

        for item in dir(getTableObject(self.metadata, "ReportVariableDataDictionary")):
            print item
        print type(tReportVariableData)
        print tReportVariableData.columns
        print tReportVariableData.count
        print tReportVariableData.join
        print tReportVariableData.foreign_keys
        print tReportVariableData.primary_key
        #print tReportVariableData.__table_args__
        #tReportVariableData.join(tTime)
        #raise
        """
        SELECT column_name(s)
        FROM table1
        INNER JOIN table2
        ON table1.column_name=table2.column_name;
        """



        qry = tReportVariableData.join(tTime, tReportVariableData.c.TimeIndex  == tTime.c.TimeIndex)

        qry = sa.join(tReportVariableData,tTime,tReportVariableData.c.TimeIndex  == tTime.c.TimeIndex)

        qry = qry.select()

        #qry = sa.select(from_obj = qry )
        #results = self.engine.execute(qry)
        #print qry
        print type(qry)
        print qry
        results = self.engine.execute(qry)


        print results
        for res in results:
            print res
        raise
        #join(right, onclause=None, isouter=False)


        RAW_SQL = """
        ALTER TABLE Employees
        ADD FOREIGN KEY (UserID)
        REFERENCES ActiveDirectories(id)
        """
        RAW_SQL = """ALTER TABLE ReportVariableData
        ADD CONSTRAINT FK_TimeIndex_Time FOREIGN KEY (TimeIndex)
        REFERENCES Time(TimeIndex)"""

        RAW_SQL = """ALTER TABLE ReportVariableData
        ADD FOREIGN KEY (TimeIndex)
        REFERENCES Time(TimeIndex)"""

        RAW_SQL = """ALTER TABLE ReportVariableData
        ADD CONSTRAINT PerOrders
        FOREIGN KEY (TimeIndex)
        REFERENCES Time(TimeIndex)"""

        RAW_SQL = """ALTER TABLE ReportVariableData"""

"""
***ReportVariableData***
+-----------+-----------------------------------+------------------+---------------------------------+
| TimeIndex | ReportVariableDataDictionaryIndex |  VariableValue   | ReportVariableExtendedDataIndex |
+-----------+-----------------------------------+------------------+---------------------------------+
|     1     |                 6                 | -0.0583333333333 |               None              |
|     1     |                 7                 |      -1.95       |               None              |
"""

"""
***ReportVariableDataDictionary***
+-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
| ReportVariableDataDictionaryIndex | VariableType | IndexGroup | TimestepType |          KeyValue         |             VariableName            | ReportingFrequency | ScheduleName | VariableUnits |
+-----------------------------------+--------------+------------+--------------+---------------------------+-------------------------------------+--------------------+--------------+---------------+
|                 6                 |     Avg      |    Zone    |     Zone     |        Environment        |           Outdoor Dry Bulb          |       Hourly       |     None     |       C       |
"""


"""
***Zones***
+-----------+-----------------------------+----------+---------+---------+---------+----------------+----------------+---------------+--------+------------+----------------+----------------+----------------+-----------------+-----------------+----------+----------+---------------+---------------+----------------------+-----------------------+-----------+------------------+----------------+---------------+-------------------+
| ZoneIndex |           ZoneName          | RelNorth | OriginX | OriginY | OriginZ |   CentroidX    |   CentroidY    |   CentroidZ   | OfType | Multiplier | ListMultiplier |    MinimumX    |    MaximumX    |     MinimumY    |     MaximumY    | MinimumZ | MaximumZ | CeilingHeight |     Volume    | InsideConvectionAlgo | OutsideConvectionAlgo | FloorArea | ExtGrossWallArea | ExtNetWallArea | ExtWindowArea | IsPartOfTotalArea |
+-----------+-----------------------------+----------+---------+---------+---------+----------------+----------------+---------------+--------+------------+----------------+----------------+----------------+-----------------+-----------------+----------+----------+---------------+---------------+----------------------+-----------------------+-----------+------------------+----------------+---------------+-------------------+
|     1     |  A4%1NPA:1NPA%OFFICE%NORTH  |   0.0    |   0.0   |   0.0   |   0.0   | -17.1730861826 | -33.0571134869 | 2.05999999685 |   1    |    1.0     |      1.0       | -23.5490771482 | -12.7021670377 |  -38.1740888444 |  -30.0069178664 |   0.0    |   4.12   |      4.12     | 156.555857223 |          2           |           7           |  41.7482  |  47.5573685367   | 42.1173685367  |     4.978     |         1         |

"""

"""
***Time***
+-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
| TimeIndex | Month | Day | Hour | Minute | Dst | Interval | IntervalType | SimulationDays | DayType | EnvironmentPeriodIndex | WarmupFlag |
+-----------+-------+-----+------+--------+-----+----------+--------------+----------------+---------+------------------------+------------+
|     1     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |
|     2     |   1   |  1  |  1   |   0    |  0  |    60    |      1       |       1        |  Sunday |           3            |    None    |

"""

@unittest.skipIf(0,"")
class test_simple_load(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())
        
    def test010_simple_load(self):
        print "**** TEST {} ****".format(whoami())

        path_file = r"M:\52_CES\14011_LEED_MediaTower\4_Doks\41_Ein_Doks\140603 Site visit MJ FB\A_01_MV_KM1_KM1.Power_anz\2009032809.txs"

        load_database(path_file)


@unittest.skipIf(1,"")
class testDataBase(unittest.TestCase):
    def setUp(self):
        print "**** TEST {} ****".format(whoami())

        myLogger.setLevel("CRITICAL")


        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.ordered('v100',(1,2,3,4)),
                        Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]

        thisDspace = DesignSpace(basisVariables)
        self.D1 = thisDspace

        myLogger.setLevel("DEBUG")

    def test010_(self):
        testLocation = "C:\TestSQL\update.sql"
        metadata, engine = createTables(self.D1,":memory:")
        populateTableDSpace(metadata, engine,self.D1)


        #print "Table names:"
        #print metadata.tables.keys()
        #variablesTable = metadata.tables["variables"]



        someResults = (
                       (-37584290, datetime.datetime.now(), datetime.datetime.now(), 1, 1, 1, 1),
                       (-37584230, datetime.datetime.now(), datetime.datetime.now(), 1, 1, 1, 2),
                       )

        #theResult =
        insertRows(engine, metadata.tables["results"],someResults )


        print_all_pretty_tables(engine, metadata)

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print ABSOLUTE_LOGGING_PATH
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    #excel_path_vector_table = os.path.join(SAMPLE_SQL,"test_vectors.xlsx")

    #sql_path = os.path.join(SAMPLE_SQL,"Proposed2.sql")
    #run_project(sql_path,excel_path_vector_table)


    logging.debug("Finished _main".format())
