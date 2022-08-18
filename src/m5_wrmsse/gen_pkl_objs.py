import numpy as np
import pandas as pd
import importlib.resources
import data

from .aggregation import aggregation


def _gen_weights(sales, calendar, prices):
    """
    Generate the weights for each store-product combination aggregated
    over the 12 levels. Weights are the percentage of total revenue for
    the final 28 days of sales of the training period, ie [-58:-28]
    """
    print('Creating weights file...')
    sales_lm = sales.iloc[:,-56:-28].set_index(sales['id'])
    wm_d = calendar[calendar['d'].isin(sales_lm.columns)]
    prices_lm = prices[prices['wm_yr_wk'].isin(wm_d['wm_yr_wk'].unique())]
    prices_lm = (prices_lm
                 .merge(wm_d, how='left', on='wm_yr_wk')
                 .pivot_table(index=['store_id','item_id'], 
                              columns='d',values='sell_price')
                 .merge(sales[['id','item_id', 'store_id']], 
                        how='left', on=['item_id', 'store_id'])
                 .set_index('id')
                 .drop(['item_id','store_id'], axis=1)
                 .reindex(index=sales_lm.index)       
                )
    revenue_lm = (sales_lm * prices_lm).sum(axis=1)
    revenue_pct = ((revenue_lm / revenue_lm.sum())
                   .to_frame(name='revenue_pct')
                   .reset_index()
                   .merge(sales.loc[:,:'state_id'], how='left', on='id')
                  )
    weights = pd.Series([], dtype='float64')
    for v in agg_levels.values():
        if v == None:
            w = pd.Series([1])
        else:
            w = revenue_pct.groupby(by=v).sum()['revenue_pct']
        weights = pd.concat([weights,w])
    weights = weights * 1/12
    weights.to_pickle(
        importlib.resources.path('data', 'weights.pkl.zip')
    )
    
def _gen_sales_ids(sales):
    """
    Save the categorical data from the training set, this will be
    used to concatenate with the forecasts so the 12-level aggregation
    can be performed using the _aggregation() function.
    """
    print('Creating sales IDs file...')
    sales_ids = sales.loc[:,:'state_id']
    sales_ids.to_pickle(
        importlib.resources.path('data', 'sales_ids.pkl.zip')
    )

    
def _gen_train_mse(sales):
    """
    Calculate the mean squared error for each row in the training 
    set. This will be used in the RMSSE calculation.
    """
    print('Creating train MSE file...')
    train_agg = _aggregation(sales.iloc[:,:-28])
    train_mse = [np.mean((np.diff(np.trim_zeros(row))**2)) 
                 for row in train_agg.values]
    pd.Series(train_mse).to_pickle(
        importlib.resources.path('data', 'train_mse.pkl.zip')
    )
    

def _gen_test_agg(sales):
    print('Creating aggregated test file...')
    test = sales.drop(list(sales)[6:-28], axis=1)
    test_agg = _aggregation(test)
    test_agg.to_pickle(
        importlib.resources.path('data', 'test_agg.pkl.zip')
    )
    

def _gen_pkl_objs():
    """ 
    Create and pickle dataframes required to run the wrmsse function. 
    Requires sales_train_evaluation.csv, sell_prices.csv and
    calendar.csv which are available through Kaggle:
    https://www.kaggle.com/competitions/m5-forecasting-accuracy/data
    """
    try:
        sales = pd.read_csv('sales_train_evaluation.csv')
        calendar = pd.read_csv('calendar.csv')
        prices = pd.read_csv('sell_prices.csv')
        _gen_weights(sales, calendar, prices)
        _gen_sales_ids(sales)
        _gen_train_mse(sales)
        _gen_test_agg(sales)
    except FileNotFoundError as missing:
        print(f'Cannot complete, missing file: {missing.filename}')

        
