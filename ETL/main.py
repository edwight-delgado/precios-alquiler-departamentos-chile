# -*- coding: utf-8 -*-
"""

This is a script file developed by edwight
github.com/edwight-delgado

"""
from scrapper import HomePage, DetailPage
from pathlib import Path
from transform_data import transform
import datetime
import argparse
_URL = 'portalinmobiliario'
path = Path('./apartamento.db')

def main(_URL, parser):
    fecha = datetime.datetime.now().strftime("%m_%d_%Y")
    
    if parser == '1':
        main_page = HomePage(_URL,fecha_table=fecha)
        main_page.get_link()

    #if path.is_file() == False:
    #    main_page = HomePage(_URL)
    #    fecha = main_page.get_link()

    if parser == '2':
        detail_page = DetailPage(_URL,fecha_table=fecha)
        detail_page.update()

    if parser == '3':
        transform(fecha_table=fecha)

    else:
        exit()

if __name__ == "__main__":

    MENU ="""
    1 - hacer scrapping a portalinmobiliario
    2 - hacer full scrapping a portalinmobiliario
    3 - transformar datos 
    q - salir
    """
    print(MENU)
    parser = input('selecione una opción:')

    main(_URL, parser)