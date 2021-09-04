#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:15:46 2021

@author: Shalin Shah

Update the latent factors using gradient descent
"""
import random
import numpy as np
from util import sigmoid, get_sigma

def update_latent_factors(movies, users, categories, root, learning_rate):
    
    # The variance of the normal distribution
    sigma = get_sigma()
    
    # Paramaters
    delta = 10
    tau = 10
    
    for u in users.keys():
        user = users[u]
        pos_keys = list(user.trainp.keys())
        neg_keys = list(user.trainn.keys())
        if len(neg_keys) == 0:
            # If there are no movies that a user does not like, use the entire set of movies to sample a negative from
            neg_keys = list(movies.keys())
        
        pos_movie = None
        neg_movie = None
        if len(pos_keys) > 0:
            pos_rand = int(random.random() * len(pos_keys))
            neg_rand = int(random.random() * len(neg_keys))
            pos_movie = movies[pos_keys[pos_rand]]
            neg_movie = movies[neg_keys[neg_rand]]
            
            # Update user latent factor
            xui = np.dot(user.factor, pos_movie.factor) + pos_movie.bias
            xuj = np.dot(user.factor, neg_movie.factor) + neg_movie.bias
            cuij = 1 - sigmoid(xui - xuj)
            du = cuij * (pos_movie.factor - neg_movie.factor) - user.factor / sigma
            user.factor = user.factor + learning_rate*du
        
            # Update positive movie path in the taxonomy
            pathi = pos_movie.path
            previous = categories[pathi[0]]
            for i in range(2,4):
                nodeid = pathi[i]
                node = categories[nodeid]
                wik = node.factor - previous.factor
                dwik = cuij*user.factor - pos_movie.factor/sigma
                wik = wik + learning_rate*dwik
                node.factor = previous.factor + wik
                previous = node
            
            # Update negative movie path in the taxonomy
            pathj = neg_movie.path
            previous = categories[pathj[0]]
            for i in range(2,4):
                nodeid = pathj[i]
                node = categories[nodeid]
                wik = node.factor - previous.factor
                dwik = cuij*user.factor - pos_movie.factor/sigma
                wik = wik + learning_rate*dwik
                node.factor = previous.factor + wik
                previous = node
        
            # Update positive movie factor
            pathi = pos_movie.path
            last = pathi[3]
            previous = categories[last]
            wik = pos_movie.factor - previous.factor
            dwik = cuij*user.factor - pos_movie.factor/sigma
            wik = wik + learning_rate*dwik
            pos_movie.factor = previous.factor + wik
        
            # Update positive movie factor
            pathj = pos_movie.path
            last = pathj[3]
            previous = categories[last]
            wik = neg_movie.factor - previous.factor
            dwik = cuij*user.factor - neg_movie.factor/sigma
            wik = wik + learning_rate*dwik
            neg_movie.factor = previous.factor + wik
            
            # Update positive movie bias
            biasi = pos_movie.bias     
            dbi = (cuij * np.exp(biasi / delta)) / (1 + np.exp(biasi / delta)) - biasi / (tau*tau)
            pos_movie.bias = pos_movie.bias + learning_rate * dbi
            
            # Update negative movie bias
            biasj = neg_movie.bias
            dbj = cuij * np.exp(biasj / delta) / (1 + np.exp(biasj / delta)) - biasj / (tau*tau)
            neg_movie.bias = neg_movie.bias + learning_rate * dbj