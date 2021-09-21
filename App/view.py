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
    print("6- Calcular costo de transportar las obras de un departamento")
    print("0-  Salir")

def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()


def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    return controller.loadData(catalog)

catalog = None

def printArtistData_Req1(artists):
    size = lt.size(artists)
    if size>0:
        for artist in lt.iterator(artists):
            print ("Nombre: " + artist["DisplayName"] + ", Año nacimiento:  " 
                    + artist["BeginDate"] + ", Año fallecimiento: " + artist["EndDate"]
                    + ", Nacionalidad: " + artist["Nationality"] + ", Género: " + artist["Gender"])
    else:
        print ("No se encontraron artistas")

def printArtworkData_Req3(artworks):
    size = lt.size(artworks)
    if size>0:
        for artwork in lt.iterator(artworks):
            print ("ID: " + artwork["ObjectID"] + ", Título: " + artwork["Title"] 
                    + ", Fecha:  " + artwork["Date"] + ", Medio: " 
                    + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"])
    else:
        print ("No se encontraron artistas")

def printArtworkData_Req5(artworks):
    size = lt.size(artworks)
    if size>0:
        for artwork in lt.iterator(artworks):
            print ("ID: " + artwork["ObjectID"] + ", Título: " + artwork["Title"] 
                    + ", ID artistas: " + artwork['ConstituentID'] + ", Clasificacion: " 
                    + artwork['Classification'] + ", Fecha:  " + artwork["Date"] + ", Medio: " 
                    + artwork["Medium"] + ", Dimensiones: " + artwork["Dimensions"] 
                    + ", Costo de transporte (USD): " + str(int(artwork['Transcost (USD)'])))
    else:
        print ("No se encontraron artistas")

def requerimiento1(catalog, anio_inicial, anio_final):
    """
    Genera una lista cronológicamente ordenada de los artistas en un rango de anios.
    Retorna el total de artistas en el rango cronológico, y los primeros 3 y ultimos 3 artistas del rango.
    """
    org_anio = controller.artistsbyAnio(catalog, anio_inicial, anio_final)
    print("\n")
    print("Total de artistas en el rango " + str(anio_inicial) + " - " + str(anio_final) + ": " + str(lt.size(org_anio)))
    print("-" * 50)
    last = controller.lastThreeD(org_anio)
    first = controller.firstThreeD(org_anio)
    print ("  Estos son los 3 primeros Artistas encontrados: ")
    printArtistData_Req1(first)
    print("-" * 50)
    print ("  Estos son los 3 ultimos Artistas encontrados: ")
    printArtistData_Req1(last)
    print("-" * 50)

def requerimiento3(catalog,nombre):
    artworks = controller.artworksbyArtist(catalog,nombre)
    print("\n")
    print("Total de obras del artista " + str(nombre) + ": " + str(lt.size(artworks)))
    lista = controller.artworksbyMedium(artworks)
    medios = controller.contarMedios(artworks)
    medio_max = controller.medioMax(lista)
    print("-" * 50)
    print("Total de medios usados por el artista en sus obras: " + str(medios))
    print("-" * 50)
    print("La técnica más usada por el artista es: " + str(medio_max))
    print("-" * 50)
    print("Listado de obras con la técnica más usada: ")
    printArtworkData_Req3(lista)

def requerimiento5(catalog,department):
    obras = controller.artworksbyDepartment(catalog,department)
    total = controller.costoTotal(obras)
    peso = controller.pesoTotal(obras)
    antiguas = controller.masAntiguas(obras)
    costosas = controller.masCostosas(obras)
    print('Total de obras para transportar: ' + str(lt.size(obras)))
    print("-" * 50)
    print('Costo total estimado de transportar las obras (USD): ' + str(total))
    print("-" * 50)
    print('Peso total estimado de las obras (kg): ' + str(peso))
    print("-" * 50)
    print('Las 5 obras más antiguas a transportar son: ')
    print("-" * 50)
    printArtworkData_Req5(antiguas)
    print("-" * 50)
    print('Las 5 obras más costosas a transportar son: ')
    print("-" * 50)
    printArtworkData_Req5(costosas)

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
        print(controller.firstThreeD(catalog["artists"]))
        print("Ultimos 3 elementos de Obras: ")
        print(controller.lastThreeD(catalog["artworks"]))

    elif int(inputs[0]) == 2:
        anio_inicial = input("Ingrese el año inicial: ")
        anio_final = input("Ingrese el año final: ")
        requerimiento1(catalog, anio_inicial, anio_final)

    elif int(inputs[0]) == 4:
        nombre = input("Ingrese el nombre del artista: ")
        requerimiento3(catalog,nombre)

    elif int(inputs[0]) == 6:
        department = input("Ingrese el nombre del departamento del museo: ")
        requerimiento5(catalog,department)

    else:
        sys.exit(0)
sys.exit(0)