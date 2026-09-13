#!/usr/bin/env python3
"""
Preprocesses the raw coinbase and bitstamp BTC datasets

The raw files hold one row per 60 second window, cover years of trading at
prices that no longer resemble the market being forecast, and leave every
minute without a trade empty. This module turns them into a single hourly
series of scaled features and stores it in a compressed .npz archive that
forecast_btc.py can load directly.
"""


import numpy as np
import pandas as pd


COINBASE = '../Data/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv'
BITSTAMP = '../Data/bitstampUSD_1-min_data_2012-01-01_to_2020-04-22.csv'
OUTPUT = 'preprocessed_btc.npz'

# BTC traded thinly below $1000 until 2017, so earlier rows describe a
# market that no longer behaves like the one being forecast
START_DATE = '2017-01-01'

# 'Open' restates the previous close and 'Volume_(Currency)' is
# 'Volume_(BTC)' scaled by the price, so neither carries new information
FEATURES = ['High', 'Low', 'Close', 'Volume_(BTC)', 'Weighted_Price']

# volume is heavy tailed, so it is compressed before being standardized
LOG_FEATURES = ['Volume_(BTC)']

# the series is split in time order: the model may never see its future
TRAIN_FRACTION = 0.7
VALIDATION_FRACTION = 0.15


def load_minute_data(path):
    """
    Reads one raw dataset and indexes it by time

    parameters:
        path [str]: path to a raw 1 minute csv file

    returns:
        pandas.DataFrame of minute rows indexed by timestamp,
            with the empty minutes dropped
    """
    data = pd.read_csv(path)
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')
    data = data.set_index('Timestamp').sort_index()
    return data.dropna()


def to_hourly(data):
    """
    Aggregates minute rows into the hourly windows being forecast

    A single minute says little about where the price is heading, so the
    rows are collapsed into the one hour horizon the model predicts.

    parameters:
        data [pandas.DataFrame]: minute rows indexed by timestamp

    returns:
        pandas.DataFrame of hourly rows, empty hours left as NaN
    """
    return data.resample('60min').agg({'Open': 'first',
                                       'High': 'max',
                                       'Low': 'min',
                                       'Close': 'last',
                                       'Volume_(BTC)': 'sum',
                                       'Volume_(Currency)': 'sum',
                                       'Weighted_Price': 'mean'})


def merge_exchanges(coinbase_path=COINBASE, bitstamp_path=BITSTAMP):
    """
    Builds one continuous hourly series out of both exchanges

    bitstamp covers the whole period and is used throughout so that the
    series never jumps between exchanges; coinbase only fills the hours
    bitstamp is missing.

    parameters:
        coinbase_path [str]: path to the raw coinbase csv file
        bitstamp_path [str]: path to the raw bitstamp csv file

    returns:
        pandas.DataFrame of hourly rows covering both exchanges
    """
    coinbase = to_hourly(load_minute_data(coinbase_path))
    bitstamp = to_hourly(load_minute_data(bitstamp_path))
    merged = bitstamp.combine_first(coinbase)
    return merged[merged.index >= START_DATE]


def fill_gaps(hourly):
    """
    Fills the hours in which neither exchange recorded a trade

    An hour without trades means the price never moved, so the last known
    prices are carried forward while the traded amounts are set to zero.

    parameters:
        hourly [pandas.DataFrame]: hourly rows that may contain NaN

    returns:
        pandas.DataFrame of hourly rows with no missing values
    """
    filled = hourly.copy()
    volumes = ['Volume_(BTC)', 'Volume_(Currency)']
    prices = [column for column in filled.columns if column not in volumes]
    filled[prices] = filled[prices].ffill()
    filled[volumes] = filled[volumes].fillna(0)
    return filled.dropna()


def split(series):
    """
    Splits a series into training, validation, and test sets

    The split is chronological rather than random: shuffling first would
    let the model train on hours that follow the ones it is scored on.

    parameters:
        series [numpy.ndarray of shape (hours, features)]:
            the hourly feature series

    returns:
        train, validation, test [numpy.ndarray]: the three subsets
    """
    hours = series.shape[0]
    train_end = int(hours * TRAIN_FRACTION)
    validation_end = int(hours * (TRAIN_FRACTION + VALIDATION_FRACTION))
    return (series[:train_end],
            series[train_end:validation_end],
            series[validation_end:])


def scale(train, validation, test):
    """
    Standardizes each feature using the training set statistics only

    The features span dollars and coin amounts across several orders of
    magnitude, which an RNN trains on poorly, so each one is centered and
    reduced to unit variance. The statistics come from the training set
    alone to keep the later hours out of the model's reach.

    parameters:
        train [numpy.ndarray]: the training subset
        validation [numpy.ndarray]: the validation subset
        test [numpy.ndarray]: the test subset

    returns:
        scaled_sets, mean, std
            scaled_sets [tuple of numpy.ndarray]: the standardized subsets
            mean [numpy.ndarray]: the per feature training mean
            std [numpy.ndarray]: the per feature training deviation
    """
    mean = train.mean(axis=0)
    std = train.std(axis=0)
    std[std == 0] = 1
    scaled = tuple((subset - mean) / std
                   for subset in (train, validation, test))
    return scaled, mean, std


def preprocess(coinbase_path=COINBASE, bitstamp_path=BITSTAMP, output=OUTPUT):
    """
    Runs the whole pipeline and saves the result

    The archive holds the three scaled subsets, the statistics needed to
    read a prediction back in dollars, and the index of the close column
    the model is trained to predict.

    parameters:
        coinbase_path [str]: path to the raw coinbase csv file
        bitstamp_path [str]: path to the raw bitstamp csv file
        output [str]: path of the .npz archive to write

    returns:
        the path the archive was written to
    """
    hourly = fill_gaps(merge_exchanges(coinbase_path, bitstamp_path))
    series = hourly[FEATURES].copy()
    for feature in LOG_FEATURES:
        series[feature] = np.log1p(series[feature])
    series = series.to_numpy(dtype='float64')

    train, validation, test = split(series)
    scaled, mean, std = scale(train, validation, test)

    np.savez_compressed(output,
                        train=scaled[0].astype('float32'),
                        validation=scaled[1].astype('float32'),
                        test=scaled[2].astype('float32'),
                        mean=mean,
                        std=std,
                        features=np.array(FEATURES),
                        close_index=FEATURES.index('Close'))
    return output


if __name__ == '__main__':
    path = preprocess()
    archive = np.load(path, allow_pickle=False)
    print('wrote {}'.format(path))
    for name in ('train', 'validation', 'test'):
        print('{}: {} hours'.format(name, archive[name].shape[0]))
