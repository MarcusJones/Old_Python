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

# Testing imports
from ..design_space import (Variable, DesignSpace, Mapping, create_database, 
                            load_project_from_database, ObjectiveSpace, add_population_db, 
                            evaluate_population, get_gen_stats, get_run_stats
                            )

from ..individuals import BasicIndividual

from utility_path import get_new_file_rev_path, get_latest_revision

import utility_SQL_alchemy as util_sa

from ..evaluators import random_fitness

#===============================================================================
# Logging
#===============================================================================
logging.config.fileConfig(ABSOLUTE_LOGGING_PATH)
myLogger = logging.getLogger()
myLogger.setLevel("DEBUG")

#===============================================================================
# Unit testing
#===============================================================================

class CreateSimpleMemoryDB(unittest.TestCase):
    def setUp(self):
        myLogger.setLevel("CRITICAL")
        

        myLogger.setLevel("CRITICAL")
        basisVariables = [
                          Variable("C1",50),
                          Variable.ordered("C2",3.14),
                          Variable.ordered('v100',(1,2,3,4)),
                          Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        thisDspace = DesignSpace(basisVariables)
        D1 = thisDspace
        
        # Create OSpace
        objective_names = ('obj1','obj3')
        objective_goals = ('Max', 'Min')
        this_obj_space = ObjectiveSpace(objective_names, objective_goals)
        obj_space1 = this_obj_space
        
        self.mapping = Mapping(D1, obj_space1, BasicIndividual, random_fitness)

        myLogger.setLevel("DEBUG")
        
        print("Created a test mapping;", self.mapping)

    def test000_CreateDB_memory(self):
        print("**** TEST {} ****".format(whoami()))
        # Create the setUp DB in memory
        db_path = ":memory:"
        db_engine = create_database(self.mapping, dataBasePath = db_path )
        db_metadata = util_sa.get_metadata(db_engine)
        print("Engine; {}".format(db_engine))
        print("Metadata; {}".format(db_metadata))
        
        #print(db.engine)
        
        #db.print_results_table()
        print("All tables in db:")
        
        print(util_sa.getTableNames(db_engine))
        for table in util_sa.get_all_pretty_tables(db_engine):
            print(table[0])
            print(table[1])
            
        print("Success in creating database in {}".format(db_path))


#===============================================================================
#---Test DataBase
#===============================================================================

class StoreDB_Disk(unittest.TestCase):
    def setUp(self):
        # First, create a test DB object
        myLogger.setLevel("CRITICAL")
        basisVariables = [
                          Variable("C1",50),
                          Variable.ordered("C2",3.14),
                          Variable.ordered('v100',(1,2,3,4)),
                          Variable.unordered('VarStr',["Blue","Red","Green"]),
                        ]
        thisDspace = DesignSpace(basisVariables)
        D1 = thisDspace
        
        # Create OSpace
        objective_names = ('obj1','obj3')
        objective_goals = ('Max', 'Min')
        this_obj_space = ObjectiveSpace(objective_names, objective_goals)
        obj_space1 = this_obj_space
        
        self.mapping = Mapping(D1, obj_space1, BasicIndividual, random_fitness)

        myLogger.setLevel("DEBUG")
        
        print("Created a test mapping;", self.mapping)

        full_path = "..\..\..\TestOutput\update.sql"
        self.full_abs_path =  os.path.abspath(full_path)

    def test010_save_space(self):
        print("**** TEST {} ****".format(whoami()))
        path_new_sql = get_new_file_rev_path(self.full_abs_path)
        self.theDB = create_database(self.mapping, path_new_sql)

class ReloadDB_AddGens(unittest.TestCase):
    def setUp(self):
        print("**** TEST {} ****".format(whoami()))
        full_path = "..\..\..\TestOutput\update.sql"
        self.full_abs_path =  os.path.abspath(full_path)

    def test010_reload_add_gens(self):
        print("**** TEST {} ****".format(whoami()))

        path_last_sql = get_latest_revision(self.full_abs_path)

        mapping, engine = load_project_from_database(path_last_sql)
        print(mapping)
        
        #util_sa.print_all_pretty_tables(engine,maxRows = None)

        for generation in range(5):
            print("Generation {}".format(generation))
            this_pop = mapping.get_random_population(10)
            
            this_pop = evaluate_population(this_pop, engine)
            add_population_db(engine,this_pop)
            
    
    def test020_reload(self):
        print("**** TEST {} ****".format(whoami()))

        path_last_sql = get_latest_revision(self.full_abs_path)
        dspace, ospace, engine = load_project_from_database(path_last_sql)

class AnalyzeDB(unittest.TestCase):
    def setUp(self):
        myLogger.setLevel("CRITICAL")
        print("**** TEST {} ****".format(whoami()))
        full_path = "..\..\..\TestOutput\update.sql"
        self.full_abs_path =  os.path.abspath(full_path)
        path_last_sql = get_latest_revision(self.full_abs_path)
        dspace, ospace, engine = load_project_from_database(path_last_sql)
        self.dspace = dspace
        self.ospace = ospace
        self.engine = engine
        
        myLogger.setLevel("DEBUG")
        
        
    def test010_analyze(self):
        print("**** TEST {} ****".format(whoami()))
        #util_sa.print_all_pretty_tables(self.engine,maxRows = None)
        genNum = 2
        print(self.dspace)
        gen_results = get_gen_stats(self.engine,genNum)
        print(gen_results)
        run_results = get_run_stats(self.engine)
        print(run_results)
    
    def test020_data(self):
        pass
        
        
class LargeDisk(unittest.TestCase):
    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

        full_path = "..\..\TestOutput\update.sql"
        self.full_abs_path =  os.path.abspath(full_path)

    def test000_createDB(self):
        print("**** TEST {} ****".format(whoami()))

        from itertools import product
        from string import ascii_lowercase
        keywords = [''.join(i) for i in product(ascii_lowercase, repeat = 3)]

        myLogger.setLevel("CRITICAL")
        basisVariables = [
                          Variable("C1",50),
                        Variable.ordered("C2",3.14),
                        Variable.from_range('v100','0.00','0.01','1.00'),
                        Variable.unordered('VarStr',keywords),
                        ]
        objectives = ["obj1","obj3"]
        thisDspace = DesignSpace(basisVariables,objectives)
        self.D1 = thisDspace
        myLogger.setLevel("DEBUG")

        print("Created a test space;", self.D1)

        path_new_sql = get_new_file_rev_path(self.full_abs_path)

        self.theDB = create_database(self.D1,path_new_sql)

    def test010_load_and_run_10x10(self):
        print("**** TEST {} ****".format(whoami()))

        start = time.time()

        path_last_sql = get_latest_revision(self.full_abs_path)

        dspace, engine = load_project_from_database(path_last_sql)

        #util_sa.print_all_pretty_tables(engine,maxRows = None)

        for generation in range(10):
            this_pop = dspace.get_random_population(10)

            for indiv in this_pop:
                indiv.fitness = eval_minus_one(indiv.fitness)

            add_population_db(engine,this_pop)

        end = time.time()
        print("total time: {}".format(end - start))


    #@unittest.skip("")
    def test020_load_and_run_1000x10(self):
        print("**** TEST {} ****".format(whoami()))

        start = time.time()

        path_last_sql = get_latest_revision(self.full_abs_path)

        dspace, engine = load_project_from_database(path_last_sql)

        util_sa.print_all_pretty_tables(engine,maxRows = None)

        for generation in range(1000):
            this_pop = dspace.get_random_population(10)

            for indiv in this_pop:
                indiv.fakeEval()

            add_population_db(engine,this_pop)

        end = time.time()
        print("total time: {}".format(end - start))

    #@unittest.skip("")
    def test030_load_and_run_100x1000(self):
        print("**** TEST {} ****".format(whoami()))

        start = time.time()

        path_last_sql = get_latest_revision(self.full_abs_path)

        dspace, engine = load_project_from_database(path_last_sql)

        util_sa.print_all_pretty_tables(engine,maxRows = None)

        for generation in range(100):
            this_pop = dspace.get_random_population(1000)

            for indiv in this_pop:
                indiv.fakeEval()

            add_population_db(engine,this_pop)

        end = time.time()
        print("total time: {}".format(end - start))

class LoadAnalyze(unittest.TestCase):
    def setUp(self):
        print("**** TEST {} ****".format(whoami()))

        full_path = "..\..\TestOutput\update.sql"
        self.full_abs_path =  os.path.abspath(full_path)

    def test040_load_and_analyze(self):
        print("**** TEST {} ****".format(whoami()))

        start = time.time()

        path_last_sql = get_latest_revision(self.full_abs_path)

        dspace, engine = load_project_from_database(path_last_sql)

        util_sa.print_all_pretty_tables(engine,maxRows = None)

        end = time.time()
        print("total time: {}".format(end - start))

