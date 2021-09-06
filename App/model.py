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

    catalog["artworks"] = lt.newList("SINGLE_LINKED", 
                                    cmpfunction=compareDates)
    catalog["artists"] = lt.newList("SINGLE_LINKED", 
                                    cmpfunction=compareCID)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)
    
def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

# Funciones para creacion de datos

# Funciones de consulta

def getArtworkbydate(catalog, date):
    """
    Retorna una obra por su fecha de adquisición.
    """
    artworks = catalog["artworks"]
    pos = lt.isPresent(artworks, date)
    if pos > 0:
        artwork = lt.getElement(artworks, pos)
        return artwork
    return None

def countPurchase(artworks):
    """
    Cuenta la cantidad de obras que fueron adquiridas por compra.
    """
    size = lt.size(artworks)
    count_p = 0
    if size:
        for artwork in lt.iterator(artworks):
            if "purchase" in artwork["CreditLine"].lower():
                count_p +=1    
    return count_p

# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date_1, artwork):
    if (date_1 in artwork["DateAcquired"]):
        return 0
    return -1

def compareCID(cID, artist):
    if cID in artist["ConstituentID"]:
        return 0
    return -1

# Funciones de ordenamiento

def organizeArtworkbyDate(catalog, startDate, finishDate):
    """
    Organiza y retorna las obras que esten en un rango de 
    una fecha inicial y final.
    """
    org = lt.newList()
    d_0 = date.fromisoformat(startDate)
    d_f = date.fromisoformat(finishDate)
    delta = d_f - d_0
    for day in range(delta.days + 1):
        new_day = d_0 + timedelta(days=day)
        new_date = new_day.strftime("%Y-%m-%d")
        art = getArtworkbydate(catalog, new_date)
        if art is not None:
            lt.addLast(org, art)
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

    