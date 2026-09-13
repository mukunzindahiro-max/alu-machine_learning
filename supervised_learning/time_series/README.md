# Time Series Forecasting

This directory forecasts the Bitcoin (BTC) close price one hour ahead from
the previous 24 hours of trading, using a recurrent network trained on
mean squared error.

## Files

| File | Description |
| --- | --- |
| `preprocess_data.py` | Turns the raw per-minute coinbase and bitstamp files into a scaled hourly series saved as `preprocessed_btc.npz` |
| `forecast_btc.py` | Builds, trains, and validates the keras RNN on that series |

## Data

Both scripts expect the raw datasets where the rest of this repository
keeps them:

```
../Data/coinbaseUSD_1-min_data_2014-12-01_to_2019-01-09.csv
../Data/bitstampUSD_1-min_data_2012-01-01_to_2020-04-22.csv
```

Each row is one 60 second window holding the start time in Unix time, the
open, high, low, and close price in USD, the amount of BTC transacted, the
amount of USD transacted, and the volume-weighted average price.

## Preprocessing

`preprocess_data.py` answers the questions the task raises as follows.

**Are all of the data points useful?** No. Minutes in which nothing traded
are blank in the raw files and are dropped. Hours where neither exchange
recorded a trade carry the last known price forward, since a price that was
never traded away from has not changed, and their traded amounts are set to
zero.

**Are all of the data features useful?** No. `Open` restates the previous
window's close and `Volume_(Currency)` is `Volume_(BTC)` scaled by the
price, so both are dropped as redundant. The model keeps `High`, `Low`,
`Close`, `Volume_(BTC)`, and `Weighted_Price`.

**Should you rescale the data?** Yes. The features range from single-digit
coin amounts to five-figure dollar prices, which trains poorly, so each is
centered and scaled to unit variance. Volume is heavy tailed and is passed
through `log1p` first. The mean and deviation come from the training set
only, so the hours the model is scored on never influence its inputs, and
both are stored in the archive so a prediction can be read back in dollars.

**Is the current time window relevant?** A single minute says very little
about the next hour, so the minute rows are aggregated into hourly windows:
high is the maximum, low the minimum, close the last value, volumes are
summed, and the weighted price is averaged. Data before 2017 is also
dropped, because BTC traded thinly below \$1000 then and that market does
not resemble the one being forecast.

**How should you save this preprocessed data?** As a compressed
`preprocessed_btc.npz` archive holding the three chronological subsets
(70% train, 15% validation, 15% test), the scaling statistics, the feature
names, and the index of the close column.

Both exchanges are used: bitstamp spans the whole period and is the primary
series so that prices never jump between venues mid-series, while coinbase
fills only the hours bitstamp is missing.

## Model

`forecast_btc.py` feeds the series to the model through a
`tf.data.Dataset`. Windows of 25 consecutive hours are cut with a stride of
one hour; the first 24 hours of every feature are the input and the close
price of the 25th hour is the target. Training windows are shuffled, and
windows are only ever cut within a single subset, so no window straddles
the train, validation, and test boundaries.

The network is a 64 unit LSTM that reduces the window to one state, dropout
at 0.2 because neighbouring windows overlap heavily, and a single linear
unit that reads the next close off that state. It is compiled with Adam and
mean squared error, trained for up to 20 epochs, and stopped early when the
validation loss stops improving, restoring the best weights.

## Usage

```
./preprocess_data.py
./forecast_btc.py
```

The first writes `preprocessed_btc.npz` and reports how many hours went to
each subset. The second prints the model summary, a per-epoch table of
training and validation loss, the test MSE on the scaled prices, and that
error converted back to dollars, then saves the trained model to
`forecast_btc.h5`.
