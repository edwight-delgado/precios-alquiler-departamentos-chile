import sqlite3
from sqlite3 import Error


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
DB_FILE = "productos.sqlite3"

#engine = create_engine(f"sqlite:///{DB_PATH}{DB_FILE}")
engine = create_engine(f"sqlite:///apartamento.db")
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Mysqlite:
    def __init__(self,db_file,table_name) -> None:
        self.db_file = db_file
        self.table_name = table_name

    def create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            self.conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

        


    def create_table(self):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return id
        """

        create_table_sql = f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                                        id integer PRIMARY KEY,
                                        link text NOT NULL,
                                        titulo text NULL,
                                        precio text NULL,
                                        direction text NULL,
                                        superficie_total text NULL,
                                        superficie_util text NULL,
                                        superficie_terraza text NULL,
                                        ambientes text NULL,
                                        dormitorios text NULL,
                                        banos text NULL,
                                        estacionamientos text NULL,
                                        cant_max_habitantes text NULL,
                                        bodegas text NULL,
                                        gastos_comunes text NULL,
                                        orientacion text NULL,
                                        tipo_departamento text NULL,
                                        cantidad_pisos text NULL,
                                        departamentos_piso text NULL,
                                        numero_piso_unidad text NULL,
                                        codigo text NULL,
                                        fecha text NULL,
                                        published_time text NULL,
                                        latitude text NULL,
                                        longitude ttext NULL,
                                        comuna text NULL
                                    ); """
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def insert_data(self,project):
        sql = f""" INSERT INTO {self.table_name} (
            link, 
            titulo, 
            precio, 
            direction,
            superficie_util,
            fecha                             
            ) VALUES(?,?,?,?,?,?) """

        cur = self.conn.cursor()
        cur.execute(sql, project)
        self.conn.commit()
        cur.close()
        return cur.lastrowid

    def insert_values(self,project):
        sql = """ INSERT INTO apartamentos (
            link, 
            titulo, 
            precio, 
            direction, 
            map, 
            superficie_total, 
            superficie_util, 
            superficie_terraza,
            ambientes, 
            dormitorios, 
            banos, 
            estacionamientos, 
            cant_max_habitantes, 
            bodegas,
            gastos_comunes, 
            orientación, 
            tipo_departamento,
            cantidad_pisos, 
            departamentos_piso, 
            numero_piso_unidad,
            codigo
                                       
            ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

        cur = self.conn.cursor()
        cur.execute(sql, project)
        self.conn.commit()
        cur.close()
        return cur.lastrowid

    def update_apartamentos(self, task):
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = ''' UPDATE apartamentos2
                SET titulo = ? ,
                    precio = ? ,
                    direction = ? ,
                    map = ?,
                    superficie_total = ? ,
                    superficie_util = ? ,
                    superficie_terraza = ?,
                    ambientes = ?,
                    dormitorios = ?,
                    banos = ?,
                    estacionamientos = ?,
                    cant_max_habitantes = ?,
                    bodegas = ?,
                    gastos_comunes = ?,
                    orientación = ?,
                    tipo_departamento = ?,
                    cantidad_pisos = ?,
                    departamentos_piso = ?,
                    numero_piso_unidad = ?,
                WHERE code = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        cur.close()

    def update_apartamentos(self, task):
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = ''' UPDATE apartamentos2
                SET 
                    direction = ? ,
                    
                WHERE code = ?'''
        cur = self.conn.cursor()
        cur.execute(sql, task)
        self.conn.commit()
        cur.close()

    def select_links(self):
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = f'''SELECT link FROM {self.table_name}'''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        #cur.close()
        return cur.fetchall()

    def select_apartamentos(self):
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = ''' SELECT * FROM apartamentos2'''
        cur = self.conn.cursor()
        cur.execute(sql)
        self.conn.commit()
        #cur.close()
        return cur.fetchall()

    def select_data(self,code):
        """
        update priority, begin_date, and end date of a task
        :param conn:
        :param task:
        :return: project id
        """
        sql = ''' SELECT * FROM apartamentos2 WHERE codigo = ?'''
        cur = self.conn.cursor()
        cur.execute(sql,(code,))
        self.conn.commit()
        #cur.close()
        return cur.fetchall()

        
def main():
    database = r"./pythonsqlite.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS apartamentos2 (
                                        id integer PRIMARY KEY,
                                        link text NOT NULL,
                                        titulo text NULL,
                                        precio text NULL,
                                        direction text NULL,
                                        map = text NULL,
                                        superficie_total = text NULL,
                                        superficie_util = text NULL,
                                        superficie_terraza = text NULL,
                                        ambientes = text NULL,
                                        dormitorios = text NULL,
                                        banos = text NULL,
                                        estacionamientos = text NULL,
                                        cant_max_habitantes = text NULL,
                                        bodegas = text NULL,
                                        gastos_comunes = text NULL,
                                        orientación = text NULL,
                                        tipo_departamento = text NULL,
                                        cantidad_pisos = text NULL,
                                        departamentos_piso = text NULL,
                                        numero_piso_unidad = text NULL,
                                        begin_date text,
                                        end_date text
                                    ); """

    sql_create_apartamentos_table = """CREATE TABLE IF NOT EXISTS apartamentos (
                                    id integer PRIMARY KEY,
                                    link text NOT NULL,
                                    precio text NOT NULL,
                                    ubicacion text NULL,
                                    banos text NULL,
                                    superficie text NULL
                                    
                                );"""

    # create a database connection
    conn = Mysqlite()
    conn.create_connection(database)


    # create tables
    if conn is not None:
        # create projects table
        conn.create_table(sql_create_projects_table)

        # create tasks table
        #conn.create_table(conn, sql_create_apartamentos_table)

        #project = ('link', 'precio', 'ubicacion','bano','superficie');
        #project_id = conn.create_project(project)
    else:
        print("Error! cannot create the database connection.")



if __name__ == '__main__':
    main()