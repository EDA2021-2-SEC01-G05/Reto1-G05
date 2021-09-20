"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import model
import csv
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    catalog = model.newCatalog()
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtworks(catalog)
    loadArtists(catalog)

def loadArtworks(catalog):
    """
    Carga las obras del archivo.  Por cada libro se toman sus artistas y por
    cada uno de ellos, se crea en la lista de artistas, a dicho artista y una
    referencia a la obra que se esta procesando.
    """
    booksfile = cf.data_dir + 'MoMA/Artworks-utf8-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)   

def loadArtists(catalog):
    """
    """
    booksfile = cf.data_dir + 'MoMA/Artists-utf8-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    
# Funciones de ordenamiento

def artistsbyAnio(catalog,anio_inicial,anio_final):
    """
    """
    return model.organizeArtistsbyanio(catalog,anio_inicial,anio_final)

def artworksbyArtist(catalog,nombre):
    """
    """
    return model.artworksbyArtist(catalog,nombre)

def medioMax(obras):
    """
    """
    medio = lt.firstElement(obras)
    return medio['Medium']

def contarMedios(obras):
    """
    """
    return model.contarMedios(obras)

def artworksbyMedium(obras):
    """
    """
    return model.artworksbyMedium(obras)

def artworksbyDepartment(catalog,department):
    """
    """
    return model.artworksbyDepartment(catalog,department)

def costoTransporte(obras):
    """
    """
    return model.costoTransporte(obras)

def costoTotal(obras):
    """
    """
    return model.costoTotal(obras)

def pesoTotal(obras):
    """
    """
    return model.pesoTotal(obras)

def masAntiguas(obras):
    """
    """
    return model.masAntiguas(obras)


def masCostosas(obras):
    """
    """
    return model.masCostosas(obras)

# Funciones de consulta sobre el catálogo

def firstThree(catalog):
    """
    """
    return model.firstThree(catalog)

def lastThree(catalog):
    """
    """
    return model.lastThree(catalog)