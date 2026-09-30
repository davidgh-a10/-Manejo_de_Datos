"""
Manejo de Datos - Facultad de Ciencias, UNAM
Ejercicio 3: Diccionario de palabras distintas, ordenadas alfabéticamente,
con conteo de frecuencia, tabla hash propia y dos algoritmos de
ordenamiento O(n log n) implementados desde cero (Merge Sort y Quick Sort).

Restricción del ejercicio: no se usa set() ni sorted()/list.sort() en
ningún punto. La eliminación de repetidos se hace con una tabla hash
propia (encadenamiento separado) y el ordenamiento con Merge Sort /
Quick Sort implementados manualmente.
"""

import random
import string
import time


# ---------------------------------------------------------------------------
# 1. Excepción propia
# ---------------------------------------------------------------------------

class TextoVacioError(Exception):
    """Se lanza cuando el texto de entrada está vacío."""


# ---------------------------------------------------------------------------
# 2. Normalización de texto
# ---------------------------------------------------------------------------

class NormalizadorTexto:
    """Limpia y normaliza texto antes de extraer palabras."""

    _ACENTOS = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "ñ": "n",
    }

    @classmethod
    def normalizar(cls, texto: str) -> str:
        if texto is None or texto.strip() == "":
            raise TextoVacioError("El texto de entrada está vacío.")

        texto = texto.lower()
        texto_normalizado = []
        for caracter in texto:
            texto_normalizado.append(cls._ACENTOS.get(caracter, caracter))
        return "".join(texto_normalizado)

    @staticmethod
    def extraer_palabras(texto: str) -> list:
        """Extrae secuencias de caracteres alfabéticos (a-z) como palabras."""
        palabras = []
        actual = []
        for caracter in texto:
            if "a" <= caracter <= "z":
                actual.append(caracter)
            else:
                if actual:
                    palabras.append("".join(actual))
                    actual = []
        if actual:
            palabras.append("".join(actual))
        return palabras


# ---------------------------------------------------------------------------
# 3. Tabla hash propia (encadenamiento separado) para eliminar repetidos
#    y contar frecuencias
# ---------------------------------------------------------------------------

class TablaHash:
    """
    Tabla hash con listas (buckets) para resolver colisiones por
    encadenamiento separado: cada posición del arreglo guarda una lista
    de pares (palabra, frecuencia); si dos palabras distintas producen
    el mismo índice, simplemente conviven en la misma lista y se
    distinguen comparando la palabra completa.
    """

    def __init__(self, num_buckets: int = 211):
        self.num_buckets = num_buckets
        self.buckets = [[] for _ in range(num_buckets)]
        self.num_palabras_distintas = 0

    def _funcion_hash(self, palabra: str) -> int:
        """Hash polinomial simple: h = (h*31 + ord(c)) mod num_buckets."""
        h = 0
        for caracter in palabra:
            h = (h * 31 + ord(caracter)) % self.num_buckets
        return h

    def agregar(self, palabra: str) -> None:
        indice = self._funcion_hash(palabra)
        bucket = self.buckets[indice]
        for i in range(len(bucket)):
            if bucket[i][0] == palabra:
                bucket[i] = (palabra, bucket[i][1] + 1)
                return
        bucket.append((palabra, 1))
        self.num_palabras_distintas += 1

    def obtener_pares(self) -> list:
        """Regresa una lista de tuplas (palabra, frecuencia), sin orden."""
        pares = []
        for bucket in self.buckets:
            for par in bucket:
                pares.append(par)
        return pares


# ---------------------------------------------------------------------------
# 4. Algoritmos de ordenamiento O(n log n) implementados desde cero
# ---------------------------------------------------------------------------

def merge_sort(lista: list) -> list:
    """Ordena una lista de cadenas (o tuplas cuyo primer elemento es una
    cadena) usando Merge Sort. Complejidad: Theta(n log n) siempre."""
    if len(lista) <= 1:
        return lista[:]

    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    return _combinar(izquierda, derecha)


def _combinar(izquierda: list, derecha: list) -> list:
    resultado = []
    i = j = 0
    while i < len(izquierda) and j < len(derecha):
        clave_izq = izquierda[i][0] if isinstance(izquierda[i], tuple) else izquierda[i]
        clave_der = derecha[j][0] if isinstance(derecha[j], tuple) else derecha[j]
        if clave_izq <= clave_der:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1
    while i < len(izquierda):
        resultado.append(izquierda[i])
        i += 1
    while j < len(derecha):
        resultado.append(derecha[j])
        j += 1
    return resultado


