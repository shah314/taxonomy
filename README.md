# Taxonomy for Recommender Systems
### Shalin Shah

An implementation of the Taxonomy Discovery for Personalized Recommendation paper on the <a href="https://grouplens.org/datasets/movielens/" target="_blank">MovieLens</a> (small) dataset. The code is written in python.
The original paper can be found <a href="https://research.google/pubs/pub42499/" target="_blank">here</a>.

The algorithm alternates between latent factor updates and taxonomy path sampling. The latent factors are used to generate recommendations.<br><br>
Path sampling uses the latent factors and the genres of the movies in a Gibbs sampling procedure to generate new paths for movies.<br><br>
The initial taxonomy is generated randomly and then movies are assigned to nodes randomly. The Chinese restaurant process is not used.<br><br>
As iterations progress, the taxonomy as well as the latent factors are updated using Gibbs sampling and gradient descent respectively.

### Results
Random initialization hit rate@10:<br><b>3%</b><br><br>
Hit rate@10 after 10 iterations:<br><b>48%</b><br><br>
A random sample of 10% of the movies are taken for the hit rate calculation (as negative sampling).
