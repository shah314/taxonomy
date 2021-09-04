#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 11:22:53 2021

@author: Shalin Shah

Calculate the hit rate @ position 10, after the learning has completed.
"""
from classes import user_movie_dot
import numpy as np

def hit_rate(mov, users):

    sample = dict()

    # Take a 10% random sample of movies, as negative sampling
    rng = np.random.RandomState(314)
    for m in mov:
        if rng.uniform() <= 0.1:
            sample[m] = mov[m]

    hits = 0
    dots = list()
    for u in users.keys():
        user = users[u]

        for m in sample.keys():
            if m not in user.test:
                movie = sample[m]
                dot = np.dot(user.factor, movie.factor)
                udot = user_movie_dot(u, m, dot)
                dots.append(udot)

        for m in user.test:
            movie = mov[m]
            dot = np.dot(user.factor, movie.factor)
            udot = user_movie_dot(u, m, dot)
            dots.append(udot)

        dots.sort(reverse=True, key=lambda x: x.dot)
        count = 0
        for umd in dots:
            if umd.movieid in user.test:
                hits = hits + 1
                break

            count+=1

            if count > 10:
                break

    return hits
