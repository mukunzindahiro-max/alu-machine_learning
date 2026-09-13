#!/usr/bin/env python3
"""
Creates, trains, and validates a keras model that forecasts BTC

The model reads the past 24 hours of hourly BTC data, as produced by
preprocess_data.py, and predicts the close price of the following hour.
It is a recurrent network trained on mean squared error, and the windows
are fed to it through a tf.data.Dataset.
"""


import numpy as np
import pandas as pd
import tensorflow as tf


DATA = 'preprocessed_btc.npz'
MODEL = 'forecast_btc.h5'

# hours of history the model reads before each prediction
SEQUENCE_LENGTH = 24

BATCH_SIZE = 64
EPOCHS = 20
SHUFFLE_BUFFER = 10000


def make_dataset(series, close_index, shuffle=False):
    """
    Builds a tf.data.Dataset of (history, next close) pairs

    Each element pairs SEQUENCE_LENGTH consecutive hours of every feature
    with the close price of the hour that follows them. Windows are cut
    with a stride of one hour, so each hour is seen in several windows.

    parameters:
        series [numpy.ndarray of shape (hours, features)]:
            a scaled hourly feature series
        close_index [int]: column of the close price within the series
        shuffle [bool]: whether to shuffle the windows, used for training

    returns:
        tf.data.Dataset of batched (window, target) pairs
    """
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(SEQUENCE_LENGTH + 1, shift=1,
                             drop_remainder=True)
    dataset = dataset.flat_map(
        lambda window: window.batch(SEQUENCE_LENGTH + 1))
    dataset = dataset.map(
        lambda window: (window[:-1], window[-1:, close_index]))
    if shuffle:
        dataset = dataset.shuffle(SHUFFLE_BUFFER)
    return dataset.batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)


def build_model(features):
    """
    Builds the recurrent forecasting model

    A single LSTM layer summarizes the 24 hour window into one state, and
    a linear unit reads the next close price off that state. Dropout is
    applied to the summary because neighbouring windows overlap heavily
    and the model would otherwise memorize them.

    parameters:
        features [int]: number of features per hour

    returns:
        the compiled keras model
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(SEQUENCE_LENGTH, features)),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model


def forecast(data=DATA, model_path=MODEL):
    """
    Trains and validates the forecasting model

    parameters:
        data [str]: path of the archive written by preprocess_data.py
        model_path [str]: path to save the trained model to

    returns:
        model, history
            model: the trained keras model
            history: the keras history of the training run
    """
    archive = np.load(data, allow_pickle=False)
    close_index = int(archive['close_index'])

    train = make_dataset(archive['train'], close_index, shuffle=True)
    validation = make_dataset(archive['validation'], close_index)
    test = make_dataset(archive['test'], close_index)

    model = build_model(archive['train'].shape[1])
    model.summary()

    stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                patience=3,
                                                restore_best_weights=True)
    history = model.fit(train,
                        validation_data=validation,
                        epochs=EPOCHS,
                        callbacks=[stopping])

    epochs = pd.DataFrame(history.history)
    epochs.index.name = 'epoch'
    print(epochs)

    loss = model.evaluate(test, verbose=0)[0]
    # the model is trained on standardized prices, so undoing the scaling
    # reports the error in the dollars it was built to predict
    dollars = np.sqrt(loss) * archive['std'][close_index]
    print('test MSE (scaled): {:.6f}'.format(loss))
    print('test RMSE (USD): {:.2f}'.format(dollars))

    model.save(model_path)
    return model, history


if __name__ == '__main__':
    forecast()
