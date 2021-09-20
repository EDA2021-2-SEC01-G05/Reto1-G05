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
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as si
from DISClib.Algorithms.Sorting import mergesort as ms
from DISClib.Algorithms.Sorting import quicksort as qs
assert cf
from datetime import date, timedelta
import time

"""
Se define la estructura de un catálogo de obras en el museo. 
El catálogo tendrá dos listas, una para los obras del museo, 
otra para los artistas.
"""

# Construccion de modelos

def newCatalog(type):
    """
    Inicializa el catálogo de obras. Crea una lista vacia para guardar
    todos las obras, adicionalmente, crea una lista vacia para los artistas.
    Retorna el catalogo inicializado.
    """
    catalog = {"artworks": None,
                "artists": None}

    catalog["artworks"] = lt.newList(type, 
                                    cmpfunction=compareDates)
    catalog["artists"] = lt.newList(type, 
                                    cmpfunction=compareCID)
    catalog["nations"] = lt.newList(type,
                                    cmpfunction=compareNation)
    return catalog

# Funciones para agregar informacion al catalogo

def addArtwork(catalog, artwork):
    if artwork["DateAcquired"] == "" or artwork["DateAcquired"] == "Unknown":
        hoy = date.today()
        artwork["DateAcquired"] = hoy.strftime("%Y-%m-%d")
    lt.addLast(catalog["artworks"], artwork)
    addNation(catalog, artwork)

def addNation(catalog, artwork):
    """
    Adiciona una nacionalidad a la lista de de nacionalidades,
    la cual hace referencia a las obras que provengan de esa nacionalidad.
    """
    codes = artwork["ConstituentID"]
    nations = catalog["nations"]
    countries = ArtworkNationality(catalog, codes)
    for country in lt.iterator(countries):
        pos_country = lt.isPresent(nations, country)
        if pos_country > 0:
            nation = lt.getElement(nations, pos_country)
        else:
            nation = newCountry(country)
            lt.addLast(nations, nation)
        lt.addLast(nation["artworks"], artwork)

def addArtist(catalog, artist):
    lt.addLast(catalog["artists"], artist)

# Funciones para creacion de datos

def newCountry(name):
    """
    Crea un nuevo diccionario de pais para agregar su 
    nombre y obras relacionadas a ese pais.
    """
    country = {"name": "", "artworks": None}
    country["name"] = name
    country["artworks"] = lt.newList()
    return country

def costoTransporte(obras):
    """
    Calcular el costo de transporte de cada obra en obras y agregar el dato al elemento correspondiente.
    """
    for obra in lt.iterator(obras):
        # sacar los datos relevantes y estipular valores por defecto
        peso = obra['Weight (kg)']
        largo = obra['Length (cm)']
        ancho = obra['Width (cm)']
        profundidad = obra['Depth (cm)']
        altura = obra['Height (cm)']
        if peso is "":
            peso = 0
        if largo is "":
            largo = 0
        if ancho is "":
            ancho = 0
        if profundidad is "":
            profundidad = 0
        if altura is "":
            altura = 0
        # calcular el tamano (tres posibles formas)
        t1 = (float(ancho)/100)*(float(altura)/100)
        t2 = (float(ancho)/100)*(float(largo)/100)
        t3 = (float(ancho)/100)*(float(altura)/100)*(float(profundidad)/100)
        # crear lista para comparar los tamanos y sacar el mas grande
        lista = lt.newList()
        lt.addLast(lista,peso)
        lt.addLast(lista,t3)
        lt.addLast(lista,t2)
        lt.addLast(lista,t1)
        ms.sort(lista,cmpfunction=ordenAscendente)
        tamano = lt.lastElement(lista)
        # estipular el costo y agregarlo a los datos de la obra
        if tamano == 0:
            costo = 48
        else:
            costo = tamano*72
        obra['Transcost (USD)'] = costo
    return obras

# Funciones de consulta

def getArtistbyCode(catalog, codes):
    """
    Consigue a un Artista por su codigo.
    """
    artists = catalog["artists"]
    group = lt.newList()
    cIDSs = codes.replace("[", "").replace("]", "").split(",")
    for cID in cIDSs:
        cID =cID.strip()
        pos = lt.isPresent(artists, cID)
        if pos>0:
            artist = lt.getElement(artists, pos)
            lt.addLast(group, artist)
    return group

def getArtistname(catalog, codes):
    """
    Consigue el nombre de un artista.
    """
    artists = getArtistbyCode(catalog, codes)
    names = ""
    for artist in lt.iterator(artists):
        names += artist["DisplayName"] + " "
    return names

def ArtworkNationality(catalog, codes):
    """
    Consigue la nacionalidad de una obra utilizando los codigos de la misma.
    """
    artists = getArtistbyCode(catalog, codes)
    nations = lt.newList()
    for artist in lt.iterator(artists):
        if artist["Nationality"] != "":
            lt.addLast(nations, artist["Nationality"])
    return nations

def getArtworkbydate(artworks, date):
    """
    Retorna una obra por su fecha de adquisición.
    """
    
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

def getArtworkbyNationality(catalog, country):
    """
    Devuelve todos las obras que pertenezcan a la nacionalidad
    solicitada.
    """
    nations = catalog["nations"]
    pos_country = lt.isPresent(nations, country)
    if pos_country > 0:
        nation = lt.getElement(nations, pos_country)
    return nation["artworks"]


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

def contarMedios(obras):
    """
    Cuenta la cantidad de medios que se usan en una lista de obras
    """
    medios = listaMedios(obras)
    num = lt.size(medios)
    return num

