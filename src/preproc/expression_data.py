import pandas as pd

from os import path
from sys import platform

def load():
    prefix = 'G:' if platform == 'win32' else '/Volumes/GoogleDrive'
    data_folder = path.join(prefix, 'Shared drives/NIAAA_ASSIST/Data')
    derived_data_folder = path.join(data_folder, 'eda_derived')
    expression_meta_path = path.join(derived_data_folder, 'expression_meta.csv')
    if path.exists(expression_meta_path):
        expression_meta = pd.read_csv(expression_meta_path, low_memory = False)
    else:
        network_only_expression_path = path.join(derived_data_folder, 'network_only_expression.csv')
        if path.exists(network_only_expression_path):
            network_only_expression = pd.read_csv(network_only_expression_path, low_memory = False)
        else:
            expression = pd.read_csv(path.join(data_folder, 'kapoor2019_batch.age.rin.sex.pm.alc.corrected.coga.inia.expression.txt'), sep = '\t')
            network_ids_path = path.join(derived_data_folder, 'eda_derived/network_IDs.csv')
            if path.exists(network_ids_path):
                network_IDs = pd.read_csv(path.join(derived_data_folder, 'eda_derived/network_IDs.csv'), index_col = 0)
            else:
                adj_df = pd.read_csv(path.join(data_folder), 'Kapoor_adjacency.csv', index_col = 0)
                network_IDs = pd.Series(adj_df.columns)
                network_IDs.to_csv(network_ids_path)
            network_only_expression = expression[expression.id.isin(network_IDs['0'])]
            network_only_expression.to_csv(network_only_expression_path, index = 0)
        network_only_expression_t = network_only_expression.T
        network_only_expression_t.drop('id', inplace=True)
        meta = pd.read_csv(path.join(data_folder, 'kapoor2019_coga.inia.detailed.pheno.04.12.17.csv'))
        expression_meta = pd.merge(network_only_expression_t, meta, left_index = True, right_on = 'IID')
        expression_meta.to_csv(expression_meta_path, index = 0)
    
    return expression_meta

expression_meta = load()