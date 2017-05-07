#===============================================================================
# Title of this Module
# Authors; MJones, Other
# 00 - 2012FEB05 - First commit
# 01 - 2012MAR17 - Update to ...
#===============================================================================

"""This module does A and B.
Etc.
"""

#===============================================================================
# Set up
#===============================================================================
# Standard:
from __future__ import division
from __future__ import print_function

from config import *

import logging.config
import unittest

from utility_inspect import whoami, whosdaddy, listObject
from utility_path import get_current_file_dir
import re

from collections import defaultdict
from numpy import genfromtxt

import datetime
import pandas as pd
#===============================================================================
# Code
#===============================================================================
PRIMARY_TOKENS = {
        'start_file'           : re.compile("^Program Version"),
        'end_var_defs'           : re.compile("^End of Data Dictionary"),
        'environment'       : re.compile("Environment Title"),
        'time'              : re.compile("^Day of Simulation"),
        #'unit'              : re.compile("([^[]*)[([^]]*)]"),
        'unit_brackets'     : re.compile('\[(.+?)\]'),
        'comment'           : re.compile("(!.*)"),
        'report_step_in_comment'        : re.compile("^(Detailed|TimeStep|Hourly|Daily|Monthly|Runperiod)"),
        'test'              : re.compile("End",re.VERBOSE),
            }

def get_headers(eso_file):



    data = list()
    for line in eso_file:

        #======================================================================
        # Split the comment off of the line
        #======================================================================
        data_comment = re.split("!",line)
        # The first element is always the data
        data = data_comment.pop(0).strip()
        # And get the second element if exists
        if data_comment:
            comment = data_comment.pop(0).strip()
        else:
            comment = None
        assert(not(data_comment), "There should be no more elements in the line other than data and comment after splitting")

        #print("{} - {}".format(data,comment))

        #=======================================================================
        # Skip the first line
        #=======================================================================
        if re.compile(PRIMARY_TOKENS['start_file']).match(data):
            continue


        #=======================================================================
        # Finished with variable definitions
        #=======================================================================
        if re.compile(PRIMARY_TOKENS['end_var_defs']).match(data):
            #df.index.name = "Variable ID"

            logging.debug("Found {} variable definitions".format(len(df)))
            return df


        #=======================================================================
        # The variable signatures
        #=======================================================================
        var = dict()
        split_data = re.split(",",data)
        logging.debug("Line: {} !! {}".format(split_data,comment))


        #flg_hourly = comment == "Hourly"
        # First element is variable ID
        var['Variable ID'] = int(split_data.pop(0))
        # Second element is number columns
        var['Number columns'] = int(split_data.pop(0))
        # Third element is the
        var['Category'] = split_data.pop(0)

        # Manage units for environment types
        #if var['Type'] == "Environment":
        if split_data:
            name_units = split_data.pop(0)
            # Check for square brackets
            unit_search = re.search(PRIMARY_TOKENS['unit_brackets'],name_units)
            #print(unit_search)
            #print(unit_search.group(0))
            #print(unit_search.group(1))
            #raise

            if unit_search:
                # SRE_Match.group(1) is the matched object without brackets?
                var['Units'] = unit_search.group(1)
                # Replace the unit with nothing and the remainder is the name
                var['Name'] = re.sub('\[(.+?)\]','',name_units)
            # There are no unit brackets found
            else:
                var['Name'] = name_units
                var['Units'] = "Unknown"
            #else:
            #    var['Name'] = "Unknown"
            #    var['Units'] = "Unknown"

        if comment:
            period = re.search(PRIMARY_TOKENS['report_step_in_comment'],comment)
            if period:
                var['Timestep'] = period.group(0)
            else:
                var['Timestep'] = "N/A"
        else:
            var['Timestep'] = "N/A"
        #if flg_hourly:
        #    var['Timestep'] = comment
        #else:
        #    var['Timestep'] = "unk"

        #print(var)
        # Append this row
        #s = pd.Series(var)
        #s.name = var_index
        #df = df.append(s)
    #df = pd.DataFrame(columns=['Variable ID','Number columns','Category','Name', 'Units', 'Timestep'])
