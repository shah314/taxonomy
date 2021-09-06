#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:17:46 2021

@author: Shalin Shah
"""
from classes import User, Movie, Category
import numpy as np

# Read the ratings file
def read_ratings(ratings_file):
    
    # Create a random state, a random number generator initialized using a seed
    rng = np.random.RandomState(314)
    file = open(ratings_file, "r")
    header = True
    users = dict()
    movies = dict()
    for line in file:
        if header:
            header = False
            continue
    
        sp = line.split(",")
        userid = sp[0]
        movieid = sp[1]
        rating = float(sp[3])
        
        user = User(userid)
        if userid in users.keys():
            user = users[userid]
                        
        user.ratings[movieid] = rating
        users[userid] = user
        
        if rng.uniform() < 0.7:
            if rating > 3:
                user.trainp[movieid] = rating
            else:
                user.trainn[movieid] = rating
        else:
            if rating > 3:
                user.test[movieid] = rating
        
        movie = Movie(movieid)
        if movieid in movies.keys():
            movie = movies[movieid]
        
        movies[movieid] = movie
        
    return users, movies

# Create a random taxonomy with num_children of each node, five levels deep.
# There are 341 nodes in the taxonomy
def create_random_taxonony(num_children):
    categories = dict()
    
    root = Category(0)
    categories[0] = root
    count = 1
    for i in range(0, num_children):
        child = Category(count)
        root.children.add(count)
        child.parent = root.id
        categories[count] = child
        count+=1
        for j in range(0, num_children):
            child1 = Category(count)
            child1.parent = child.id
            child.children.add(count)
            categories[count] = child1
            count+=1
            
            for k in range(0, num_children):
                child2 = Category(count)
                child2.parent = child1.id
                child1.children.add(count)
                categories[count] = child2
                count+=1
                
                for l in range(0, num_children):
                    child3 = Category(count)
                    child3.parent = child2.id
                    child2.children.add(count)
                    categories[count] = child3
                    count+=1
            
    return root, categories

# Assign items to a random path in the taxonomy
def assign_random_paths(items, root, categories):
    
    rng = np.random.RandomState(314)

    for i in items.keys():
        item = items[i]
        path = list()
        
        path.append(root.id)
        
        c = list(root.children)
        rand = int(rng.uniform() * len(c))
        nextcat = c[rand]
        path.append(nextcat)
        
        cattwo = categories[nextcat]
        c = list(cattwo.children)
        rand = int(rng.uniform() * len(c))
        nextcat = c[rand]
        path.append(nextcat)
        
        catthree = categories[nextcat]
        c = list(catthree.children)
        rand = int(rng.uniform() * len(c))
        nextcat = c[rand]
        path.append(nextcat)
        
        catfour = categories[nextcat]
        c = list(catfour.children)
        rand = int(rng.uniform() * len(c))
        nextcat = c[rand]
        path.append(nextcat)
        
        item.path = path

# Read the genres of the movies from the movielens data.
def read_genres(genresfile):
    f = open(genresfile, "r")
    genres = dict()
    for line in f:
        sp = line.split(",")
        movieid = sp[0]
        g = sp[2].strip().lower()
        sp = g.split("|")
        genres[movieid] = sp
   
    return genres

    