import pickle as pkl
import pandas as pd


with open('files/_analytical_data/_ana_heuristic_bestfit_area_numpy.pkl', 'rb') as f:
    print('-' * 111)
    print('ANALYTICAL DATA OF heuristic_bestfit_area_numpy.py'.center(111))
    print('-' * 111)

    df = pkl.load(f)
    print(df.describe())