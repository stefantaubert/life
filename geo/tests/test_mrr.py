import unittest
import pandas as pd

from geo.metrics.mrr import mrr_score
from geo.metrics.mrr import mrr_score_df

class TestMrrEvaluationMethod(unittest.TestCase):
    '''Tests the calculation of the mrr'''

    def test_mrr_zeros(self):
        score = mrr_score([1, 2, 3, 0, 8, 0, 0, 7])
        self.assertEqual(1/8 * (1/1 + 1/2 + 1/3 + 1/8 + 1/7), score)

    def test_mrr_zero(self):
        score = mrr_score([0])
        self.assertEqual(0, score)
        
    def test_mrr1(self):
        score = mrr_score([1])
        self.assertEqual(1, score)

    def test_mrr2(self):
        score = mrr_score([1, 2])
        self.assertEqual(1/2 * (1/1 + 1/2), score)
    
    def test_mrr3(self):
        score = mrr_score([1, 2, 3])
        self.assertEqual(1/3 * (1/1 + 1/2 + 1/3), score)
    
    def test_mrr4(self):
        score = mrr_score([1, 2, 3, 6])
        self.assertEqual(1/4 * (1/1 + 1/2 + 1/3 + 1/6), score)

    def test_mrr5(self):
        score = mrr_score([10000, 132654])
        self.assertEqual(1/2 * (1/10000 + 1/132654), score)

    def test_mrr_df(self):
        sol_rows = []
        sol_row = []
        sol_row.append("")#current_glc_id
        sol_row.append("")#current_species
        sol_row.append("")#current_prediction
        sol_row.append("1")#current_rank

        sol_rows.append(sol_row)

        sol_row = []
        sol_row.append("")#current_glc_id
        sol_row.append("")#current_species
        sol_row.append("")#current_prediction
        sol_row.append("2")#current_rank

        sol_rows.append(sol_row)

        result_ser = pd.DataFrame(sol_rows, columns = ['glc_id', 'species_glc_id', 'probability', 'rank'])
        score = mrr_score_df(result_ser)

        self.assertEqual(1/2 * (1/1 + 1/2), score)

if __name__ == '__main__':
    unittest.main()