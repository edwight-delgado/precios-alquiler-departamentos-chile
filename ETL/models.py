import database as db

from sqlalchemy import Column, Integer, String, Float


class Producto(db.Base):
    __tablename__ = 'apartamentos2'

    id = Column(Integer, primary_key=True)
    titulo = Column(String, nullable=True)

    precio = Column(Float, nullable=True)
    #precio = Column(String, nullable=True)
    codigo = Column(String, nullable=True)
    superficie_total = Column(String, nullable=True)
    superficie_util = Column(String, nullable=True)
    superficie_terraza = Column(String, nullable=True)
    ambientes = Column(String, nullable=True)
    dormitorios = Column(String, nullable=True)
    banos = Column(String, nullable=True)
    cant_max_habitantes = Column(String, nullable=True)
    gastos_comunes = Column(String, nullable=True)
    cantidad_pisos = Column(String, nullable=True)
    departamentos_piso = Column(String, nullable=True)
    numero_piso_unidad = Column(String, nullable=True)

    link = Column(String, nullable=False)

    def __init__(self, link, titulo, precio, codigo,superficie_total, superficie_util,superficie_terraza,ambientes,dormitorios,banos,cant_max_habitantes):
        self.titulo = titulo
        self.precio = precio
        self.codigo = codigo
        self.link = link
        self.superficie_total = superficie_total
        self.superficie_util = superficie_util
        self.superficie_terraza = superficie_terraza
        self.ambientes = ambientes
        self.dormitorios= dormitorios
        self.banos = banos
        self.cant_max_habitantes=cant_max_habitantes
        #self.resp = f'({self.titulo}, {self.precio},{self.codigo},{self.superficie_total},{self.superficie_util},{self.superficie_terraza},{self.ambientes},{self.dormitorios},{self.banos},{self.cant_max_habitantes})'

    def __repr__(self):

        return f'({self.titulo}, {self.precio},{self.codigo},{self.superficie_total},{self.superficie_util},{self.superficie_terraza},{self.ambientes},{self.dormitorios},{self.banos},{self.cant_max_habitantes})'

    def __str__(self):
        return f'({self.titulo}, {self.precio},{self.codigo},{self.superficie_total},{self.superficie_util},{self.superficie_terraza},{self.ambientes},{self.dormitorios},{self.banos},{self.cant_max_habitantes})'