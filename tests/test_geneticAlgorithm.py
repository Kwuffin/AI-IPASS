import unittest
import geneticAlgorithm as ga
import numpy as np


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

    #  Tests if crossover individuals only get genes from both parents
    def test_crossover(self):
        p1 = ga.createIndividual(True, None)
        p2 = ga.createIndividual(True, None)

        parents = [p1, p2]

        population = ga.createPopulation(False, 5, parents)

        for individual in population:
            tableCounter = -1

            for table in individual:
                rowCounter = -1
                tableCounter += 1

                for row in table:
                    geneCounter = -1
                    rowCounter += 1

                    for gene in row:
                        geneCounter += 1

                        self.assertTrue(gene == p1[tableCounter].item(rowCounter, geneCounter) or
                                        gene == p2[tableCounter].item(rowCounter, geneCounter))
