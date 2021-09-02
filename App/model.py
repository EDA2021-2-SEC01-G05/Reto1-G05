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

    catalog["artworks"] = lt.newList()
    catalog["artists"] = lt.newList("ARRAY_LIST")
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    lt.addLast(catalog["artworks"], artwork)

def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

# Funciones para creacion de dato

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def lastThreeArtist(catalog, name):
    """
    Retorna una lista con los 3 ultimos elementos del catalogo escogido.
    """
    last = []
    for x in range(0,3):
        pos = int(lt.size(catalog[name])) - x
        i = (lt.getElement(catalog[name], pos))
        last.append(i)
    return last
    