def quick_sort(lista: list) -> list:
    """Ordena una lista de cadenas (o tuplas) usando Quick Sort in-place
    sobre una copia. Complejidad: O(n log n) en promedio, O(n^2) en el
    peor caso (entrada ya ordenada con este esquema de pivote)."""
    copia = lista[:]
    _quick_sort_recursivo(copia, 0, len(copia) - 1)
    return copia


def _clave(elemento):
    return elemento[0] if isinstance(elemento, tuple) else elemento


def _quick_sort_recursivo(lista: list, bajo: int, alto: int) -> None:
    if bajo < alto:
        indice_pivote = _particionar(lista, bajo, alto)
        _quick_sort_recursivo(lista, bajo, indice_pivote - 1)
        _quick_sort_recursivo(lista, indice_pivote + 1, alto)


def _particionar(lista: list, bajo: int, alto: int) -> int:
    # Pivote aleatorio para evitar el peor caso en entradas ya ordenadas
    pivote_aleatorio = random.randint(bajo, alto)
    lista[pivote_aleatorio], lista[alto] = lista[alto], lista[pivote_aleatorio]

    pivote = _clave(lista[alto])
    i = bajo - 1
    for j in range(bajo, alto):
        if _clave(lista[j]) <= pivote:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    lista[i + 1], lista[alto] = lista[alto], lista[i + 1]
    return i + 1


# ---------------------------------------------------------------------------
# 5. Función principal del diccionario (extracción + dedup + orden + conteo)
# ---------------------------------------------------------------------------

def construir_diccionario(texto: str, algoritmo_orden=merge_sort) -> list:
    """
    Recibe un texto y regresa una lista de tuplas (palabra, frecuencia)
    ordenadas alfabéticamente, sin repetidos.
    """
    texto_normalizado = NormalizadorTexto.normalizar(texto)
    palabras = NormalizadorTexto.extraer_palabras(texto_normalizado)

    tabla = TablaHash()
    for palabra in palabras:
        tabla.agregar(palabra)

    pares = tabla.obtener_pares()
    return algoritmo_orden(pares)


# ---------------------------------------------------------------------------
# 6. Demostración con el ejemplo del enunciado
# ---------------------------------------------------------------------------

def demo_ejemplo():
    texto_ejemplo = (
        "Adventures in Disneyland. Two blondes were going to Disneyland "
        "when they came to a fork in the road. The sign read: Disneyland "
        "LEFT. So they went home."
    )
    diccionario = construir_diccionario(texto_ejemplo, algoritmo_orden=merge_sort)
    print("=== Diccionario alfabético (con frecuencia) ===")
    for palabra, frecuencia in diccionario:
        print(f"{palabra}: {frecuencia}")
    print()


# ---------------------------------------------------------------------------
# 7. Comparación empírica de tiempos de ejecución
# ---------------------------------------------------------------------------

def generar_texto_aleatorio(num_palabras: int) -> str:
    """Genera un texto sintético con num_palabras palabras aleatorias,
    reutilizando palabras de un vocabulario reducido para forzar
    repeticiones (y así probar también la deduplicación)."""
    vocabulario = [
        "".join(random.choices(string.ascii_lowercase, k=random.randint(3, 9)))
        for _ in range(max(20, num_palabras // 10))
    ]
    palabras = [random.choice(vocabulario) for _ in range(num_palabras)]
    return " ".join(palabras)


def medir_tiempo(func, *args) -> float:
    inicio = time.perf_counter()
    func(*args)
    fin = time.perf_counter()
    return fin - inicio


def comparacion_empirica():
    tamanios = [100, 1000, 10000]
    resultados = []

    print("=== Comparación empírica Merge Sort vs Quick Sort ===")
    print(f"{'N palabras':>12} | {'Distintas':>10} | {'Merge Sort (s)':>15} | {'Quick Sort (s)':>15}")
    print("-" * 62)

    for n in tamanios:
        texto = generar_texto_aleatorio(n)
        texto_normalizado = NormalizadorTexto.normalizar(texto)
        palabras = NormalizadorTexto.extraer_palabras(texto_normalizado)

        tabla = TablaHash()
        for palabra in palabras:
            tabla.agregar(palabra)
        pares = tabla.obtener_pares()

        t_merge = medir_tiempo(merge_sort, pares)
        t_quick = medir_tiempo(quick_sort, pares)

        resultados.append((n, len(pares), t_merge, t_quick))
        print(f"{n:>12} | {len(pares):>10} | {t_merge:>15.6f} | {t_quick:>15.6f}")

    return resultados


# ---------------------------------------------------------------------------
# 8. Programa principal
# ---------------------------------------------------------------------------

def main():
    try:
        demo_ejemplo()
    except TextoVacioError as e:
        print(f"Error: {e}")

    comparacion_empirica()


if __name__ == "__main__":
    main()
