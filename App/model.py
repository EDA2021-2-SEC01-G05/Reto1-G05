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

import config as cf
from DISClib.ADT import list as lt
assert cf
from DISClib.Algorithms.Sorting import mergesort as merge

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

    catalog["artworks"] = lt.newList("SINGLE_LINKED", cmpfunction=compareOID)
    catalog["artists"] = lt.newList("SINGLE_LINKED", cmpfunction=compareID)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)

def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

# Funciones para creacion de dato

def getElementbyparameterE(lista, parameter):
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

def getElementbyparameter(lista, parameter):
    """
    Retorna un elemento de una lista dado un parametro, no lo elimina de la lista
    """
    pos = lt.isPresent(lista, parameter)
    if pos > 0:
        element = lt.getElement(lista, pos)
        return element
    else:
        return None

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def mayorQue(a,b):
    if (a > b):
        return 0
    return -1

def compareID(ID, artist):
    if (ID in artist['ConstituentID']):
        return 0
    return -1

def compareOID(OID, artwork):
    if (OID in artwork['ObjectID']):
        return 0
    return -1

def compareCID(CID, artwork):
    x = str(CID)
    string1 = '[' + x + ']'
    string2 = ',' + x + ','
    if (string1 in artwork["ConstituentID"]):
        return 0
    elif (string2 in artwork["ConstituentID"]):
        return 0
    else:
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
    # crear lista artistas con funcion de comparacion compareAnio para iterar sobre esta y no modificar el catalogo original
    artistas = lt.newList('SINGLE_LINKED',cmpfunction=compareAnio)
    artists = catalog["artists"]
    for artist in lt.iterator(artists):
        lt.addLast(artistas,artist)
    # crear y llenar una nueva lista ordenada de artistas por anio_inicial y anio_final
    org = lt.newList()
    anio = int(anio_inicial)
    while anio <= int(anio_final):
        artista = getElementbyparameterE(artistas,str(anio))
        if artista is not None:
            lt.addLast(org,artista)
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
        obra = getElementbyparameterE(obras1,ident)
        if obra is not None:
            lt.addLast(obras,obra)
        else:
            i+=1
    return obras

def listaMedios(obras):
    """
    Retorna lista con representantes unicos para cada medio que se usa en una lista de obras 
    """
    first = lt.firstElement(obras)
    medios = lt.newList("SINGLE_LINKED",cmpfunction=compareMedium)
    lt.addFirst(medios,first)        
    for obra in lt.iterator(obras):
        i = 0
        for medio in lt.iterator(medios):
            if (str(obra['Medium']) == str(medio['Medium'])):
                i += 1
        if (i == 0):
            lt.addLast(medios,obra)
    return medios

def contarMedios(obras):
    """
    Cuenta la cantidad de medios que se usan en una lista de obras
    """
    medios = listaMedios(obras)
    num = lt.size(medios)
    return num
    
def artworksbyMedium(obras):
    """
    Retorna un lt con las obras que usan la tecnica o medio mas recurrente en obras.
    """
    # contamos numero de veces que aparece cada medio y agregamos este numero a una lista (numeros)
    medios = listaMedios(obras)
    numeros = lt.newList()
    for medio in lt.iterator(medios):
        i = 0
        for obra in lt.iterator(obras):
            if (medio['Medium'] == obra['Medium']):
                i += 1
        lt.addLast(numeros,i)
    # ordenamos la lista y sacamos el numero mas grande
    merge.sort(numeros,cmpfunction=mayorQue)
    num = lt.lastElement(numeros)
    # hallamos el medio (medio) correspondiente a este numero mas grande (num)
    for medio in lt.iterator(medios):
        i = 0
        for obra in lt.iterator(obras):
            if (medio['Medium'] == obra['Medium']):
                i += 1
        if i is num:
            break
    # hacemos una lista (lista) con las obras que usan el medio hallado (medio)
    lista = lt.newList()
    if medio is not None:
        for obra in lt.iterator(obras):
            if (obra['Medium'] ==  medio['Medium']):
                lt.addLast(lista,obra)
        return lista
        
def firstThree(lista):
    """
    Retorna una lista con los tres primeros elementos de una lista.
    """
    first = lt.subList(lista,1,3)
    return first
    
def lastThree(lista):
    """
    Retorna una lista con los 3 ultimos elementos de una lista.
    """
    last = lt.subList(lista,lt.size(lista)-2,3)
    return last
   