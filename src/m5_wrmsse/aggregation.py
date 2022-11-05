import pandas as pd

def aggregate(df: pd.DataFrame) -> pd.DataFrame:
    """ 
    Perform the 12 levels of aggregation as described in the M5
    Competitors Guide
    """
    df_agg = pd.DataFrame([])
    for v in levels.values():
        if v == None:
            agg = df.sum(numeric_only=True)
            agg = agg.to_frame().T
        else:
            agg = df.groupby(by=v).sum(numeric_only=True)
        df_agg = pd.concat([df_agg, agg])
    return df_agg


levels = {
    'level_1': None,
    'level_2': ['state_id'],
    'level_3': ['store_id'],
    'level_4': ['cat_id'],
    'level_5': ['dept_id'],
    'level_6': ['state_id', 'cat_id'],
    'level_7': ['state_id', 'dept_id'],
    'level_8': ['store_id', 'cat_id'],
    'level_9': ['store_id', 'dept_id'],
    'level_10': ['item_id'],
    'level_11': ['item_id', 'state_id'],
    'level_12': ['id']
}
