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

from DISClib.ADT.list import size
import config as cf
import model
import csv
from datetime import date
from DISClib.ADT import list as lt

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def initCatalog():
    """
    Llama la funcion de inicializacion del catalogo del modelo.
    """
    t = "SINGLE_LINKED"
    catalog = model.newCatalog(t)
    return catalog

# Funciones para la carga de datos

def loadData(catalog):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    loadArtists(catalog)
    loadArtworks(catalog)
    

def loadArtworks(catalog):
    """
    Carga las obras del archivo.
    """
    booksfile = cf.data_dir + 'MoMA/Artworks-utf8-10pct.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artwork in input_file:
        model.addArtwork(catalog, artwork)   

def loadArtists(catalog):
    """
    Carga los artistas.
    """
    booksfile = cf.data_dir + 'MoMA/Artists-utf8-10pct.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)

# Funciones de ordenamiento

def organizeTopNationaliy(catalog):
    """
    Llama a la función que devuelve el top cantidad de obras de la lista de nacionalidades.
    """
    return model.organizeTopNationaly(catalog)

def organizeBooksbyDate(catalog, startDate, finishDate, size, option):
    """
    Organiza las obras por fecha.
    """
    return model.organizeArtworkbyDate(catalog, startDate, finishDate, size, option)


# Funciones de consulta sobre el catálogo

def getArtistsofArtwork(catalog, codes):
    """
    Llama a la funcion que identifica al artista o artistas de un aobra.
    """
    return model.getArtistname(catalog,codes)

def countPurchase(artworks):
    """
    Llama a la función que cuenta cuantas obras fueron compradas en una lista dada.
    """
    return model.countPurchase(artworks)

def firstThree(catalog):
    """
    Devuelve los primeros 3 elementos dela catalogo de artistas y obras.
    """
    return model.firstThree(catalog)

def lastThree(catalog):
    """
    Devuelve los primeros 3 elementos dela catalogo de artistas y obras.
    """
    return model.lastThree(catalog)

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

def firstThreeD(catalog):
    """
    """
    return model.firstThreeD(catalog)

def lastThreeD(catalog):
    """
    """
    return model.lastThreeD(catalog)

def getArtworkbyNationality(catalog, name):
    """
    Ordena y consigue el top 10 de las nacionalidades con más obras.
    """
    return model.getArtworkbyNationality(catalog, name)
