# !wget https://downloads.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz
# !tar xvfz ta-lib-0.4.0-src.tar.gz
# !cd ta-lib ; ./configure --prefix=/usr ; make ; make install
# !pip install TA-Lib

import sys

import numpy as np
import pandas as pd
import talib
from talib.abstract import *

import matplotlib
import matplotlib.pyplot as plt

from pprint import pprint


df = pd.DataFrame({'open': np.random.random(100),
    'high': np.random.random(100),
    'low': np.random.random(100),
    'close': np.random.random(100),
    'volume': np.random.random(100)})

pprint(df.head(10))


np.arange('2016-01-01T00:00:00', '2016-01-02T00:00:00', dtype='datetime64[s]')[:100]

ts = pd.Timestamp('2016-06-30')
ts

dti = pd.date_range('2016/01/01', freq='D', periods=30)
dti