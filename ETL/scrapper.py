from log import Log
from common import config
import requests, urllib3
from bs4 import BeautifulSoup
from time import sleep
import datetime
#from database import *
from db import Mysqlite
from db import *
import gc
import re

DATABASE = r"./apartamento.db"




log = Log()
# create tables

http = urllib3.PoolManager(maxsize=15,num_pools=50)
#HTTPConnectionPool and HTTPSConnectionPool. T
fecha = datetime.datetime.now()
fecha_table = fecha.strftime("%m_%d_%Y")
fecha_colum = fecha.strftime("%m-%d-%Y")

class BasePage:
    """clase pricipal (superClase) """
    def __init__(self, items_site_uid,fecha_table) -> None:
        self.site_name = items_site_uid
        self._config = config()['inmobiliario_sites'][items_site_uid]
        self._queries = self._config['queries']
        self.url = self._config['base_url']


        self.connection = connection
        self._table_name = f'alquiler_{fecha_table}'
        self.conn = Mysqlite(DATABASE,table_name=self._table_name)
        self.conn.create_connection()
        if self.conn is not None:
        #    # creacion de tabla si no existe
            self.conn.create_table()
            log.get_log(level='info', msg='creacion de tabla')

        self.name ={
            'Superficie total':0,
            'Superficie útil':0,
            'Superficie de terraza':0,
            'Ambientes':0,
            'Dormitorios':0,
            'Baños':0,
            'Estacionamientos':0,
            'Cantidad máxima de habitantes':0,
            'Bodegas':0,
            'Número de piso de la unidad':0,
            'Gastos comunes':0,
            'Orientacion':0,
            'Tipo de departamento':0,
            'Cantidad de pisos':0,
            'Departamentos por piso':0,
            
        }
        self.column_name = [
                    'superficie_total',
                    'superficie_util', 
                    'superficie_terraza', 
                    'ambientes', 
                    'dormitorios', 
                    'banos', 
                    'estacionamientos', 
                    'cant_max_habitantes', 
                    'bodegas', 
                    'numero_piso_unidad', 
                    'gastos_comunes', 
                    'orientacion', 
                    'tipo_departamento', 
                    'cantidad_pisos', 
                    'departamentos_piso' 
                ]
        
    def request(self, sub_url=None):
        if sub_url == None:
            return requests.get(self.url, allow_redirects=False)
        else:
            return requests.get(f'{self.url}/{sub_url}', allow_redirects=False)

    def get_queries(self,name,level):
        if level=='name':
            title = self._queries[name][0]
            return title
        if level =='tag':
            tag = self._queries[name][1]
            return tag
    
    def formatted(self,item, value:str,array=False):
        try:
            if array:
                return item.find_all(self.get_queries(value,'tag'), class_=self.get_queries(value,'name'))
            
            else:
                return item.find(self.get_queries(value,'tag'), class_=self.get_queries(value,'name')).text
        except:
            log.get_log(level='warning',msg=f'values {value} no found')
            return None

class HomePage(BasePage):
    def __init__(self, items_site_uid,fecha_table) -> None:
            super().__init__(items_site_uid,fecha_table)

    def save_data(self, data):
        item_id = self.conn.insert_data(data)
        log.get_log(level='info',msg=f'item data Success!!! id {item_id}')

    def get_link(self):
        limit_page = 40
        for i in range(0,limit_page):
            sleep(.075)
            if i < 1:
                r = self.request(sub_url='arriendo/departamento')
            else: 
                num = (50 * i) + 1
                r = self.request(sub_url=f'arriendo/departamento/_Desde_{num}_NoIndex_True')
                status = r.status_code
                if status !=200:
                    log.get_log(level="error",msg="Connection Error with code:{status}")
                else: 

                    log.get_log(level="info",msg=f"request with status code 200. Extraing url of page ({i}/{limit_page})")
                    #print(r)
                    soup = BeautifulSoup(r.text, 'lxml')

                    items = soup.find_all(self.get_queries('items','tag'), class_=self.get_queries('items','name'))
                    for item in items:
                        
                        link = item.find(self.get_queries('link','tag'), class_=self.get_queries('link','name'))['href']
                        price =  self.formatted(item, value='price')
                        direction = self.formatted(item, value='direction')
                        titulo = self.formatted(item, value='title', array=True)[1].text
                        
                        superficie_util = self.formatted(item, value='area', array=True)[0].text

                        data = (link ,titulo ,price, direction, superficie_util,fecha_colum)
                        
                        self.save_data(data)

        
        
