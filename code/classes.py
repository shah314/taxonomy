#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:06:36 2021

@author: Shalin Shah
"""
from util import normal_sample, normal_sample2

# A user is the person who watched the movie and then rated the movie.
class User:
    def __init__(self, id):
        self.id = id
        self.factor = normal_sample()
        self.ratings = dict()
        self.test = dict()
        self.trainp = dict()
        self.trainn = dict()
        
# A class for a movie, rated by at least one user
class Movie:
    def __init__(self, id):
        self.id = id
        self.factor = normal_sample()
        self.path = list()
        self.bias = normal_sample2()
        
# A category is a node in the taxonomy
class Category:
    def __init__(self, id):
        self.id = id
        self.factor = normal_sample()
        self.children = set()
        self.items = set()
        self.parent = 0
        self.genres = dict()
        
# This class is used in the hit rate calculation (measurement.py)
class user_movie_dot:
    def __init__(self, userid, movieid, dot):
        self.userid = userid
        self.movieid = movieid
        self.dot = dot
