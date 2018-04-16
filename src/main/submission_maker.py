import numpy as np
import data_paths
import pickle
from tqdm import tqdm
from scipy.stats import rankdata
import pandas as pd
from sklearn.model_selection import train_test_split
import json 

def make_submission_array(classes, predictions, glc_ids):
    '''
    Erstellt eine Submission mit den Einträgen in folgendem Schema: glc_id, species_glc_id, probability, rank.
    Ausgabe zb: [[1, "9", 0.5, 1], [1, "3", 0.6, 2], [2, "9", 0.7, 1], [2, "3", 0.6, 2]]
    Die glc_id ist dabei 1-basiert.
    '''
    assert len(glc_ids) == len(predictions)

    count_predictions = len(predictions)
    count_classes = len(classes)
    submission = []

    for i in tqdm(range(count_predictions)):
        current_glc_id = glc_ids[i]
        current_predictions = predictions[i]
        assert len(current_predictions) == count_classes

        current_ranks = rankdata(current_predictions, method="ordinal")
        # rang 100,99,98 zu rang 1,2,3 machen
        current_ranks = count_classes - current_ranks + 1
        current_glc_id_array = count_classes * [current_glc_id]
        submissions = [list(a) for a in zip(current_glc_id_array, classes, current_predictions, current_ranks)]
        submission.extend(submissions)
    
    return submission

def make_submission_df(classes, predictions, glc_ids):
    submission = make_submission_array(classes, predictions, glc_ids)
    submission_df = pd.DataFrame(submission, columns = ['glc_id', 'species_glc_id', 'probability', 'rank'])
    return submission_df

def make_submission():
    print("Make submission...")
    # y_ids = np.load(data_paths.y_ids)

    # np.save(data_paths.species_map_training, np.unique(y_ids))

    classes = np.load(data_paths.species_map_training)

    predictions = np.load(data_paths.prediction)
    df = make_submission_df(classes, predictions, glc_ids)

    print("Save submission...")
    df.to_csv(data_paths.submission_val, index=False)

    # y = None
    # with open(data_paths.species_map, 'rb') as f:
    #     y = pickle.load(f)
        
# def make_submission2():
#     print("Make submission...")    
#     #x_text = np.load(data_paths.x_text)
    
#     x_text = pd.read_csv(data_paths.occurrences_train_gen)
#     species = x_text.species_glc_id.unique()
#     #y = x_text.species_glc_id
#     x_text = x_text[['chbio_1', 'chbio_5', 'chbio_6','month', 'latitude', 'longitude']]

#     y = np.load(data_paths.y_array)
#     #species = np.load(data_paths.species_map)
#     y_predicted = np.load(data_paths.prediction)
#     x_train, x_valid, y_train, y_valid = train_test_split(x_text, y, test_size=train_val_split, random_state=seed)

#     # print("Validationset rows after removing unique species:", len(x_valid.index))

#     sol_rows = []

#     for i in tqdm(range(len(y_valid))):
#         current_pred_array = y_predicted[i]
#         current_glc_id = i
#         pred_r = rankdata(current_pred_array, method="ordinal")
#         # absteigend sortieren
#         pred_r = len(species) - pred_r + 1
       
#         i, = np.where(y_valid[i] == 1)
#         assert len(i) == 1

#         current_rank = int(pred_r[i])
#         current_species = int(species[i])
#         current_prediction = float(current_pred_array[i])

#         sol_row = []
#         sol_row.append(current_glc_id)
#         sol_row.append(current_species)
#         sol_row.append(current_prediction)
#         sol_row.append(current_rank)

#         sol_rows.append(sol_row)

#     # <glc_id;species_glc_id;probability;rank>        
#     result_ser = pd.DataFrame(sol_rows, columns = ['glc_id', 'species_glc_id', 'probability', 'rank'])
#     result_ser.to_csv(data_paths.submission_val, index=False)

def make_submission_for_current_training():
    print("Make submission...")

    classes = np.load(data_paths.current_training_species_map)

    predictions = np.load(data_paths.current_training_results)
    df = make_submission_df(classes, predictions)

    print("Save submission...")
    df.to_csv(data_paths.current_training_submission, index=False)

if __name__ == '__main__':
    make_submission_for_current_training()