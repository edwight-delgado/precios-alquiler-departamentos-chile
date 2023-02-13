
#import hashlib
#import nltk
#from nltk.corpus import stopwords # los stopwords no nos añaden valor al análisis ulterior (la, los, nos, etc.)
from urllib.parse import urlparse
import pandas as pd 
import re
import numpy as np
import logging # con este módulo le vamos imprimiendo en la consola al usuario lo que está pasando
from sqlite3 import connect
import datetime
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO)


logger = logging.getLogger(__name__) # obtenemos una referencia a nuestro logger con nuestro nombre interno de python
def main(fecha_table):
    file_name = f'alquiler_{fecha_table}'
    transform(file_name)
    
def transform(fecha_table):
    file_name = f'alquiler_{fecha_table}'
    logger.info('Starting cleaning process')
    #----------------------

    #----------------------
    df = _read_data(file_name, types='sql')
    df = _to_lower(df)
    df = _to_datetime(df,'fecha')
    df['published_time'].fillna(value=np.nan, inplace=True)
    df['published_time']= df['published_time'].replace(np.nan, fecha_table)
    df['published'] = df['published_time'].apply(_published_datetime_format)
    df = _to_datetime(df,'published')
    df = _remove_duplicate_entries(df, 'link') # eliminamos duplicados
    df['divisa'] = df['precio'].apply(_extraer_text)
    df['precio'] = _price_format(df,'precio')
    df['gastos_comunes'] = _price_format(df,'gastos_comunes')
    df['dormitorios'] = df['dormitorios'].fillna(0)
    transform_area(df,listas=['superficie_total','superficie_util','superficie_terraza'])
    transform_int_date(df,listas=['banos','ambientes','dormitorios','cant_max_habitantes','cantidad_pisos','departamentos_piso','numero_piso_unidad'])
    format_gps(df)
    df['orientacion'] = _categorical_format(df,'orientacion')
    df['region'] = df['comuna'].apply(_region_format_chile)
    df['comuna'] = df['comuna'].apply(_comuna_format_chile)
    _save_data(df, file_name, types='csv')

def _read_data(file_name, types='csv'):
    logger.info(f'Reading file {file_name}')
    if types =='csv':
        return pd.read_csv(file_name) # como lo vimos en el jupyter notebooks, leemos el archivo csv
    elif types =='sql':
        conn = connect('apartamento.db')
        #pd.read_sql_query(f'DROP TABLE clean_{file_name} IF EXISTS', conn)
        return pd.read_sql(f'''SELECT * FROM {file_name}''', conn)

def _remove_duplicate_entries(df, column_name):
    logger.info('Removing duplicate entries')
    df.drop_duplicates(subset=[column_name], keep='first', inplace=True)

    return df



def format_gps(df):

    df['latitude'] = df['latitude'].astype('float')
    df['longitude'] = df['longitude'].astype('float')


def _drop_rows_with_missing_values(df):
    logger.info('Dropping rows with missing data')

    return df.dropna()

def clean_currency(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace('$', '').replace('.', '').replace('Normal:','').replace(',',''))
    return(x)

def transform_area(df,listas):
    for lista in listas:
        df[lista] = df[lista].apply(clean_area)
        df[lista] = df[lista].astype(float)

        #df[lista].fillna(0)
def transform_int_date(df,listas):
    for lista in listas:

        if isinstance(lista, str):
            #print('-->',df[lista])
            df[lista].fillna(value=np.nan, inplace=True)
            df[lista] = df[lista].replace(np.nan, 0)
            df[lista] = df[lista].astype(float).astype('int32')


def clean_area(x):
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):

        result = (x.replace('útiles', '').replace('m²', '')).strip()
        return _extraer_number(result)
    return(0)

def _to_lower(df):
    #df.select_dtypes(include=['object','str'])
    #df.str.lower()
    df = df.applymap(lambda s:s.lower() if type(s) == str else s)
    return df

def _extraer_number(string):
    return ''.join(re.findall('[0-9]+', string))


def _price_format(df,tag):
    df[tag].fillna(value=np.nan, inplace=True)
    df[tag] = df[tag].replace(np.nan, '0')
    df[tag] = df[tag].apply(_extraer_number)

    df[tag] = df[tag].astype('float')
    return df[tag]

def _extraer_text(string):
    	return ''.join(re.findall('[A-Za-z]', string))

def _categorical_format(df,tag):
    df[tag].fillna(value=np.nan, inplace=True)
    df[tag] = df[tag].replace(np.nan, 'null')
    if tag == 'orientacion':
       df[tag] = df[tag].replace('s', 'sur').replace('n','norte').replace('o','oeste').replace('poniente','oeste').replace('p','oeste')
       df[tag] = df[tag].replace('surponiente','sur-oeste').replace('oriente','este').replace('suroriente','sur-este').replace('sur-oriente','sur-este')
       df[tag] = df[tag].replace('nor-oriente','norte-este').replace('so','sur-oeste').replace('nor-poniente','norte-oeste')
       return df[tag]

def _to_datetime(df,name):
    df[name] = pd.to_datetime(df[name])
    return df
def _published_datetime_format(published_time):
    fecha = datetime.datetime.now()
    if published_time !='None':
        if 'meses' in published_time:
            value = _extraer_number(published_time)
            return fecha - relativedelta(months=+int(value))
        
        if 'días' in published_time:
            value = _extraer_number(published_time)
            return fecha - datetime.timedelta(days=int(value))
    
    return fecha

def _region_format_chile(region):
    if region:
        value = region.split('|')[0].capitalize()   
    else:
         value = 'None'
    return value

def _comuna_format_chile(region):
    if region:
        value = region.split('|')[1].capitalize()   
    else:
         value = 'None'
    return value
def _save_data(df, file_name, types='csv'):

    clean_file_name = f'clean_{file_name}'
    logger.info(f'Saving file at: {clean_file_name}')
    if types == 'csv':
        df.to_csv(f'clean_data/{clean_file_name}.csv')
    elif types == 'sql':
        conn = connect('apartamento.db')
        df.to_sql(clean_file_name,conn)


    
