import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt


pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.expand_frame_repr = False


output_file_path = 'files/_ana_data_loaded_describe.txt'
char_count = 124


with open('files/_analytical_data/_ana_heuristic_bestfit_area_numpy_0.1.pkl', 'rb') as fi:
    df_area_01 = pkl.load(fi)
    with open(output_file_path, 'w') as fo:
        print('-' * char_count, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_area_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 0.1'.center(111), file=fo)
        print('-' * char_count, file=fo)
        print(df_area_01.describe(), file=fo)

with open('files/_analytical_data/_ana_heuristic_bestfit_area_numpy_1.pkl', 'rb') as fi:
    df_area_1 = pkl.load(fi)
    with open(output_file_path, 'a') as fo:
        print('-' * char_count, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_area_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 1'.center(111), file=fo)
        print('-' * char_count, file=fo)
        print(df_area_1.describe(), file=fo)

with open('files/_analytical_data/_ana_heuristic_bestfit_maxside_numpy_0.1.pkl', 'rb') as fi:
    df_maxside_01 = pkl.load(fi)
    with open(output_file_path, 'a') as fo:
        print('-' * char_count, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_maxside_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 0.1'.center(111), file=fo)
        print('-' * char_count, file=fo)
        print(df_maxside_01.describe(), file=fo)

with open('files/_analytical_data/_ana_heuristic_bestfit_maxside_numpy_1.pkl', 'rb') as fi:
    df_maxside_1 = pkl.load(fi)
    with open(output_file_path, 'a') as fo:
        print('-' * char_count, file=fo)
        print('ANALYTICAL DATA OF heuristic_bestfit_maxside_numpy.py WITH GLOBAL_TIME_LIMIT_PER_ITER = 1'.center(111), file=fo)
        print('-' * char_count, file=fo)
        print(df_maxside_1.describe(include='all'), file=fo)


print('Described data saved to', output_file_path)

df_area_01.plot(x='rect_count', y=['total cost'])
plt.savefig('files/_analytical_figures/df_area_01 total_cost')
df_area_01.plot(x='rect_count', y=['running time'])
plt.savefig('files/_analytical_figures/df_area_01 running time')
df_area_01.plot(x='rect_count', y=['time_exceeded_count'])
plt.savefig('files/_analytical_figures/df_area_01 time_exceeded_count')

df_area_1.plot(x='rect_count', y=['total cost'])
plt.savefig('files/_analytical_figures/df_area_1 total_cost')
df_area_1.plot(x='rect_count', y=['running time'])
plt.savefig('files/_analytical_figures/df_area_1 running time')


df_maxside_01.plot(x='rect_count', y=['total cost'])
plt.savefig('files/_analytical_figures/df_maxside_01 total_cost')
df_maxside_01.plot(x='rect_count', y=['running time'])
plt.savefig('files/_analytical_figures/df_maxside_01 running time')
df_maxside_01.plot(x='rect_count', y=['time_exceeded_count'])
plt.savefig('files/_analytical_figures/df_maxside_01 time_exceeded_count')

df_maxside_1.plot(x='rect_count', y=['total cost'])
plt.savefig('files/_analytical_figures/df_maxside_1 total_cost')
df_maxside_1.plot(x='rect_count', y=['running time'])
plt.savefig('files/_analytical_figures/df_maxside_1 running time')

print('Figures saved to files/_analytical_figures/')