import pandas as pd
import os

def save(dir, sheets, sheets_name):
    
    for sheet, name in zip(sheets, sheets_name):

        dataframe = pd.DataFrame(sheet)
        file = os.path.join(dir, name+'.csv')
        dataframe.to_csv(path_or_buf=file, sep=';', index=False)