def parse_timestep(lines, line_index,hourly_indices):
    this_line = lines[line_index]
    this_line = this_line.strip()
    split_line = re.split(",",this_line)


    #2,    6,      Day of Simulation[],    Month[], Day of Month[],DST Indicator[1=yes 0=no],Hour[],StartMinute[],EndMinute[],DayType
    #2,            1,                      12,      21,            0,                        1,     0.00,         60.00,      WinterDesignDay

    id = split_line.pop(0)
    year = 2014

    day_of_simulation = int(split_line.pop(0))
    month = int(split_line.pop(0))
    day = int(split_line.pop(0))
    dst = int(split_line.pop(0))
    hour = int(split_line.pop(0))
    start_minute = int(float(split_line.pop(0)))
    end_minute = int(float(split_line.pop(0)))
    time_step = end_minute - start_minute
    day_type=split_line.pop(0)


    timestamp = datetime.datetime(year, month, day, hour-1,start_minute)
    #logging.debug("TIMESTEP at {}, {} minute step, {} ".format(timestamp,time_step,day_type))

    flg_end_tstep = False
    line_index += 1
    values = list()
    while not flg_end_tstep:

        this_line = lines[line_index]
        split_line = re.split(",",this_line)
        #logging.debug("{}".format(split_line))

        if split_line[0] == "1":
            #logging.debug("Found next environment, break ".format())
            flg_end_tstep = True
            line_index -= 1
        elif split_line[0] == "2":
            flg_end_tstep = True
            #logging.debug("Found next tstep, break".format())
            line_index -= 1
        elif re.compile(r"^ Number of Records Written=").match(this_line):
            flg_end_tstep = True
            #logging.debug("Found EOF, break".format())
            line_index -= 1
        elif re.compile(r"^End of Data").match(this_line):
            flg_end_tstep = True
            #logging.debug("Found EOF, break".format())
            line_index -= 1

        elif int(split_line[0]) in hourly_indices:
            # A time line
            var_id = split_line.pop(0)
            value = float(split_line.pop(0))
            values.append((var_id, value))
            assert(not split_line)
        else:
            # Skip if not an hourly timestep
            pass
        line_index += 1
    #logging.debug("Found {} hourly values in this timestep".format(len(values)))

    table_row = dict((('Timestamp',timestamp), ('step', time_step), ('Day type',day_type)))
    table_row.update(dict(values))
    logging.debug("TIMESTEP {}".format(table_row))
    return line_index, table_row

def parse_environment(lines,line_index,hourly_indices):
    this_line = lines[line_index]
    split_line = re.split(",",this_line)
    id = split_line.pop(0)
    location = split_line.pop(0)
    logging.debug("Found environment {}".format(location))

    #environ_table = defaultdict(list)
    time_rows = list()
    line_index += 1

    flg_end_environment = False
    while not flg_end_environment:
        this_line = lines[line_index]
        split_line = re.split(",",this_line)
        #logging.debug("{}".format(split_line))
        if split_line[0] == "1":
            id = split_line.pop(0)
            location = split_line.pop(0)
            logging.debug("Found next environment, break".format())
            flg_end_environment = True
            line_index -= 1

        elif re.compile(r"^ Number of Records Written=").match(this_line):
            logging.debug("Found EOF, break".format())
            flg_end_environment = True
            line_index -= 1

        elif re.compile(r"^End of Data").match(this_line):
            flg_end_environment = True
            logging.debug("Found EOF, break".format())
            line_index -= 1

        elif split_line[0] == "2":
            # Timestep
            line_index, table_row = parse_timestep(lines, line_index,hourly_indices)
            time_rows.append(table_row)
            continue
        else:
            print(this_line)
            raise
        line_index += 1

    df = pd.DataFrame.from_records(time_rows, index='Timestamp')
    #print(df.head())

    return line_index - 1,  (location, df)



def get_hourly_data(lines,hourly_indices):
    line_count = 0
    #lines = eso_file.readlines()
    mark_environment = list()
    mark_timestep = list()
    line_index = 0

    tokenized_lines = list()
    flg_stop = False
    flg_header = True
    environments = list()
    while not flg_stop:
        if line_index >= 1000:
            flg_stop = True

        #for line in lines[:200]:

        line = lines[line_index]

        print("Line: {}",line,end='')
        #tokenized_line = list()

        #=======================================================================
        # Skip the header
        #=======================================================================
        if re.compile("^End of Data Dictionary").match(line):
            flg_header = False
            #print("End header")
            #line_index += 1
            #tokenized_line += ['HEAD']

        if flg_header:
            #tokenized_line += ['HEAD']
            #print("HEAD")
            line_index += 1
            continue

        line = line.strip()
        split_line = re.split(",",line)
        #print(line)
        #print(split_line)

        #=======================================================================
        # Environment
        #=======================================================================
        #1,5,Environment Title[],Latitude[deg],Longitude[deg],Time Zone[],Elevation[m]
        #1,DENVER CENTENNIAL  GOLDEN   N ANN HTG 99% CONDNS DB,  48.20,  17.20,   1.00, 130.00

        if split_line[0] == "1":

            line_index, this_environment = parse_environment(lines, line_index,hourly_indices)
            environments.append(this_environment)
        else:
            line_index += 1

    environments = dict(environments)
    #print("Done")
    return environments





