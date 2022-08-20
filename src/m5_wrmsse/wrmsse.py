import numpy as np
import pandas as pd
import importlib.resources

from . import data
from . import aggregation

def _rmsse(test, forecast, train_mse):
    """
    Calculate the Root Mean Squared Scaled Error of the
    aggregated forecast dataframe, which is to be of shape
    (42840,28). 
    """
    forecast_mse = np.mean((test - forecast)**2, axis=1)
    return np.sqrt(forecast_mse / train_mse)

        
def wrmsse(forecast: np.ndarray) -> float:  
    """
    Return the WRMSSE of a 28-day forecast for the M5 dataset
    """
    if not isinstance(forecast, (list, np.ndarray)):
        raise TypeError('Forecast must be of type list or numpy array')
    elif np.shape(forecast) != (30490, 28):
        raise ValueError('Forecast must be of dimensions (30490, 28)')
    else:
        forecast = pd.DataFrame(forecast)
    try:
        sales_ids = pd.read_csv(
            importlib.resources.path(data, 'sales_ids.csv.gz'),
            index_col = False,
        )
        test_agg = pd.read_csv(
            importlib.resources.path(data, 'test_agg.csv.gz'),
            index_col = False,
        )                             
        train_mse = pd.read_csv(
            importlib.resources.path(data, 'train_mse.csv.gz'),
            index_col = False,
        )
        train_mse = train_mse.values.flatten()
        weights = pd.read_csv(
            importlib.resources.path(data, 'weights.csv.gz'),
            index_col = False,
        )
        weights = weights.values.flatten()
    except FileNotFoundError as missing_file:
        print(f'Unable to complete, missing file: {missing_file.filename}')
        return
    forecast = pd.concat((sales_ids, forecast), axis=1)
    forecast_agg = aggregation.aggregate(forecast)
    rmsse = _rmsse(
        test_agg.values,
        forecast_agg.values,
        train_mse,
    )
    return (weights * rmsse).sum()
