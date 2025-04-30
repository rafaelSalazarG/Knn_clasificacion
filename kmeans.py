import random
import math

def kmeansPP(vecinos: list):
    """
    Implementación del algoritmo K-Means++ para inicializar los centroides.
    """
    centroides = []
    noEscogidos = vecinos[:]
    
    # Escoger el primer centroide aleatoriamente
    index = random.randint(0, len(noEscogidos) - 1)
    centroides.append(noEscogidos.pop(index))
    
    distancias = []
    
    # Escoger el segundo centroide
    for noEscogido in noEscogidos:
        for centroide in centroides:
            # Calcular las distancias de un punto a cada centroide
            distancias.append(math.dist(centroide, noEscogido))
        # Escoger el punto más lejano como el siguiente centroide
        clasificador = distancias.index(max(distancias))
        distancias.clear()
    centroides.append(noEscogidos.pop(clasificador))
    
    # Escoger el tercer centroide
    for noEscogido in noEscogidos:
        d1, d2 = 0, 0
        for i, centroide in enumerate(centroides):
            if i == 0:
                d1 = math.dist(noEscogido, centroide)
            else:
                d2 = math.dist(noEscogido, centroide)
        distancias.append(min(d1, d2))
    clasificador = distancias.index(max(distancias))
    centroides.append(noEscogidos.pop(clasificador))
    distancias.clear()
    
    # Escoger el cuarto centroide
    for noEscogido in noEscogidos:
        d1, d2, d3 = 0, 0, 0
        for i, centroide in enumerate(centroides):
            if i == 0:
                d1 = math.dist(noEscogido, centroide)
            elif i == 1:
                d2 = math.dist(noEscogido, centroide)
            else:
                d3 = math.dist(noEscogido, centroide)
        distancias.append(min(d1, d2, d3))
    clasificador = distancias.index(max(distancias))
    centroides.append(noEscogidos.pop(clasificador))
    distancias.clear()
    
    return centroides


def kmeans(vecinos: list, tamMuestra: int, K: int):
    """
    Implementación del algoritmo K-Means.
    """
    # Inicializar los centroides usando K-Means++
    centroides = kmeansPP(vecinos)
    maxIteraciones = 40
    distancias = []
    contador = 0
    
    elemento1, elemento2, elemento3, elemento4 = [], [], [], []
    
    while contador < maxIteraciones:
        elemento1.clear()
        elemento2.clear()
        elemento3.clear()
        elemento4.clear()
        
        try:
            # Clasificar los puntos según el centroide más cercano
            for vecino in vecinos:
                for centroide in centroides:
                    distancias.append(math.dist(centroide, vecino))
                clasificador = distancias.index(min(distancias))
                distancias.clear()
                
                # Asignar el punto al grupo correspondiente
                if clasificador == 0:
                    elemento1.append(vecino)
                elif clasificador == 1:
                    elemento2.append(vecino)
                elif clasificador == 2:
                    elemento3.append(vecino)
                elif clasificador == 3:
                    elemento4.append(vecino)
                else:
                    print('Error en la clasificación')
            
            # Recalcular los centroides
            for j in range(K):
                for i in range(len(elemento1[0])):  # Asume que todos los puntos tienen la misma dimensión
                    suma = 0
                    if j == 0:
                        for z in range(len(elemento1)):
                            suma += elemento1[z][i]
                        centroides[j][i] = suma / len(elemento1)
                    elif j == 1:
                        for z in range(len(elemento2)):
                            suma += elemento2[z][i]
                        centroides[j][i] = suma / len(elemento2)
                    elif j == 2:
                        for z in range(len(elemento3)):
                            suma += elemento3[z][i]
                        centroides[j][i] = suma / len(elemento3)
                    elif j == 3:
                        for z in range(len(elemento4)):
                            suma += elemento4[z][i]
                        centroides[j][i] = suma / len(elemento4)
                    else:
                        print('Error en el cálculo de centroides')
            
            # Verificar si los grupos están balanceados
            if not (
                ((tamMuestra - 0.1 * tamMuestra) < len(elemento1) < (tamMuestra + 0.1 * tamMuestra)) and
                ((tamMuestra - 0.1 * tamMuestra) < len(elemento2) < (tamMuestra + 0.1 * tamMuestra)) and
                ((tamMuestra - 0.1 * tamMuestra) < len(elemento3) < (tamMuestra + 0.1 * tamMuestra)) and
                ((tamMuestra - 0.1 * tamMuestra) < len(elemento4) < (tamMuestra + 0.1 * tamMuestra))
            ) and (contador > (0.9 * maxIteraciones)):
                centroides = random.choices(vecinos, k=K)
                contador = 0
            
            contador += 1
        
        except ZeroDivisionError:
            centroides = random.choices(vecinos, k=K)
    
    return elemento1, elemento2, elemento3, elemento4