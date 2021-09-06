#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:15:34 2021

@author: Shalin Shah

Sample paths of movies in the taxonomy using Gibbs Sampling.
The only sampling that happens here, is the choosing of a child from the children of a node using np.random.choice.
The random choice happens using both, the latent factors (as a normal hierarchy) and the probability of a movie belonging to that node using genres.
Also, I don't use the chinese restaurant process, rather, I create a random taxonomy and then do an initial random assignment of movies to the taxonomy.
"""

import numpy as np
from scipy.stats import multivariate_normal
from util import cov_mtx

def sample_paths(categories, movies, genres):
    cg = create_genres_dict(movies, genres)
    np.random.seed(314)
    for m in movies:
        newpath = list()
        newpath.append(0)
        movie = movies[m]
        oldpath = movie.path
        mg = genres[m]
        mfactor = movie.factor
        
        root = categories[0]
        children = root.children
        chosenchild = -1
        probs = dict()
        for c in children:
            cfac = categories[c].factor
            if c in cg.keys():
                cgenres = cg[c]
            
            gprob = 0
            facprob = multivariate_normal.pdf(mfactor, cfac, cov_mtx())
            if c in cg.keys():
                gprob = genres_probability(cgenres, mg)
            
            totalprob = 0
            if (c in cg.keys()) & (gprob > 0) & (facprob > 0):
                totalprob = facprob + gprob
            elif facprob > 0:
                totalprob = facprob
            
            probs[c] = totalprob
    
        useold = True
        for c in probs:
            if probs[c] > 0:
                useold = False
                break
    
        if useold == False:
            p1 = list(probs.values())
            s = sum(p1)
            p1 = p1 / s
            chosenchild = np.random.choice(list(probs.keys()), 1, p=p1)[0]
            #chosenchild = list(probs.keys())[chosenindex]
            newpath.append(chosenchild)
        else:
            newpath.append(oldpath[3])
            chosenchild = oldpath[3]
           
        children = categories[chosenchild].children
        chosenchild = -1
        probs = dict()
        for c in children:
            cfac = categories[c].factor
            if c in cg.keys():
                cgenres = cg[c]
            
            gprob = 0
            facprob = multivariate_normal.pdf(mfactor, cfac, cov_mtx())
            if c in cg.keys():
                gprob = genres_probability(cgenres, mg)
            
            totalprob = 0
            if (c in cg.keys()) & (gprob > 0) & (facprob > 0):
                totalprob = facprob + gprob
            elif facprob > 0:
                totalprob = facprob
            
            probs[c] = totalprob
    
        useold = True
        for c in probs:
            if probs[c] != 0:
                useold = False
                break
    
        if useold == False:
            p1 = list(probs.values())
            s = sum(p1)
            p1 = p1 / s
            chosenchild = np.random.choice(list(probs.keys()), 1, p=p1)[0]
            #chosenchild = list(probs.keys())[chosenindex]
            newpath.append(chosenchild)
        else:
            newpath.append(oldpath[3])
            chosenchild = oldpath[3]
   
        children = categories[chosenchild].children
        chosenchild = -1
        probs = dict()
        for c in children:
            cfac = categories[c].factor
            if c in cg.keys():
                cgenres = cg[c]
            
            gprob = 0
            facprob = multivariate_normal.pdf(mfactor, cfac, cov_mtx())
            if c in cg.keys():
                gprob = genres_probability(cgenres, mg)
            
            totalprob = 0
            if (c in cg.keys()) & (gprob > 0) & (facprob > 0):
                totalprob = facprob + gprob
            elif facprob > 0:
                totalprob = facprob
            
            probs[c] = totalprob
    
        useold = True
        for c in probs:
            if probs[c] != 0:
                useold = False
                break
    
        if useold == False:
            p1 = list(probs.values())
            s = sum(p1)
            p1 = p1 / s
            chosenchild = np.random.choice(list(probs.keys()), 1, p=p1)[0]
            #chosenchild = list(probs.keys())[chosenindex]
            newpath.append(chosenchild)
        else:
            newpath.append(oldpath[3])
            chosenchild = oldpath[3]

        children = categories[chosenchild].children
        chosenchild = -1
        probs = dict()
        for c in children:
            cfac = categories[c].factor
            if c in cg.keys():
                cgenres = cg[c]
            
            gprob = 0
            facprob = multivariate_normal.pdf(mfactor, cfac, cov_mtx())
            if c in cg.keys():
                gprob = genres_probability(cgenres, mg)
            
            totalprob = 0
            if (c in cg.keys()) & (gprob > 0) & (facprob > 0):
                totalprob = facprob + gprob
            elif facprob > 0:
                totalprob = facprob
            
            probs[c] = totalprob
    
        useold = True
        for c in probs:
            if probs[c] != 0:
                useold = False
                break
    
        if useold == False:
            p1 = list(probs.values())
            s = sum(p1)
            p1 = p1 / s
            chosenchild = np.random.choice(list(probs.keys()), 1, p=p1)[0]
            #chosenchild = list(probs.keys())[chosenindex]
            newpath.append(chosenchild)
        else:
            newpath.append(oldpath[4])
            chosenchild = oldpath[4]    

        #print(oldpath)
        #print(newpath)

        movie.path = newpath

        update_path(movie, oldpath, newpath, genres, cg)

def genres_probability(catg, mg):
    total = 0
    for c in catg:
        val = catg[c]
        total+=val
    
    num = 0
    for m in mg:
        if m in catg:
            num+=1
    
    if total > 0:
        return float(num) / float(total)
    else:
        return 0

def create_genres_dict(movies, genres):
    for i in movies.keys():
        movie = movies[i]
        path = movie.path
        moviegenres = genres[i]
        categorygenres = dict()
        for p in path:
            if p not in categorygenres.keys():
                categorygenres[p] = dict()
            for mg in moviegenres:
                if mg in categorygenres[p]:
                    categorygenres[p][mg]+=1
                else:
                    categorygenres[p][mg] = 1
    
    return categorygenres

def update_path(movie, oldpath, newpath, genres, cg):
    
    for p in oldpath:
        if p in cg:
            olddict = cg[p]
            mg = genres[movie.id]
            for gg in mg:
                if gg in olddict:
                    if olddict[gg] > 0:
                        olddict[gg]-=1
    
    for p in newpath:
        if p in cg:
            newdict = cg[p]
        else:
            newdict = dict()
            cg[p] = newdict
        
        mg = genres[movie.id]
        for gg in mg:
            if gg in newdict:
                newdict[gg]+=1
            else:
                newdict[gg] = 1