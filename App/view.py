"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller 
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Listar crónologicamente los artistas")
    print("3- Listar crónologicamente las adquisiciones")
    print("4- Clasificar las obras de los artistas por tecnica")
    print("5- Clasificar las obras por la nacionalidad de sus creadores")
    print("0- Salir")

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)

catalog = None

def printArtworkData(catalog, artworks):
    size = lt.size(artworks)
    if size:
        for artwork in lt.iterator(artworks):
            artists = controller.getArtistsofArtwork(catalog, artwork["ConstituentID"])
            print ("Título: " + artwork["Title"] + " Artista(s): " + artists + "Fecha de Adquisición:  " 
                    + artwork["DateAcquired"] + " Medio: " + artwork["Medium"] + " Dimensiones: " + artwork["Dimensions"])
    else:
        print ("No se encontraron obras")

def printArtistData(artists):
    size = lt.size(artists)
    if size:
        for artist in lt.iterator(artists):
            print ("Nombre: " + artist["DisplayName"] + " Contituent ID:  " 
                    + artist["ConstituentID"])
    else:
        print ("No se encontraron artistas")

def artworksBydate(catalog, startDate, finishDate):
    """
    Genera una lista cronológicamente ordenada de las obras adquiridas 
    por el museo en un rango de fecha. Retorna el total de obras en el rango cronológico, 
    total de obras adquiridas por compra y las primeras 3 y utimas 3 obras del rango.
    """
    org_dates = controller.organizeBooksbyDate(catalog, startDate, finishDate)
    last = controller.lastThree(org_dates)
    first = controller.firstThree(org_dates)
    print("\n")
    print("Total de obras en el rango " + str(startDate) + " - " + str(finishDate) + ": " + str(lt.size(org_dates))) 
    print("-" * 50)
    print("Total de obras compradas en el rango: " + str(controller.countPurchase(org_dates)))
    print("-" * 50)
    print ("  Estos son las 3 primeras Obras encontrados: ")
    printArtworkData(catalog, first)
    print("-" * 50)
    print ("  Estos son las 3 ultimas Obras encontrados: ")
    printArtworkData(catalog, last)
    print("-" * 50)

def topArtworksbyNationality(top):
    """
    """
    keys = list(top.keys())
    top_nations = ""
    count = 0
    for x in range(0,10):
        count += 1
        top_nations += str(count) + ". " + str(keys[x]) + ": " + str(top[str(keys[x])]) + " "
    print("Top Nacionalidades con más obras obras: ")
    print (top_nations[:-1])
    print("-" * 50)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        print('Obras cargados: ' + str(lt.size(catalog['artworks'])))
        print('Artistas cargados: ' + str(lt.size(catalog['artists'])))
        print("Ultimos 3 elementos de Artistas: ")
        printArtistData(controller.lastThree(catalog["artists"]))
        print("Ultimos 3 elementos de Obras: ")
        printArtworkData(catalog, controller.lastThree(catalog["artworks"]))
        
    elif int(inputs[0]) == 3:
        startDate = input("Fecha de Inicio (YYYY-MM-DD): ")
        finishDate = input("Fecha Final (YYYY-MM-DD): ")
        artworksBydate(catalog, startDate, finishDate) 
    
    elif int(inputs[0]) == 5:
        top = (controller.organizeTopNationaliy(catalog))
        topArtworksbyNationality(top)
        first = str(list(top.keys())[0])
        artworks = controller.getArtworkbyNationality(catalog, first)
        printArtworkData(catalog, controller.firstThree(artworks))
        print("-"*50)
        printArtworkData(catalog, controller.lastThree(artworks))
    else:
        sys.exit(0)
sys.exit(0)
