# Knn_clasificacion
Este código implementa un sistema de clasificación de imágenes basado en los algoritmos K-Means y K-Nearest Neighbors (KNN). Está diseñado para identificar objetos como tornillos, clavos, arandelas y tuercas a partir de imágenes binarizadas. El código presentado debe servir como ejemplo, dado que no se proveen las imágenes necesarias para entrenar al algoritmo de ML.
A continuación, se explica su funcionamiento:

1. Cálculo de características (Momentos de Hu)
La función calcularMomentos procesa imágenes binarizadas para calcular los momentos de Hu, que son características invariantes a rotaciones, traslaciones y escalas.
Estas características se utilizan para representar cada imagen de manera compacta y robusta.
2. Cálculo de distancias
La función calcularDistancias calcula la distancia euclidiana entre los momentos de Hu de una imagen de prueba y los momentos de Hu de las imágenes de referencia (vecinos).
Esto es esencial para el algoritmo KNN, que clasifica una imagen en función de sus vecinos más cercanos.
3. Clasificación con K-Means
La función kmeans (importada del archivo kmeans.py) agrupa las imágenes de referencia en 4 grupos (tornillos, clavos, arandelas y tuercas) basándose en sus momentos de Hu.
La función identificarElementos asigna un tipo de objeto a cada grupo utilizando la moda (el tipo más frecuente entre los vecinos).
4. Clasificación con KNN
Para cada imagen de prueba, el sistema:
Calcula las distancias a todos los vecinos.
Ordena las distancias y selecciona los K vecinos más cercanos.
Determina la clase de la imagen de prueba basándose en la moda de las clases de los K vecinos.
5. Flujo principal (main)
Carga de datos:
Procesa imágenes de tornillos, clavos, arandelas y tuercas para calcular sus momentos de Hu.
Almacena estos momentos en una lista de vecinos.
Agrupamiento con K-Means:
Agrupa los vecinos en 4 grupos y asigna un tipo de objeto a cada grupo.
Clasificación de imágenes de prueba:
Clasifica imágenes de prueba (e.g., pruebaArandela.jpg) utilizando KNN.
Imprime el tipo de objeto identificado (e.g., "Arandela", "Clavo").
6. Propósito
Este código es un ejemplo práctico de cómo combinar técnicas de agrupamiento no supervisado (K-Means) y clasificación supervisada (KNN) para resolver un problema de clasificación de imágenes. Es útil en aplicaciones como:

Inspección automatizada en líneas de producción.
Clasificación de objetos en sistemas de visión por computadora.
7. Resultados esperados
El sistema debería clasificar correctamente las imágenes de prueba como "Tornillo", "Clavo", "Arandela" o "Tuerca".
La precisión dependerá de la calidad de las imágenes y de los parámetros del modelo (e.g., número de vecinos K).
