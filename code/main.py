#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 09:15:13 2021

@author: Shalin Shah

An implementation of the taxonomy discovery for personalized recommendations paper.
The algorithm alternates between latent factor updates and path sampling.
The latent factors are used to generate recommendations.
Path sampling uses the latent factors and the genres of the movies in a Gibbs sampling algorithm to generate new paths for movies
The initial taxonomy is generated randomly and then movies are assigned to nodes randomly.
As iterations progress, the taxonomy as well as the latent factors are updated.

The paper can be found here:
https://research.google/pubs/pub42499/

"""

from file_reader import read_ratings, create_random_taxonony, assign_random_paths, read_genres
from factor_update import update_latent_factors
from measurement import hit_rate
import random
from path_sampling import sample_paths
import numpy as np

# Numnber of iterations
iterations = 10

# The random number seeds
np.random.seed(314)
random.seed(314)

# The learning rate, which is exponentially decreased as iterations progress
learning_rate = 1

# The movielens ratings file
ratings_file = "../data/ratings.csv"

# The movielens file that contains the genres of the movies, used in path sampling
genres_file = "../data/movies.csv"

print("Reading genres...")
genres = read_genres(genres_file)
print("Reading Ratings...")
users, movies = read_ratings(ratings_file)
print("Number of users: " + str(len(users)))
print("Number of movies: " + str(len(movies)))
print("Creating random taxonomy...")
root, categories = create_random_taxonony(4)
print("Number of nodes in the taxonomy: " + str(len(categories)))
print("Assigning movies to random nodes...")
assign_random_paths(movies, root, categories)
print("Calculating initial hit rate...")
hits = hit_rate(movies, users) / len(users)
print("Number of users hits " + str(hits))
print("Updating latent factors...")
for i in range(0, iterations):
    learning_rate = learning_rate / np.exp(i)
    print("Iteration " + str(i))
    print("Updating Factors...")
    update_latent_factors(movies, users, categories, root, learning_rate)
    print("Sampling Paths...")
    sample_paths(categories, movies, genres)

print("Calculating final hit rate...")
hits = hit_rate(movies, users) / len(users)
print("Number of users hits after factor update " + str(hits))