class DetailPage(BasePage):

    def __init__(self, items_site_uid, fecha_table) -> None:
        super().__init__(items_site_uid,fecha_table)
        log.get_log(level='info', msg='Start Scrapping to DetailPage')

    def query(self, enlaces:str, name:str) -> str:
        """ extrae las Características de la Propiedad """

        for enlace in enlaces:
            sleep(.075)
            value = enlace.find('th').text
            
            if value == name:
                # print(enlace.find('th').text)
                try:
                    result = enlace.find('td').text
                    
                except:
                    result = '0'
                #print(name, result)
                return result

    def lat_and_long(self,soup):
        script_tag = soup.find_all("script")
        tag = script_tag[-1]
        if tag:
            script_tag_contents = tag.string


        latitude_match = re.search('"latitude":"(-?\d+\.\d+)"', script_tag_contents)
        longitude_match = re.search('"longitude":"(-?\d+\.\d+)"', script_tag_contents)
        latitude = None
        longitude = None
        if latitude_match and longitude_match:
            latitude = float(latitude_match.group(1))
            longitude = float(longitude_match.group(1))
        
        else:
            log.get_log(level="warning",msg="No se pueden extraer los valores de latitud y longitud.")

        return latitude, longitude

    def scrapper(self):
        
        links = self.conn.select_links()

        for link in links:
            link = ''.join(link)
            
            data = {}
            shortlink = link.replace(self.url+'/','')
            r = self.request(sub_url=shortlink)
            status = r.status_code
            if status == 200:
                soup = BeautifulSoup(r.text, 'lxml')
                tabla = self.formatted(soup,'tabla', array=True)
                for key, key2 in zip(self.name.keys(), self.column_name):
                    data[key2] = self.query(tabla, key)                    

                
                
                data['codigo'] = self.formatted(soup,'code')
                data['link'] = link
                data['gastos_comunes'] = self.formatted(soup,'gastos_comunes')
                data['published_time'] = self.formatted(soup,'published_time')
                comuna = self.formatted(soup, value='comuna', array=True)[3].text
                comuna2 = self.formatted(soup, value='comuna', array=True)[4].text
                data['comuna'] = f'{comuna}|{comuna2}'
                #print('comuna')
                #print(data['comuna'])
                lat, longi = self.lat_and_long(soup)

                data['latitude'] = lat
                data['longitude'] = longi

                

                yield data
                gc.collect()
                # return data
                # yield data
            r.close()
    
    def save(self, res, data, link, name, num):
        """
            metodo que actualiza la tabla (res) 
            si la celda (res[num]) esta vacia y el dato (data[name]) tiene un valor se actualiza la cerda donde el link es igual 
            a el argumento link 
        """
        if res[num] == None and data[name] != None:
            _value = data[name]
            update = f'UPDATE {self._table_name} SET {name}="{_value}" WHERE link = ?'
            ids = self.connection.execute(update, (link,))
            log.get_log(level='info', msg=f'{name} updated')


    def update(self):

        for data in self.scrapper():

            link = data['link']
            query = f"""SELECT * FROM {self._table_name} WHERE link == ? LIMIT 1;"""
            results = self.connection.execute(query, (link,))
            #row = results.fetchone()
            #name_columns = row.keys()
            
            
            # print(results)
            for res in results:
                log.get_log(level='info',msg=f'database id: {res[0]}')
                #self.save(res, data, link, 'map', 5)
                self.save(res, data, link, 'superficie_total', 5)
                self.save(res, data, link, 'superficie_util', 6)
                self.save(res, data, link, 'superficie_terraza', 7)
                self.save(res, data, link, 'ambientes', 8)
                self.save(res, data, link, 'dormitorios', 9)
                self.save(res, data, link, 'banos', 10)
                self.save(res, data, link, 'estacionamientos', 11)
                self.save(res, data, link, 'cant_max_habitantes', 12)
                self.save(res, data, link, 'bodegas', 13)
                self.save(res, data, link, 'gastos_comunes', 14)
                self.save(res, data, link, 'orientacion', 15)
                self.save(res, data, link, 'tipo_departamento', 16)
                self.save(res, data, link, 'cantidad_pisos', 17)
                self.save(res, data, link, 'departamentos_piso', 18)
                self.save(res, data, link, 'numero_piso_unidad', 19)
                self.save(res, data, link, 'codigo', 20)
                self.save(res, data, link, 'published_time', 22)
                self.save(res, data, link, 'latitude', 23)
                self.save(res, data, link, 'longitude', 24)
                self.save(res, data, link, 'comuna', 25)
                                
        self.connection.close()

def main():
    h = DetailPage('portalinmobiliario')
    h.update()

if __name__=='__main__':
    main()

