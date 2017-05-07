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
import utility_path as util_path
import re
import pandas as pd
import numpy as np
import time
#===============================================================================
# Code
#===============================================================================
def convert_tstamp(stampstring):
    #print(stampstring)
    split_time = re.split('\.',stampstring)
    day = split_time.pop(0)
    month = split_time.pop(0)
    remainder = split_time.pop(0)
    split_rem = re.split(' ',remainder)
    timestring = split_rem.pop()
    year = split_rem.pop()
    timestr_split = re.split(':',timestring)
    sec = timestr_split.pop()
    min = timestr_split.pop()
    hr = timestr_split.pop()

    return pd.datetime(int(year),
                      int(month),
                      int(day),
                      int(hr),
                      int(min),
                      int(sec),
                      )

def replace_index(df,col_name):
    newindex = df.loc[:,col_name].map(convert_tstamp)
    df.index = newindex
    df.drop(col_name,inplace = True,axis =1)
    #print(df)
    df.drop('Events',axis =1, inplace = True)
    df.drop('Comment',axis =1, inplace = True)
    df.drop('User',axis =1, inplace = True)
    return df

def split_fname(fname):
    split_path = util_path.split_up_path(fname)
    this_fname = split_path[-2]
    #print(this_fname)

    new = re.sub('Interval Trend ','',this_fname)
    new = re.sub('1. 4. 2014', '', new)
    new = re.split('_',new)
    new = ' '.join(new)
    new = new.strip()
    #print(new)
    return new


def drop_duplicates_indexed(df):
    """Small helper to select duplicate indices and delete them
    Necessary because Pandas does not support this directly
    Simply create a new column and then delete it
    """
    df["index"] = df.index
    df.drop_duplicates(cols='index', take_last=True, inplace=True)
    del df["index"]
    #dupes = df.index.get_duplicates()
    #assert(len(dupes)==0)
    return df
#===============================================================================
# Unit testing
#===============================================================================



class allTests(unittest.TestCase):

    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

    def test010_SimpleCreation(self):
        print("**** TEST {} ****".format(whoami()))
        path_root = r"D:\Dropbox\EXERGY\02 Running\095 - LEED EcoPoint Kosice (Bischoff)\08 Monitoring\Sensor Data\\"
        path_root = r"C:\Dropbox\EXERGY\02 Running\095 - LEED EcoPoint Kosice (Bischoff)\08 Monitoring\Sensor Data\\"
        out_path_pickle = path_root + 'combined.pck'
        out_path_excel = path_root + 'combined.xlsx'

        assert(util_path.path_exists(path_root))
        file_names = util_path.get_files_by_ext_recurse(path_root, 'csv')

        df_list = list() # All CSV's are stored in a list
        for name in file_names:
            start_time = time.time()

            # Load and replace index with time
            this_frame = pd.read_csv(name, decimal=',')
            date_col_name = 'Time stamp'
            df = replace_index(this_frame,date_col_name)

            # Variable name from filename
            this_valname = split_fname(name)

            # Add the variable name to the columns
            new_cols = df.columns.values
            new_cols[0] = this_valname
            df.columns = new_cols

            # Drop duplicate timestamps
            df = drop_duplicates_indexed(df)

            elapsed_time = time.time() - start_time
            logging.debug("Loaded {} over {:0.3} s".format(this_valname,elapsed_time))

            df_list.append(df)

        logging.debug("{} total frames".format(len(df_list),elapsed_time))

        merged = pd.concat(df_list,axis = 1)
        merged.sort_index(inplace=True)
        merged.to_pickle(out_path_pickle)
        raise
        #print(merged)
        #print(merged.shape)


        with pd.ExcelWriter(out_path, engine='xlsxwriter') as writer:
            merged.to_excel(writer)
            #writer.save()
        logging.debug("Wrote {}".format(out_path))

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