def costoTotal(obras):
    """
    Calcula el costo total de transportar unas obras.
    """
    ob = costoTransporte(obras)
    t = 0
    for o in lt.iterator(ob):
        c = o['Transcost (USD)']
        t += float(c)
    return int(t)

def pesoTotal(obras):
    """
    Calcula el peso total de las obras
    """
    w = 0
    for obra in lt.iterator(obras):
        peso = obra['Weight (kg)']
        if peso is "":
            peso = 0
        w += float(peso)
    return int(w)

# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date_1, artwork):
    if (date_1 in artwork["DateAcquired"]):
        return 0
    return -1

def compareCID(cID, artist):
    if cID in artist["ConstituentID"]:
        return 0
    return -1

def compareNation(nation, countries):
    if nation.lower() in countries["name"].lower():
        return 0
    return -1

def compareSizes(nacionality1, nacionality2):
    return ((lt.size(nacionality1["artworks"])) > (lt.size(nacionality2["artworks"])))

def cmpArtworkByDateAcquired(artwork1, artwork2):
    return (date.fromisoformat(artwork1["DateAcquired"]) < date.fromisoformat(artwork2["DateAcquired"]))

def ordenAscendente(a,b):
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

def compareDepartment(department, artwork):
    if department in artwork['Department']:
        return 0
    return -1

def compareDate(date,artwork):
    if date in artwork['Date']:
        return 0
    return -1

def compareCostos(costo,artwork):
    if costo in artwork['Transcost (USD)']:
        return 0
    return -1

# Funciones de ordenamiento

def organizeTopNationaly(catalog):
    """
    Organiza el Top de Nacionalidades con más obras.
    """
    sa.sort(catalog["nations"], cmpfunction=compareSizes)
    top = {}
    for nation in lt.iterator(catalog["nations"]):
        top[nation["name"]] = lt.size(nation["artworks"])
    return top

def sortArtworksbyDate(catalog, size, option):
    sub_list = lt.subList(catalog["artworks"], 1, size)
    sub_list = sub_list.copy()
    if int(option) == 1:
        sorted_list = si.sort(sub_list, cmpArtworkByDateAcquired)
    elif int(option) == 2:
        sorted_list = sa.sort(sub_list, cmpArtworkByDateAcquired)
    elif int(option) == 3:
        sorted_list = ms.sort(sub_list, cmpArtworkByDateAcquired)
    elif int(option) == 4:
        sorted_list = qs.sort(sub_list, cmpArtworkByDateAcquired)
    return sorted_list

def organizeArtworkbyDate(catalog, startDate, finishDate, size, option):
    """
    Organiza y retorna las obras que esten en un rango de 
    una fecha inicial y final. ()()()
    """
    org = lt.newList()
    d_0 = date.fromisoformat(startDate)
    d_f = date.fromisoformat(finishDate)
    delta = d_f - d_0
    start_time = time.process_time()
    artworks = sortArtworksbyDate(catalog, int(size), option)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    for day in range(delta.days + 1):
        new_day = d_0 + timedelta(days=day)
        new_date = new_day.strftime("%Y-%m-%d")
        art = getArtworkbydate(artworks, new_date)
        if art is not None:
            lt.addLast(org, art)
    
    return elapsed_time_mseg, org

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
    ms.sort(numeros,cmpfunction=ordenAscendente)
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

def artworksbyDepartment(catalog,department):
    """
    Retorna la lista de las obras en un departamento.
    """
    obras = lt.newList('SINGLE_LINKED',cmpfunction=compareDepartment)
    obras_d = lt.newList()
    for obra in lt.iterator(catalog['artworks']):
        lt.addLast(obras,obra)
    for o in lt.iterator(obras):
        if (o['Department'] == department):
            lt.addLast(obras_d,o)
    return obras_d

def masAntiguas(obras):
    """
    Retorna una lista con las 5 obras mas antiguas de obras 
    """
    lista = lt.newList('SINGLE_LINKED',cmpfunction=compareDate)
    fechas = lt.newList()
    antiguas = lt.newList()
    for obra in lt.iterator(obras):
        lt.addLast(lista,obra)
    for element in lt.iterator(lista):
        f = element['Date']
        if f is '':
            None
        else:
            lt.addLast(fechas,f)
    ms.sort(fechas,cmpfunction=ordenAscendente)
    i = 0
    while i < 5:
        fecha = lt.removeFirst(fechas)
        antigua = getElementbyparameterE(lista,fecha)
        lt.addLast(antiguas,antigua)
        i += 1
    return antiguas

def masCostosas(obras):
    """
    Retorna una lista con las 5 obras mas costosas de obras
    """
    datos = costoTransporte(obras)
    obras_costos = lt.newList('SINGLE_LINKED',cmpfunction=compareCostos)
    for dato in lt.iterator(datos):
        lt.addLast(obras_costos,dato)
    costos = lt.newList()
    costosas = lt.newList()
    for obra in lt.iterator(obras_costos):
        lt.addLast(costos,(obra['Transcost (USD)']))
    ms.sort(costos,cmpfunction=ordenAscendente)
    i = 0
    while i < 5:
        costo = lt.removeLast(costos)
        for obra in lt.iterator(obras_costos):
            if costo == obra['Transcost (USD)']:
                lt.addLast(costosas,obra)
        i += 1
    return costosas

def firstThreeD(lista):
    """
    Retorna una lista con los tres primeros elementos de una lista.
    """
    first = lt.subList(lista,1,3)
    return first
    
def lastThreeD(lista):
    """
    Retorna una lista con los 3 ultimos elementos de una lista.
    """
    last = lt.subList(lista,lt.size(lista)-2,3)
    return last
   
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