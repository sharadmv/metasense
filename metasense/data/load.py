import numpy as np
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
AFTER_REMOVE = {
    4: 8,
}

X_columns = ['co-corr', 'co', 'co-u', 'co-A', 'co-W', 'no2-corr', 'no2', 'no2-u', 'no2-A', 'no2-W', 'o3-corr', 'o3', 'o3-u', 'o3-A', 'o3-W', 'temperature',
       'pressure', 'humidity', 'pt', 'nc', 'epa-temperature', 'epa-humidity']
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
        50.0:  1.28,
    },
}

BASE_VOLTAGE = {
    4: {
        'CO': {
            'W': 336,
            'A': 260,
        },
        'NO2': {
            'W': 250,
            'A': 270,
        },
        'O3': {
            'W': 278,
            'A': 380,
        },
    }
}

def get_multiplier(data, gas):
    temp = data['temperature']
    def correct(x):
        x1, x2 = np.floor(x / 10) * 10.0, np.ceil(x / 10) * 10.0
        if x1 == x2:
            return CORRECTIONS[gas][x1]
        y1, y2 = CORRECTIONS[gas][x1], CORRECTIONS[gas][x2]
        return (y2 - y1) / (x2 - x1) * (x - x1) + y1
    n = temp.map(correct)
    # n = temp.map(lambda x: 1)
    return n

def load_board(board_id, data_dir=Path('/home/sharad/data/metasense/la/')):
    data = pd.read_csv(data_dir / "csv"/ "B%u.csv" % board_id, index_col='datetime', parse_dates=True)
    data = data.iloc[INITIAL_REMOVE[board_id]:-AFTER_REMOVE[board_id]]

    data['co-corr'] = get_multiplier(data, 'CO')
    data['no2-corr'] = get_multiplier(data, 'NO2')
    data['o3-corr'] = get_multiplier(data, 'O3')

    data['co'] = (data['co-W'] - BASE_VOLTAGE[board_id]['CO']['W']) - data['co-corr'] * (data['co-A'] - BASE_VOLTAGE[board_id]['CO']['A'])
    data['no2'] = (data['no2-W'] - BASE_VOLTAGE[board_id]['NO2']['W']) - data['no2-corr'] * (data['no2-A'] - BASE_VOLTAGE[board_id]['NO2']['A'])
    data['o3'] = (data['o3-W'] - BASE_VOLTAGE[board_id]['O3']['W']) - data['o3-corr'] * (data['o3-A'] - BASE_VOLTAGE[board_id]['O3']['A'])
    data['co-u'] = data['co-W'] - data['co-A']
    data['no2-u'] = data['no2-W'] - data['no2-A']
    data['o3-u'] = data['o3-W'] - data['o3-A']

    if board_id != 9:
        train_data, test_data = data.loc[:"2016-08-18"], data.loc["2016-08-18":]
    else:
        train_data, test_data = data, None
    return (train_data[X_columns], train_data[Y_columns]), (test_data[X_columns], test_data[Y_columns])
