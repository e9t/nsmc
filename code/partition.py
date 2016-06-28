#! /usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np; np.random.seed(1234)
import pandas as pd


ntrain = 150000

data = pd.read_csv('../ratings.txt', sep='\t', quoting=3)
data = pd.DataFrame(np.random.permutation(data))
trn, tst = data[:ntrain], data[ntrain:]

header = 'id document label'.split()
trn.to_csv('../ratings_train.txt', sep='\t', index=False, header=header)
tst.to_csv('../ratings_test.txt', sep='\t', index=False, header=header)
