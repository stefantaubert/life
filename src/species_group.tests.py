import unittest

class SpeciesGroupTests(unittest.TestCase):
    def test1(self):
        classes = [1, 2, 3, 4, 5, 6]
        a = [1, 2, 3, 4]
        b = [2, 1, 3, 5, 6]
        c = [3, 1, 2, 5]
        d = [4, 1, 5, 6]
        e = [5, 2, 3, 4, 6]
        f = [6, 2, 4, 5]
        g = [7]
        group1 = [1, 2, 3]
        group2 = []

        g_a = [1,2,3,4, 2,1,3,5,6, 3,1,2,5, 4,1,5,6] = [1,1,1,1, 2,2,2, 3,3,3, 4,4, 5,5,5] = [1,2,3,5]
        g_b = [2,1,3,5,6, 1,2,3,4, 3,1,2,5 5,2,3,4,6, 6,2,4,5] = [1,1,1 2,2,2,2,2, 3,3,3,3, 4,4,4, 5,5,5,5, 6,6,6] = [2,3,5]
        g_c = [3,1,2,5, 1,2,3,4, 2,1,3,5,6, 5,2,3,4,6] = [1,1,1, 2,2,2,2, 3,3,3,3, 4,4, 5,5,5] = [1,2,3,5]
        g_d = [4,1,5,6, 1,2,3,4, 5,2,3,4,6, 6,2,4,5] = [1,1, 2,2,2, 3,3, 4,4,4,4, 5,5,5, 6,6,6] = [2,4,5,6]
        g_e = [5,2,3,4,6, 2,1,3,5,6, 3,1,2,5, 4,1,5,6, 6,2,4,5] = [1,1,1, 2,2,2,2, 3,3,3, 4,4,4, 5,5,5,5,5, 6,6,6,6] = [2,5,6]
        g_f = [6,2,4,5, 2,1,3,5,6, 4,1,5,6, 5,2,3,4,6] = [1,1, 2,2,2, 3,3, 4,4,4, 5,5,5,5, 6,6,6,6] = [5,6]
        g_g = [7]
        
        dictionary = {1: set([2,3,4]), 2: set([1,3,5]), 3: set([1,2, 4]), 4: set([]), 5: set([2,6]), 6:set([5])}
        groups = species_group.find_groups(dictionary)
        self.assertEqual(len(groups), 3)

        self.assertEqual(groups[0], dictionary[1].intersection(dictionary[2]).intersection(dictionary[3])) # [1,2,3]
        self.assertEqual(groups[0], [4])
        self.assertEqual(groups[0], [5,6])


if __name__ == '__main__':
    unittest.main()