import numpy as np

data = np.load('highestIndividual.npz')

lst = [data[key] for key in data]

print("The fittest individual from your last run was:\n", lst)