def OLD():
    logging.debug("Processed {} lines".format(len(tokenized_lines)))

    with open(r'C:\EclipseWorkspace\PyIDF\SampleESO\result.txt','a') as the_file:
        for line in tokenized_lines[:300]:
            line_out = " - ".join(line)
            print(line_out, file=the_file)
            #print(line_out)


    logging.debug("Found {} environments".format(len(mark_environment)))
    logging.debug("Found {} timesteps".format(len(mark_timestep)))
    raise
    frames = list()

    while(mark_environment):
        this_env = mark_environment.pop(0)
        idx_environ = this_env[0]
        environ = this_env[1]
        if not mark_environment:
            idx_next_env = len(lines)
        else:
            idx_next_env = mark_environment[0][0]

        logging.debug("Processing environment {}, lines {} to {}".format(environ,idx_environ,idx_next_env))

        while(mark_timestep):
            this_time = mark_timestep.pop(0)
            idx_time = this_time[0]
            this_timestamp = this_time[1]
            if not mark_timestep:
                # TODO: This is not robust
                idx_next_time = len(lines) - 2
            else:
                idx_next_time = mark_timestep[0][0] - 1
            logging.debug("Processing timestep {}, lines {} to {}".format(this_timestamp, idx_time,idx_next_time))

            this_step_lines = lines[idx_time:idx_next_time]

            # Only import first 2 columns!
            step_data = genfromtxt(this_step_lines, delimiter=',',usecols=(0, 1))



            #print(step_data.dtypes)
            var_indices = step_data[:,0].astype(int)
            data = step_data[:,1]
            df = pd.DataFrame(index = var_indices, data=data,columns=[this_timestamp])
            df.index.name = 'Var_id'
            frames.append(df)
    logging.debug("Created {} frames".format(len(frames)))


    #for


    #print(len(frames))
    merged_frame = pd.concat(frames,axis =1)
    merged_frame = merged_frame.transpose()



    print(merged_frame.head())
    print("Number entries", len(merged_frame))
    print(merged_frame.ix[0:20,0:20])

    raise
    line_count += 1
    print(line_count)
#
#    # This is a header line for hourly data
#    if not flg_end_var_def and comment == "Hourly":
#        #if
#
#
#        #comment = data_comment[0]
#
#
#        var_id = split_data.pop(0)
#        var_n_cols = split_data.pop(0)
#        var_type = split_data.pop(0)
#        # Environemnt row
#        #if var_type == "Environment":
#        #    print("ENV")
#
#        #var_comment =
#        print("ID = {}, Cols = {}, Name = {}".format(var_id,var_n_cols,var_type, split_data))
#        #headers.append(re.split(",",line))
#
#        #print(data)
#        #raise
#
#
#    if flg_end_var_def:
#        print(re.split(",",line))

def parse(path_eso):
    """Return the something to the something."""


    with open(path_eso, 'r') as eso_file:
        logging.debug("Opened {}".format(eso_file))
        lines = eso_file.readlines()
    headers = get_headers(lines)

    #print(data)

    #===========================================================================
    # Hourly items
    #===========================================================================
    mask_hourly = headers["Timestep"] == "Hourly"
    df_hourly = headers[mask_hourly]

    # Ensure that each hourly data item has only one defined column
    check_num_cols = df_hourly["Number columns"] == 1
    assert(check_num_cols.all())
    logging.debug("{} Hourly data items :".format(len(df_hourly)))
    hourly_indices = set(df_hourly.index)
    logging.debug("Hourly indices: {}".format(hourly_indices))

    environments = get_hourly_data(lines,hourly_indices)

    for name,frame in environments.iteritems():
        print(name)
        print(frame.head())
        #print(frame['40'])
        frame.rename(columns={'40': 'a'}, inplace=True)
        print(frame.head())
        break


    #print()
    #print(df_hourly)
    #print(df_hourly.values)
    #print(df_hourly.index)

    #print(tuple(df_hourly.values))
    print("Vals")
    print("Tuples for MI", df_hourly.values.tolist())

    cols = pd.MultiIndex.from_tuples(df_hourly.values.tolist(), names=df_hourly.columns.values.tolist())
    print("MIndex: ", cols)
    print("MI Names: ", cols.names)
    #print(cols[])
    #print(dir(cols))

    for col in cols:
        pass
        #print(col[])
        #print(frame[col])




    #columns
#    for row in df_hourly:
#        print(row)


#===============================================================================
# Unit testing
#===============================================================================

class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))
        path_eso = get_current_file_dir(__file__)
        path_eso = path_eso + r"\..\.."
        print(path_eso)
        path_eso = os.path.abspath(path_eso)
        print(path_eso)
        path_eso = path_eso + r"\SampleESO\1ZoneUncontrolled.eso"


        #path_eso = r"C:\Projects\IDFout\Baseline-G000.eso"
        #path_eso = r"C:\EclipseWorkspace\PyIDF\src\parse_eso\testfile.exo"
        parse(path_eso)

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))

#===============================================================================
# Main
#===============================================================================
if __name__ == "__main__":
    print(ABSOLUTE_LOGGING_PATH)
    logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)


    myLogger = logging.getLogger()
    myLogger.setLevel("DEBUG")

    logging.debug("Started _main".format())

    #print FREELANCE_DIR

    unittest.main()

    logging.debug("Finished _main".format())
