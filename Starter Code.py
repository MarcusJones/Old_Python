#!/usr/bin/env python
# coding: utf-8

# # Starter code for DC Bike Sharing compute to data server. 

# ## Paths

# The dataset will be mounted in the docker container at the INPUT_PATH environment variable location. Uncomment the cell below before uploading the script. 

# In[17]:


# import os
# os.environ["INPUT_PATH"] = "/volumes/input"
# os.environ["OUTPUT_PATH"] = "/volumes/output"


# For local testing, set the paths below. 

# In[19]:


#%% Paths
from pathlib import Path
import os

# INPUT DATA
if  "INPUT_PATH" in os.environ:
    path_input = Path(os.environ["INPUT_PATH"])
else:
    path_input = Path.cwd() /  "data" # this is the resulting dataset

path_input_file = path_input / "data_all_base.csv" # it's the input dataset, that you should process

# OUTPUT FOLDER
if  "OUTPUT_PATH" in os.environ:
    path_output = Path(os.environ["OUTPUT_PATH"])
else:
    #path_output = Path("/volumes/output") # this is the resulting dataset
    path_output = Path.cwd() # ("/volumes/output") # this is the resulting dataset

# LOGS FILE
path_logs = Path("/volumes/logs")

assert path_input_file.exists(), "Can't find required mounted path: {}".format(path_input_file)
assert path_input_file.is_file() | path_input_file.is_symlink(), "/volumes/input/dataset must be a file"
assert path_output.exists(), "Can't find required mounted path: {}".format(path_output)
# assert path_logs.exists(), "Can't find required mounted path: {}".format(path_output)


# ## Logging

# A good script will include logging messages to help debug remote issues. 

# In[20]:


# Logging
# =============================================================================
import sys
import logging
import datetime
from pprint import pprint

logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.INFO)

# Create formatter
FORMAT = "%(asctime)s : %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]

logging.info("Logging started")


# ## Libraries

# The following python libraries are available in the remote server environment.

# In[21]:


import os
from pathlib import Path
# Set the environment
from pprint import pprint
import json


# In[22]:


# Standard imports
# =============================================================================
import os
from pathlib import Path
import sys
import zipfile
import gc
import time
from pprint import pprint
from functools import reduce
from collections import defaultdict
import json
# import yaml
import inspect
import json
import pickle
from copy import deepcopy
import itertools
from time import sleep


# In[23]:


# ML imports
# =============================================================================
import numpy as np
print('numpy {} as np'.format(np.__version__))
import pandas as pd
print('pandas {} as pd'.format(pd.__version__))
# pd.options.mode.chained_assignment = None

import sklearn as sk
import sklearn.ensemble
import sklearn.neural_network
print('sklearn {} as sk'.format(sk.__version__))


# ## Input dataset

# Data will be loaded from the path set above. Ensure your local and remote environments are set properly. 

# In[25]:


# Load data
logging.info("Loading {}".format(path_input_file))
df = pd.read_csv(path_input_file)
df.head()


# In[55]:


y_all = df['cnt']
X_all = df.drop(['cnt'], axis=1)
X_all.drop(['dteday', 'Unnamed: 0'], axis=1, inplace=True)
X_all.info()


# Split the dataset

# In[56]:


X_tr, X_te, y_tr, y_te = sk.model_selection.train_test_split(X_all, y_all)


# ## Train the model

# In[57]:


# Instantiate and train
this_model = sk.ensemble.RandomForestClassifier()
this_model.fit(X_tr, y_tr)
logging.info("Finished training")


# In[66]:


mae = sk.metrics.mean_absolute_error(y_te, this_model.predict(X_te))
print("Mean average error: {}".format(mae))


# ## Write the results (which will be returned from the compute server) 

# In[67]:


path_model = path_output / 'dataset'
logging.info("Writing model to {}".format(path_model))
with open(path_model, 'wb') as fh:
    pickle.dump(this_model, fh)
logging.info("Saved {}".format(path_model))


# In[68]:


logging.info("Finished training run")


# In[ ]:




