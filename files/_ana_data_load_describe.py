import pickle as pkl
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.axes


# config
pd.options.display.max_rows = None
pd.options.display.max_columns = None
pd.options.display.max_colwidth = None
pd.options.display.expand_frame_repr = False

# plt.style.use('dark_background')


# consts
output_file_path = 'files/_ana_data_loaded_describe.txt'
char_count = 124


# write described data
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

df_CPM = pd.read_csv(r'scripts\output\_ana_CPM\analyze_CPM_L120_final.csv', header=0)
with open(output_file_path, 'a') as fo:
    print('-' * char_count, file=fo)
    print('ANALYTICAL DATA OF cp_model.py WITH time_limit = 120'.center(111), file=fo)
    print('-' * char_count, file=fo)
    print(df_CPM.describe(), file=fo)

df_CPM_dropped_na = df_CPM.dropna(how='any').copy()
with open(output_file_path, 'a') as fo:
    print('-' * char_count, file=fo)
    print('ANALYTICAL DATA (DROPPED N/A) OF cp_model.py WITH time_limit = 120 '.center(111), file=fo)
    print('-' * char_count, file=fo)
    print(df_CPM_dropped_na.describe(), file=fo)

print('Described data saved to', output_file_path)


# save figures
df_area_1.hist(column='rect_count', bins=10)
plt.title('rect_count or n_rect')
plt.xticks(list(range(0, 1001, 100)))
plt.savefig('files/_analytical_figures/hist_rects')

df_area_1.hist(column='car_count', bins=7)
plt.title('car_count or n_car')
plt.xticks(list(range(0, 351, 50)))
plt.savefig('files/_analytical_figures/hist_cars')

df_area_01.sort_values(by='rect_count', inplace=True)
df_area_01.plot(x='rect_count', y='total cost', kind='scatter')
plt.savefig('files/_analytical_figures/df_area_01 total cost')
df_area_01.plot(x='rect_count', y='running time', kind='scatter')
plt.savefig('files/_analytical_figures/df_area_01 running time')
df_area_01.plot(x='rect_count', y='time_exceeded_count', kind='scatter')
plt.savefig('files/_analytical_figures/df_area_01 time_exceeded_count')

df_area_1.sort_values(by='rect_count', inplace=True)
df_area_1.plot(x='rect_count', y='total cost', kind='scatter')
plt.savefig('files/_analytical_figures/df_area_1 total cost')
df_area_1.plot(x='rect_count', y='running time', kind='scatter')
plt.savefig('files/_analytical_figures/df_area_1 running time')

df_maxside_01.sort_values(by='rect_count', inplace=True)
df_maxside_01.plot(x='rect_count', y='total cost', kind='scatter')
plt.savefig('files/_analytical_figures/df_maxside_01 total cost')
df_maxside_01.plot(x='rect_count', y='running time', kind='scatter')
plt.savefig('files/_analytical_figures/df_maxside_01 running time')
df_maxside_01.plot(x='rect_count', y='time_exceeded_count', kind='scatter')
plt.savefig('files/_analytical_figures/df_maxside_01 time_exceeded_count')

df_maxside_1.sort_values(by='rect_count', inplace=True)
df_maxside_1.plot(x='rect_count', y='total cost', kind='scatter')
plt.savefig('files/_analytical_figures/df_maxside_1 total cost')
df_maxside_1.plot(x='rect_count', y='running time', kind='scatter')
plt.savefig('files/_analytical_figures/df_maxside_1 running time')

df_CPM_dropped_na.sort_values(by='n_rect', inplace=True)
df_CPM_dropped_na.plot(x='n_rect', y='cost', kind='scatter')
plt.savefig('files/_analytical_figures/df_CPM cost')
df_CPM_dropped_na.plot(x='n_rect', y='time_running', kind='scatter')
plt.savefig('files/_analytical_figures/df_CPM time_running')

print('Figures saved to files/_analytical_figures/')