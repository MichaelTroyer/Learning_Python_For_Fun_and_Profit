# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

csv = r'.\data\ping_results.csv'

df = pd.read_csv(csv)

df.header()