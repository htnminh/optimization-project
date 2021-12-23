import pickle as pkl
import pandas as pd


with open('files/_analytical_data/_ana_heuristic_bestfit_area_numpy.pkl', 'rb') as fi:
    df = pkl.load(fi)
    with open('files/_ana_data_load_describe.txt', 'w') as fo:
        print('-' * 111, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_area_numpy.py'.center(111), file=fo)
        print('-' * 111, file=fo)
        print(df.describe(), file=fo)

print('Saved to files/_ana_data_load_describe.txt')