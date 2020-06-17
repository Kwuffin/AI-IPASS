import unittest
import geneticAlgorithm

class TestAlg(unittest.TestCase):

    def test_populationLength(self):
        population = geneticAlgorithm.createPopulation(True, 5, None)
        self.assertEqual(len(population), 5)
