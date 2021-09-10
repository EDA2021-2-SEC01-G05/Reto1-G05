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


from App.controller import artworksbyartist
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

    catalog["artworks"] = lt.newList("SINGLE_LINKED")
    catalog["artists"] = lt.newList("SINGLE_LINKED", cmpfunction=compareAnio)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)

def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

# Funciones para creacion de dato

def getElementbyparameter(lista, parameter):
    """
    Retorna un elemento de una lista dado un parametro, luego, lo elimina de la lista
    """
    pos = lt.isPresent(lista, parameter)
    if pos > 0:
        element = lt.getElement(lista, pos)
        lt.deleteElement(lista, pos)
        return element
    else:
        return None

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareCID(CID, artwork):
    if (CID in artwork["ConstituentID"]):
        return 0
    return -1

def compareMedium(medium, artwork):
    if (medium in artwork["Medium"]):
        return 0
    return -1

def compareAnio(anio, artist):
    if anio in artist["BeginDate"]:
        return 0
    return -1

def compareNames(nombre,artist):
    if nombre in artist["DisplayName"]:
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
        artist = getElementbyparameter(lista,str(anio))
        if artist is not None:
            lt.addLast(org,artist)
        else:
            anio = int(anio) + 1
    return org

def artworksbyArtist(catalog,nombre):
    """
    Retorna una lt con las obras de un artista por su nombre con funcion de comparacion por el medio o tecnica.
    """
    # crear nueva lista de artistas a partir de catalog['artists'] para comparar por nombres
    artistas = lt.newList("SINGLE_LINKED",cmpfunction=compareNames)
    artists = catalog["artists"]
    for artist in lt.iterator(artists):
        lt.addLast(artistas,artist)
    # sacar la identidad del artista dado por el nombre
    artista = getElementbyparameter(artistas,nombre)
    ident = artista["ConstituentID"]
    # crear nueva lista de obras a partir de catalog['artworks'] para comparar por ID 
    obras1 = lt.newList("SINGLE_LINKED",cmpfunction=compareCID)
    artworks = catalog["artworks"]
    for artwork in lt.iterator(artworks):
        lt.addLast(obras1,artwork)
    # Crear lista de obras del artista con comparacion por medios o tecnica
    obras = lt.newList("SINGLE_LINKED",cmpfunction=compareMedium)
    i = 0
    while i <= 0:
        obra = getElementbyparameter(obras1,ident)
        if obra is not None:
            lt.addLast(obras,obra)
        else:
            i+=1
    return obras

def artworksbyMedium(obras):
    """
    Retorna una lista con tres elementos:
    Un lt de obras con la tecnica mas usada de obras en general.
    El total de tecnicas o medios que se usaron en obras.
    Y la tecnica mas recurrente que se usa en obras.
    """
     # Crear conjunto y luego lista con los medios o tecnicas que usan las obras
    medios_c = set()
    medios = []
    for obra in lt.iterator(obras):
        medios_c.add(obra['Medium'])
    for med in medios_c:
        medios.append(med)
    # Contar la cantidad de veces que se usa un medio particular en las obras
    contar = []
    j = 0
    while j < len(medios):
        q = 0
        for obra in lt.iterator(obras):
            if (obra['Medium']==str(medios[j])):
                q += 1
        contar.append(q)
        j += 1
    # Sacar la tecnica mas usada
    mas_uso = max(contar)
    indice = contar.index(mas_uso)
    tecnica = medios[indice]
    # hacer una lt con las obras que usa la tecnica mas recurrente
    obras_tecnica = lt.newList()
    k = 0
    while k <= 0:
        o = getElementbyparameter(obras,tecnica)
        if o is not None:
            lt.addLast(obras_tecnica,o)
        else:
            k += 1
    return [obras_tecnica,len(medios),tecnica]
        
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