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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


from DISClib.DataStructures.arraylist import newList
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
from datetime import date, timedelta

"""
Se define la estructura de un catálogo de obras en el museo. 
El catálogo tendrá dos listas, una para los obras del museo, 
otra para los artistas.
"""

# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de obras. Crea una lista vacia para guardar
    todos las obras, adicionalmente, crea una lista vacia para los artistas.
    Retorna el catalogo inicializado.
    """
    catalog = {"artworks": None,
                "artists": None}

    catalog["artworks"] = lt.newList("SINGLE_LINKED",cmpfunction=compareDates)
    catalog["artists"] = lt.newList("SINGLE_LINKED", cmpfunction=compareAnio)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)

def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

# Funciones para creacion de dato

def getArtistbyanio(artists, anio):
    """
    Retorna un artista por su fecha de nacimiento, luego, lo elimina de la lista
    """
    pos = lt.isPresent(artists, anio)
    if pos > 0:
        artist = lt.getElement(artists, pos)
        lt.deleteElement(artists, pos)
        return artist
    else:
        return None

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date_1, artwork):
    if (date_1 in artwork["DateAcquired"]):
        return 0
    return -1

def compareAnio(anio, artist):
    if anio in artist["BeginDate"]:
        return 0
    return -1

# Funciones de ordenamiento

def organizeArtistsbyanio(catalog,anio_inicial,anio_final):
    """
    Organiza y retorna los artistas que esten en un rango de una fecha inicial y final.
    """
    # crear copia de la lista artistas para iterar sobre esta y no modificar el catalogo original
    artistas = catalog["artists"]
    primerart = lt.firstElement(artistas)
    parametro = primerart["BeginDate"]
    pos = lt.isPresent(artistas,parametro) 
    longitud = lt.size(artistas)
    lista = lt.subList(artistas,pos,longitud)
    # crear y llenar una nueva lista ordenada de artistas por anio_inicial y anio_final
    org = lt.newList()
    anio = int(anio_inicial)
    while anio <= int(anio_final):
        artist = getArtistbyanio(lista,str(anio))
        if artist is not None:
            lt.addLast(org,artist)
        else:
            anio = int(anio) + 1
    return org

def firstThree(catalog):
    """
    Retorna una lista con los tres primeros elemento de un catalogo.
    """
    first = lt.newList()
    for x in range(1,4):
        e = lt.getElement(catalog, x)
        lt.addLast(first, e)
    return first
    
def lastThree(catalog):
    """
    Retorna una lista con los 3 ultimos elementos del catalogo escogido.
    """
    last = lt.newList()
    for x in range(0,3):
        pos = int(lt.size(catalog)) - x
        i = (lt.getElement(catalog, pos))
        lt.addFirst(last, i)
    return last