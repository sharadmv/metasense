import pandas as pd
from path import Path
import warnings
warnings.filterwarnings('ignore')

INITIAL_REMOVE = {
    4: 40,
    10: 150,
    8: 100,
    9: 110
}

X_columns = ['co', 'no2', 'o3', 'temperature',
       'pressure', 'humidity', 'pt', 'nc']
Y_columns = ['epa-co', 'epa-no2', 'epa-o3']

CORRECTIONS = {
    'CO': {
        -30.0: 1.0,
        -20.0: 1.0,
        -10.0: 1.0,
        0.0:   1.0,
        10.0:  1.0,
        20.0:  1.0,
        30.0: -0.76,
        40.0: -0.76,
        50.0: -0.76,
    },
    'NO2': {
        -30.0: 1.09,
        -20.0: 1.09,
        -10.0: 1.09,
        0.0:   1.09,
        10.0:  1.09,
        20.0:  1.35,
        30.0:  3.00,
        40.0:  3.00,
        50.0:  3.00
    },
    'O3': {
        -30.0: 0.75,
        -20.0: 0.75,
        -10.0: 0.75,
        0.0:   0.75,
        10.0:  1.28,
        20.0:  1.28,
        30.0:  1.28,
        40.0:  1.28,
        50.0:  None,
    },
}

def get_multiplier(data, gas):
    temp = data['temperature'].round(-1)
    # n = temp.map(lambda x: CORRECTIONS[gas][x])
    n = temp.map(lambda x: 1)
    return n

def load_board(board_id, data_dir=Path('/home/sharad/data/metasense/la/')):
    data = pd.read_csv(data_dir / "csv"/ "B%u.csv" % board_id, index_col='datetime', parse_dates=True)
    data = data.iloc[INITIAL_REMOVE[board_id]:]
    data['co-corr'] = get_multiplier(data, 'CO')
    data['no2-corr'] = get_multiplier(data, 'NO2')
    data['o3-corr'] = get_multiplier(data, 'O3')
    data['co'] = data['co-W'] - data['co-corr'] * data['co-A']
    data['no2'] = data['no2-W'] - data['no2-corr'] * data['no2-A']
    data['o3'] = data['o3-W'] - data['o3-corr'] * data['o3-A']
    if board_id != 9:
        train_data, test_data = data.loc[:"2016-08-18"], data.loc["2016-08-18":]
    else:
        train_data, test_data = data, None
    return (train_data[X_columns], train_data[Y_columns]), (test_data[X_columns], test_data[Y_columns])
