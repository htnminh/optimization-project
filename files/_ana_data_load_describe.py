import pickle as pkl
import pandas as pd

pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.expand_frame_repr = False


with open('files/_analytical_data/_ana_heuristic_bestfit_area_numpy_0.1.pkl', 'rb') as fi:
    df = pkl.load(fi)
    with open('files/_ana_data_load_describe.txt', 'w') as fo:
        print('-' * 111, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_area_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 0.1'.center(111), file=fo)
        print('-' * 111, file=fo)
        print(df.describe(), file=fo)

with open('files/_analytical_data/_ana_heuristic_bestfit_area_numpy_1.pkl', 'rb') as fi:
    df = pkl.load(fi)
    with open('files/_ana_data_load_describe.txt', 'a') as fo:
        print('-' * 111, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_area_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 1'.center(111), file=fo)
        print('-' * 111, file=fo)
        print(df.describe(), file=fo)

with open('files/_analytical_data/_ana_heuristic_bestfit_maxside_numpy_0.1.pkl', 'rb') as fi:
    df = pkl.load(fi)
    with open('files/_ana_data_load_describe.txt', 'a') as fo:
        print('-' * 111, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_maxside_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 0.1'.center(111), file=fo)
        print('-' * 111, file=fo)
        print(df.describe(), file=fo)

with open('files/_analytical_data/_ana_heuristic_bestfit_maxside_numpy_1.pkl', 'rb') as fi:
    df = pkl.load(fi)
    with open('files/_ana_data_load_describe.txt', 'a') as fo:
        print('-' * 111, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_maxside_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 1'.center(111), file=fo)
        print('-' * 111, file=fo)
        print(df.describe(), file=fo)

print('Saved to files/_ana_data_load_describe.txt')