from datetime import datetime
import pandas as pd
import numpy as np
from path import Path
import re
from cStringIO import StringIO
import csv

def load_data(data_dir):
    data_dir = Path(data_dir)
    data = {}
    for year in data_dir.listdir():
        for month in year.listdir():
            for csv_path in month.listdir():
                with open(csv_path, 'r') as fp:
                    data[csv_path.basename()[-12:-4]] = fp.read()
    return data

def load_csv_from_string(csv_str):
    csv_fp = StringIO(csv_str)
    return load_csv(csv_fp)

IGNORE = set([
    'Current Date:',
])

READING_MAP = {
    'OZONE': 'ozone',
    'NOX': 'nox',
    'NO2': 'no2',
    'NO': 'no',
    'CO': 'co',
    'INTMP': 'temp',
    'PM2.5': 'pm',
}

def load_csv(csv_fp):
    reader = csv.reader(csv_fp)
    cur_reading = None
    data = {}
    for line in reader:
        if line[0] in IGNORE:
            continue
        match = re.match(r'\d\d (.*)', line[0])
        if match:
            first = match.group(1).split(' ')[0]
            if first in READING_MAP:
                cur_reading = READING_MAP[first]
            else:
                cur_reading = None
        if cur_reading is not None:
            site_name = line[1].lower()
            if cur_reading not in data:
                data[cur_reading] = {}
            data[cur_reading][site_name] = line[2:26]
    return data

def convert_to_matrix(data, reading_type):
    assert reading_type in READING_MAP.values()
    if reading_type not in data:
        return None
    data = data[reading_type]
    sites = sorted(data.keys())
    X = []
    for i in xrange(24):
        vec = []
        usable = True
        for site in sites:
            try:
                vec.append(float(data[site][i]))
            except:
                usable = False
        if usable:
            X.append(vec)
    return np.array(X)

def convert_time(data, reading_type):
    assert reading_type in READING_MAP.values()
    if reading_type not in data:
        return None
    data = data[reading_type]
    sites = sorted(data.keys())
    X = []
    for i in xrange(24):
        vec = []
        usable = True
        for site in sites:
            try:
                vec.append(float(data[site][i]))
            except:
                usable = False
        if usable:
            X.append(vec)
    return np.array(X)

def load_pandas(data_dir):
    csvs = load_data(data_dir)
    data_map = {}
    for c, text in csvs.iteritems():
        data_map[c] = load_csv_from_string(text)
    data_panel = {}
    for date in data_map:
        reading_data = {}
        for reading_type in data_map[date]:
            reading_data[reading_type] = pd.DataFrame(data_map[date][reading_type])
        data_panel[date] = reading_data
    D1 = pd.Panel4D(data_panel).convert_objects(convert_numeric=True).swapaxes(1, 2)
    final_data_map = {}
    for date in D1.keys():
        for time in D1[date].keys():
            year, month, day, hour = int(date[:4]), int(date[4:6]), int(date[6:8]), int(time)
            final_data_map[datetime(year, month, day, hour=hour)] = D1[date][time]
    data = pd.Panel(final_data_map).swapaxes(0, 1)
    return data
