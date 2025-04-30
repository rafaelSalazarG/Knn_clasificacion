import cv2
import math
import kmeans
import numpy as np

def tomaUltimo(elemento: dict):
    return list(elemento.values())[0]

def calcularMomentos(tipoElemento: str, indice: int):
    """
    Calcula los momentos de Hu de una imagen binarizada.
    """
    path = 'C:/Users/rafad/OneDrive/Documentos/VSCode/fotosIA1/'
    im = cv2.imread(path + tipoElemento + str(indice) + '.jpg', cv2.IMREAD_GRAYSCALE)
    _, im = cv2.threshold(im, 70, 255, cv2.THRESH_BINARY)
    momentos = cv2.moments(im)
    return momentos

def calcularDistancias(vecinos: list, indiceVecino: int, prueba: str):
    """
    Calcula la distancia entre los momentos de Hu de una imagen de prueba y un vecino.
    """
    path = 'C:/Users/rafad/OneDrive/Documentos/VSCode/fotosIA1/'
    im = cv2.imread(prueba, cv2.IMREAD_GRAYSCALE)
    _, im = cv2.threshold(im, 70, 255, cv2.THRESH_BINARY)
    momentos = cv2.moments(im)
    momentosHu = cv2.HuMoments(momentos)
    distancia = 0
    for i in range(len(vecinos[0])):
        distancia += (momentosHu[i] - vecinos[indiceVecino][i]) ** 2
    return math.sqrt(distancia)

def identificarElementos(cantMuestra: int, e1: list, vecinos: list):
    """
    Identifica el tipo de elemento (tornillo, clavo, arandela, tuerca) basado en la moda.
    """
    modas = []
    modaTornillo = modaClavo = modaArandela = modaTuerca = 0

    for elemento in e1:
        for i in range(len(vecinos)):
            if elemento[0] == vecinos[i][0]:
                modas.append(i)

    for item in modas:
        if item < cantMuestra:
            modaTornillo += 1
        elif cantMuestra <= item < cantMuestra * 2:
            modaClavo += 1
        elif cantMuestra * 2 <= item < cantMuestra * 3:
            modaArandela += 1
        else:
            modaTuerca += 1

    numModa = max(modaTornillo, modaClavo, modaTuerca, modaArandela)
    if numModa == modaTornillo:
        return 0
    elif numModa == modaClavo:
        return 1
    elif numModa == modaArandela:
        return 2
    else:
        return 3

def main():
    """
    Función principal que clasifica elementos usando KNN y K-Means.
    """
    iteracionesCajas = 0
    numeroElementos = 4
    cantMuestra = 50
    tornillosHu, arandelasHu, clavosHu, tuercasHu = [], [], [], []
    vecinos = []
    distancias = []
    path = 'C:/Users/rafad/OneDrive/Documentos/VSCode/fotosIA1/'
    prueba = [
        path + 'pruebaArandela.jpg',
        path + 'pruebaClavo.jpg',
        path + 'pruebaTornillo.jpg',
        path + 'pruebaTuerca.jpg'
    ]
    K = 10
    kVecinos = []

    # Llenado de lista de momentos de vecinos
    for i in range(cantMuestra):
        vecinos.append(np.delete(cv2.HuMoments(calcularMomentos('tornillo', i)), 6))
    for i in range(cantMuestra):
        vecinos.append(np.delete(cv2.HuMoments(calcularMomentos('clavo', i)), 6))
    for i in range(cantMuestra):
        vecinos.append(np.delete(cv2.HuMoments(calcularMomentos('arandela', i)), 6))
    for i in range(cantMuestra):
        vecinos.append(np.delete(cv2.HuMoments(calcularMomentos('tuerca', i)), 6))

    # Aplicar K-Means
    e1, e2, e3, e4 = kmeans.kmeans(vecinos, cantMuestra, numeroElementos)

    # Clasificar los grupos obtenidos por K-Means
    for grupo, elementosHu in zip([e1, e2, e3, e4], [tornillosHu, clavosHu, arandelasHu, tuercasHu]):
        nElemento = identificarElementos(cantMuestra, grupo, vecinos)
        if nElemento == 0:
            tornillosHu = grupo[:]
        elif nElemento == 1:
            clavosHu = grupo[:]
        elif nElemento == 2:
            arandelasHu = grupo[:]
        else:
            tuercasHu = grupo[:]

    # Clasificar las pruebas
    for pruebaActual in prueba:
        distancias.clear()
        for i in range(len(vecinos)):
            distancias.append({i: calcularDistancias(vecinos, i, pruebaActual)})

        # Ordenar distancias y tomar los K vecinos más cercanos
        distancias.sort(key=tomaUltimo)
        kVecinos = [list(distancias[i].keys())[0] for i in range(K)]

        # Determinar la moda entre los K vecinos
        modaTornillo = modaArandela = modaTuerca = modaClavos = 0
        for indice in kVecinos:
            if indice < len(tornillosHu):
                modaTornillo += 1
            elif indice < len(tornillosHu) + len(clavosHu):
                modaClavos += 1
            elif indice < len(tornillosHu) + len(clavosHu) + len(arandelasHu):
                modaArandela += 1
            else:
                modaTuerca += 1

        moda = max(modaArandela, modaClavos, modaTornillo, modaTuerca)
        if moda == modaArandela:
            print('Arandela')
        elif moda == modaClavos:
            print('Clavo')
        elif moda == modaTornillo:
            print('Tornillo')
        elif moda == modaTuerca:
            print('Tuerca')
        else:
            print('Hubo un error')

        iteracionesCajas += 1

if __name__ == "__main__":
    main()
