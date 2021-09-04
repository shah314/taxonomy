#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:08:38 2021

@author: shah
"""
import numpy as np
import math

def sigmoid(x):

    if x > 100:
        return 1

    if x < -100:
        return 0

    return 1 / (1 + math.exp(-x))

def normal_sample():
    sam = np.random.multivariate_normal(means(), cov_mtx(), 1)
    return sam[0]

def normal_sample2():
    sam = np.random.normal(0, 0.01)
    return sam

def cov_mtx():
    return np.diag(means()+get_sigma())

def means():
    return np.zeros(get_dimension())

def get_dimension():
    return 10

def get_sigma():
    return 0.1
