import unittest
import geneticAlgorithm as ga
import numpy as np
import copy
import numpy.testing as npt


class TestAlg(unittest.TestCase):

    def test_indiv_creation_rand(self):
        individual = ga.createIndividual(True, None)

        #  Correct amount of Tables:
        self.assertEqual(len(individual), 3)

        #  Correct amount of columns and rows in table 1:
        self.assertEqual(len(individual[0]), 16)
        for row in individual[0]:
            self.assertEqual(len(row), 10)

        #  Correct amount of columns and rows in table 2:
        self.assertEqual(len(individual[1]), 8)
        for row in individual[1]:
            self.assertEqual(len(row), 10)

        #  Correct amount of columns and rows in table 3:
        self.assertEqual(len(individual[2]), 10)
        for row in individual[2]:
            self.assertEqual(len(row), 10)

    def test_population_length(self):
        population = ga.createPopulation(True, 5, None)
        self.assertEqual(len(population), 5)
