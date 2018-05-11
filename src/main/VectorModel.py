import module_support_main
import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.model_selection import train_test_split
import data_paths_main as data_paths
import settings_main as settings
# from sklearn.model_selection import cross_val_score
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from joblib import Parallel, delayed
import multiprocessing
import submission_maker
import get_ranks
import mrr
import time
import main_preprocessing
import Log
import datetime
import xgboost as xgb
import matplotlib.pyplot as plt
import math
import mrr

class Model():

    def __init__(self):
        x_text = pd.read_csv(data_paths.train)
        x_test = pd.read_csv(data_paths.test)#, nrows = 7)

        self.y = x_text["species_glc_id"]
        self.train_columns = [ 
        #'bs_top', 'alti', 'chbio_12', 'chbio_15', 'chbio_17', 'chbio_3', 'chbio_6', 'clc', 'crusting', 'dimp'
        'chbio_1', 'chbio_2', 'chbio_3', 'chbio_4', 'chbio_5', 'chbio_6',
        'chbio_7', 'chbio_8', 'chbio_9', 'chbio_10', 'chbio_11', 'chbio_12',
        'chbio_13', 'chbio_14', 'chbio_15', 'chbio_16', 'chbio_17', 'chbio_18','chbio_19', 
        'etp', 'alti', 'awc_top', 'bs_top', 'cec_top', 'crusting', 'dgh', 'dimp', 'erodi', 'oc_top', 'pd_top', 'text',
        'proxi_eau_fast', 'clc', 'latitude', 'longitude'
        ]

        self.x_train = x_text[self.train_columns]
        self.x_test = x_test[self.train_columns]
        self.species_count = len(np.unique(self.y))
        print("Count of species", self.species_count)        

    def get_vector_length(self, v):
        summ = 0

        for num in v:
            summ += num * num

        distance = math.sqrt(summ)
        
        return distance

    def predict_train(self):
        ranks = []
        x_train_matrix = self.x_train.as_matrix()
        to_predict_matrix = self.x_train.as_matrix()
        y_train_matrix = self.y.as_matrix()
        
        for i in tqdm(range(len(to_predict_matrix))):
            row = np.array(to_predict_matrix[i])
            distances = []
            for j in range(len(x_train_matrix)):
                if i == j:
                    continue
                else:
                    train_row = x_train_matrix[j]
                    distance = self.get_vector_length(train_row - row)
                    distances.append(distance)
            
            _, species_sorted = zip(*sorted(zip(distances, list(self.y))))
            #print(distances_sorted)
            species_sorted = list(dict.fromkeys(species_sorted))
            
            solution = y_train_matrix[i]
            rank = species_sorted.index(solution) + 1 #da 1-basiert
            ranks.append(rank)
            print("Solutionindex:", rank)
            print("Average-Rank:", np.mean(ranks))
            print("Mrr:", mrr.mrr_score(ranks))


    def predict_test(self, use_multithread = True):
        print("Run model...")

        self.x_train_matrix = self.x_train.as_matrix()
        self.to_predict_matrix = self.x_test.as_matrix()
        species = sorted(np.unique(self.y))
        # print(species)
        np.save(data_paths.vector_species, species)
        self.fake_propabilities = [(self.species_count - i) / self.species_count for i in range(self.species_count)]

        if use_multithread:
            num_cores = multiprocessing.cpu_count()
            print("Cpu count:", str(num_cores))
            predictions = Parallel(n_jobs=num_cores)(delayed(self.predict_row)(row) for row in tqdm(range(len(self.to_predict_matrix))))
            #result = Parallel(n_jobs=num_cores)(delayed(self.calc_class)(class_name) for class_name in tqdm(self.class_names))
        else:
            predictions = []
            for row in tqdm(range(len(self.to_predict_matrix))):
                predictions.append(self.predict_row(row))
        
        #sort after rows
        #print(predictions)
        predictions = sorted(predictions)
        rows, props = zip(*predictions)
        #print(rows)
        #print(props)
        #print(np.array(props))
        print("Saving test predictions...")
        np.save(data_paths.vector_test_prediction, np.array(props))
        print("Finished.", data_paths.vector_test_prediction)
        assert len(predictions) == len(self.x_test.index)

    def predict_row(self, row_nr):
        # if row_nr >= 6000:
        #     return
        row = np.array(self.to_predict_matrix[row_nr])
        distances = []
        for j in range(len(self.x_train_matrix)):                
            train_row = self.x_train_matrix[j]
            distance = self.get_vector_length(train_row - row)
            distances.append(distance)
            
        _, species_sorted = zip(*sorted(zip(distances, list(self.y))))

        species_sorted = list(dict.fromkeys(species_sorted))
        fake_props = list(self.fake_propabilities)
        # print("NEW ITERATION------------------------------------")
        print(species_sorted[:100])
        # print(fake_props[:100])

        species_map, fake_propabilities_sorted = zip(*sorted(zip(species_sorted, fake_props)))

        #print(species_map[:100])
        # print(fake_propabilities_sorted[:100])

        return (row_nr, fake_propabilities_sorted)
        #print(probabilities)

if __name__ == '__main__':
    main_preprocessing.create_datasets()
    m = Model()
    #m.predict_train()
    m.predict_test()
