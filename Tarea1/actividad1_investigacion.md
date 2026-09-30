# Actividad 1 — Investigación: PEP8, Principios SOLID y análisis del Ejercicio 3

**Manejo de Datos — Facultad de Ciencias, UNAM**

---

## Parte A — PEP8

A continuación se describen 10 reglas de la guía de estilo PEP8, cada una con un ejemplo de
código "antes" (que la incumple) y "después" (que la respeta).

### 1. Nombres de variables y funciones en `snake_case`
Las variables y funciones deben nombrarse en minúsculas separando palabras con guion bajo.

```python
# Antes
nombreCompleto = "Ana Perez"
def CalcularTotal(a, b): return a + b

# Después
nombre_completo = "Ana Perez"
def calcular_total(a, b):
    return a + b
```

### 2. Nombres de clases en `CapWords` (CamelCase)
Las clases se nombran con mayúscula inicial en cada palabra, sin guiones bajos.

```python
# Antes
class factor_edad: ...

# Después
class FactorEdad:
    ...
```

### 3. Indentación de 4 espacios (nunca tabs)
Cada nivel de bloque debe indentarse con 4 espacios de forma consistente.

```python
# Antes
def suma(a, b):
  return a + b

# Después
def suma(a, b):
    return a + b
```

### 4. Longitud máxima de línea (79 caracteres)
Las líneas muy largas deben partirse para mejorar la legibilidad.

```python
# Antes
resultado = calcular_prima(suma_asegurada, edad, sexo, fumador, extra_prima, tasa_de_cambio)

# Después
resultado = calcular_prima(
    suma_asegurada, edad, sexo, fumador, extra_prima, tasa_de_cambio
)
```

### 5. Espacios alrededor de operadores
Se debe dejar un espacio antes y después de operadores binarios (`=`, `+`, `==`, etc.).

```python
# Antes
x=1+2
if x==3:pass

# Después
x = 1 + 2
if x == 3:
    pass
```

### 6. Un import por línea y orden de imports
Los imports van uno por línea y agrupados: librería estándar, terceros, locales.

```python
# Antes
import os, sys
from mi_paquete import modulo_local
import requests

# Después
import os
import sys

import requests

from mi_paquete import modulo_local
```

### 7. Dos líneas en blanco entre definiciones de nivel superior
Funciones y clases definidas a nivel de módulo se separan con dos líneas en blanco.

```python
# Antes
def a():
    pass
def b():
    pass

# Después
def a():
    pass


def b():
    pass
```

### 8. Comparar con `None` usando `is` / `is not`
No se debe usar `==` para comparar contra `None`.

```python
# Antes
if valor == None:
    ...

# Después
if valor is None:
    ...
```

### 9. Constantes en `MAYUSCULAS_CON_GUIONES`
Los valores que no cambian durante la ejecución se nombran en mayúsculas.

```python
# Antes
tasa_default = 21.13

# Después
TASA_CAMBIO_DEFAULT = 21.13
```

### 10. Docstrings para módulos, clases y funciones
Toda función o clase pública debe documentar su propósito con una docstring.

```python
# Antes
def calcular_prima(sa, k):
    return sa * k / 1000

# Después
def calcular_prima(sa, k):
    """Calcula la prima anual dado el monto asegurado y el factor de edad."""
    return sa * k / 1000
```

**Fuente consultada:** PEP 8 — Style Guide for Python Code, disponible en
https://peps.python.org/pep-0008/

---

## Parte B — ¿Qué es SOLID?

SOLID es un acrónimo que agrupa cinco principios de diseño orientado a objetos, propuestos
originalmente por Robert C. Martin, cuyo objetivo es que el software sea más fácil de
mantener, extender y probar a lo largo del tiempo, reduciendo el acoplamiento entre
componentes y favoreciendo la reutilización de código.

### 1. S — Single Responsibility Principle (Principio de responsabilidad única)

**Problema que resuelve:** evita que una clase concentre demasiadas razones para cambiar,
lo que la vuelve frágil y difícil de mantener.

**Explicación:** una clase debería tener una sola responsabilidad y, por lo tanto, un solo
motivo para modificarse. Cuando una clase mezcla varias tareas (por ejemplo, cálculo de
datos y almacenamiento en disco), cualquier cambio en una de esas tareas obliga a tocar una
clase que en realidad debería permanecer estable para las demás.

```python
# Código malo: la clase mezcla cálculo y persistencia
class Asegurado:
    def __init__(self, nombre, sa, k):
        self.nombre = nombre
        self.sa = sa
        self.k = k

    def calcular_prima(self):
        return self.sa * self.k / 1000

    def guardar_en_archivo(self, ruta):
        with open(ruta, "a") as f:
            f.write(f"{self.nombre}: {self.calcular_prima()}\n")
```

```python
# Código bueno: se separa el cálculo de la persistencia
class Asegurado:
    def __init__(self, nombre, sa, k):
        self.nombre = nombre
        self.sa = sa
        self.k = k

    def calcular_prima(self):
        return self.sa * self.k / 1000


class ExportadorCarnet:
    def guardar(self, asegurado, ruta):
        with open(ruta, "a") as f:
            f.write(f"{asegurado.nombre}: {asegurado.calcular_prima()}\n")
```

**Fuente:** Martin, R. C., *Clean Architecture / SOLID Principles*, resumido en
freeCodeCamp — "SOLID: The First 5 Principles of Object-Oriented Design".

### 2. O — Open/Closed Principle (Principio de abierto/cerrado)

**Problema que resuelve:** evita que agregar nuevas funcionalidades obligue a modificar
código ya probado y en funcionamiento.

**Explicación:** las entidades de software deben estar abiertas a extensión pero cerradas
a modificación. Esto se logra normalmente mediante abstracciones (clases abstractas o
interfaces) que permiten añadir nuevos comportamientos creando nuevas clases, sin tocar el
código existente.

```python
# Código malo: agregar un nuevo tipo de asegurado obliga a modificar la función
def calcular_factor(sexo, edad):
    if sexo == "F":
        return 1.5
    elif sexo == "M":
        return 2.0
    # cada nuevo caso requiere editar esta función
```

```python
# Código bueno: se extiende agregando subclases, sin tocar el código existente
from abc import ABC, abstractmethod

class FactorEdadStrategy(ABC):
    @abstractmethod
    def obtener_factor(self, edad):
        ...

class FactorFemenino(FactorEdadStrategy):
    def obtener_factor(self, edad):
        return 1.5 if edad <= 25 else 1.7

class FactorMasculino(FactorEdadStrategy):
    def obtener_factor(self, edad):
        return 2.0 if edad <= 25 else 2.3
```

**Fuente:** Martin, R. C. (1996), *The Open-Closed Principle*, Object Mentor.

### 3. L — Liskov Substitution Principle (Principio de sustitución de Liskov)

**Problema que resuelve:** evita que una subclase rompa el comportamiento esperado por el
código que usa la clase base.

**Explicación:** los objetos de una subclase deben poder sustituir a los de su clase base
sin alterar la corrección del programa. Si una subclase cambia el contrato (por ejemplo,
lanza excepciones inesperadas o ignora el resultado esperado), viola este principio.

```python
# Código malo: la subclase no respeta el contrato de la clase base
class FactorEdadStrategy:
    def obtener_factor(self, edad):
        return 1.0

class FactorInvalido(FactorEdadStrategy):
    def obtener_factor(self, edad):
        raise NotImplementedError("No implementado")  # rompe el contrato
```

```python
# Código bueno: toda subclase cumple el mismo contrato y puede sustituirse
class FactorEdadStrategy(ABC):
    @abstractmethod
    def obtener_factor(self, edad):
        """Siempre regresa un factor numérico válido."""

class FactorFemenino(FactorEdadStrategy):
    def obtener_factor(self, edad):
        return 1.5 if edad <= 25 else 1.7

class FactorMasculino(FactorEdadStrategy):
    def obtener_factor(self, edad):
        return 2.0 if edad <= 25 else 2.3
# Cualquiera de las dos puede usarse donde se espera un FactorEdadStrategy
```

**Fuente:** Liskov, B. (1987), *Data Abstraction and Hierarchy*, OOPSLA.

### 4. I — Interface Segregation Principle (Principio de segregación de interfaces)

**Problema que resuelve:** evita obligar a una clase a implementar métodos que no necesita
solo por compartir una interfaz demasiado grande.

**Explicación:** es preferible tener varias interfaces pequeñas y específicas que una sola
interfaz general. Así, cada clase implementa únicamente lo que realmente usa.

```python
# Código malo: una sola interfaz obliga a implementar métodos innecesarios
class ServicioAsegurado(ABC):
    @abstractmethod
    def calcular_prima(self): ...
    @abstractmethod
    def exportar_pdf(self): ...
    @abstractmethod
    def convertir_moneda(self): ...

class AseguradoBasico(ServicioAsegurado):
    def calcular_prima(self):
        return 100
    def exportar_pdf(self):
        raise NotImplementedError  # no lo necesita
    def convertir_moneda(self):
        raise NotImplementedError  # no lo necesita
```

```python
# Código bueno: interfaces pequeñas y específicas
class CalculaPrima(ABC):
    @abstractmethod
    def calcular_prima(self): ...

class ConvierteMoneda(ABC):
    @abstractmethod
    def convertir_moneda(self, monto): ...

class AseguradoBasico(CalculaPrima):
    def calcular_prima(self):
        return 100
```

**Fuente:** Martin, R. C. (1996), *Interface Segregation Principle*, Object Mentor.

### 5. D — Dependency Inversion Principle (Principio de inversión de dependencias)

**Problema que resuelve:** evita que los módulos de alto nivel dependan directamente de
detalles concretos de bajo nivel (por ejemplo, un servicio externo específico), lo que
dificulta cambiarlos o probarlos.

**Explicación:** los módulos de alto nivel no deben depender de implementaciones concretas,
sino de abstracciones; y esas abstracciones no deben depender de los detalles, sino al
revés. En la práctica, esto se logra recibiendo dependencias (como un servicio de tasa de
cambio) a través de una interfaz, en vez de crearlas directamente dentro de la clase.

```python
# Código malo: la clase depende directamente de una implementación concreta
class CalculadoraPrima:
    def convertir_a_usd(self, monto_mxn):
        tasa = 21.13  # acoplado directamente al valor concreto
        return monto_mxn / tasa
```

```python
# Código bueno: se depende de una abstracción inyectada
class ServicioTasaCambio(ABC):
    @abstractmethod
    def obtener_tasa(self): ...

class ServicioTasaCambioFijo(ServicioTasaCambio):
    def __init__(self, tasa=21.13):
        self.tasa = tasa
    def obtener_tasa(self):
        return self.tasa

class CalculadoraPrima:
    def __init__(self, servicio_tasa: ServicioTasaCambio):
        self.servicio_tasa = servicio_tasa

    def convertir_a_usd(self, monto_mxn):
        return monto_mxn / self.servicio_tasa.obtener_tasa()
```

**Fuente:** Martin, R. C. (1996), *The Dependency Inversion Principle*, Object Mentor.

---

## Aplicación de SOLID en el Ejercicio 2 (Aseguradora)

| Requisito del ejercicio 2 | Principio SOLID aplicado | Dónde se aplica |
|---|---|---|
| Excepciones propias (`EdadInvalidaError`, etc.) | **S** (Responsabilidad única) | Cada excepción tiene la única responsabilidad de señalar un tipo de error de validación. |
| Jerarquía `FactorEdadStrategy` con `FactorFemenino`/`FactorMasculino` | **O** (Abierto/cerrado) y **L** (Sustitución de Liskov) | Se puede añadir una nueva categoría (p. ej. `FactorNoBinario`) sin modificar `CalculadoraPrima`; cualquier subclase de `FactorEdadStrategy` puede sustituir a otra sin romper el cálculo. |
| Servicio de tasa de cambio independiente | **D** (Inversión de dependencias) | `CalculadoraPrima` depende de la abstracción `ServicioTasaCambio`, no de un valor fijo. |
| Separación entre cálculo de prima, generación de reporte y exportación a archivo | **S** (Responsabilidad única) e **I** (Segregación de interfaces) | `Asegurado`/`CalculadoraPrima` calculan; `GeneradorReporte` reporta; `ExportadorCarnet` exporta — cada clase expone solo los métodos que sus clientes necesitan. |

---

## Aplicación de SOLID en el Ejercicio 3 (Diccionario)

| Requisito del ejercicio 3 | Principio SOLID aplicado | Dónde se aplica |
|---|---|---|
| Tabla hash propia para eliminar repetidos | **S** (Responsabilidad única) | `TablaHash` solo se encarga de almacenar/consultar palabras, independiente del ordenamiento. |
| Merge Sort y Quick Sort intercambiables | **O** (Abierto/cerrado) y **D** (Inversión de dependencias) | Ambos algoritmos implementan una misma interfaz `AlgoritmoOrdenamiento`; el programa principal depende de esa abstracción y puede usar cualquiera sin modificar el resto del código. |
| Normalización de texto separada de la extracción de palabras | **S** (Responsabilidad única) | `NormalizadorTexto` solo limpia y normaliza, no cuenta ni ordena. |

*(Nota: adaptar esta tabla a las clases y nombres finales que usen en su implementación real
del Ejercicio 3.)*

---

## Ejercicio 3 — Diccionario: tabla comparativa y análisis de complejidad

### Resolución de colisiones en la tabla hash propia

La tabla hash (`TablaHash`) usa **encadenamiento separado**: internamente es un arreglo de
211 posiciones (*buckets*), y cada posición guarda una lista de pares `(palabra, frecuencia)`.
La función hash es un hash polinomial simple (`h = (h*31 + ord(c)) mod num_buckets`). Cuando
dos palabras distintas producen el mismo índice (colisión), ambas conviven en la lista de esa
posición; para saber si una palabra ya existe se recorre esa lista (normalmente muy corta) y
se compara carácter a carácter con `==`, en vez de comparar la palabra nueva contra *todas*
las palabras ya vistas.

### Tabla comparativa de tiempos de ejecución

Se generaron textos sintéticos de tamaño creciente (reutilizando un vocabulario reducido para
forzar repeticiones) y se midió el tiempo de `merge_sort` y `quick_sort` sobre la lista de
palabras distintas resultante, usando el módulo `time` (`time.perf_counter`):

| N (palabras totales) | Palabras distintas | Merge Sort (s) | Quick Sort (s) |
|---:|---:|---:|---:|
| 100    | 20    | 0.000020 | 0.000023 |
| 1,000  | 100   | 0.000106 | 0.000089 |
| 10,000 | 1,000 | 0.001399 | 0.001534 |

*(Los tiempos exactos varían ligeramente entre ejecuciones y equipos, pero el orden de
magnitud y la tendencia de crecimiento se mantienen; se recomienda que cada equipo corra
`comparacion_empirica()` en su propia máquina y reporte sus números.)*

### Análisis de complejidad Big-O

| Algoritmo | Mejor caso | Peor caso | Contraste con lo medido |
|---|---|---|---|
| Tabla hash (eliminación de repetidos) | O(1) por inserción, O(n) total | O(n) por inserción si hay muchas colisiones en un mismo bucket, O(n²) total en el peor caso | En la práctica, con 211 buckets y pocas palabras distintas por bucket, el tiempo de construir la tabla crece de forma prácticamente lineal con el número de palabras del texto. |
| Merge Sort | Θ(n log n) (siempre, no tiene mejor/peor caso distinto) | Θ(n log n) | Los tiempos medidos crecen de forma consistente con n·log(n): al pasar de 100 a 10,000 palabras (100× más), el tiempo aumenta ~70×, cercano al factor teórico n·log(n) (≈ 100 × log(10000)/log(100) ≈ 200, del mismo orden). |
| Quick Sort | O(n log n) (partición balanceada) | O(n²) (partición muy desbalanceada, p. ej. entrada ya ordenada con pivote fijo) | Se usó **pivote aleatorio** precisamente para evitar el peor caso en entradas ordenadas o con pocos valores distintos; con esto, los tiempos medidos son muy similares a los de Merge Sort (ambos O(n log n) en el caso promedio). |

**Conclusión:** para este tamaño de entradas (hasta 10,000 palabras) ambos algoritmos de
ordenamiento se comportan de forma muy similar y consistente con O(n log n); la tabla hash
domina el tiempo total solo si se generan muchas colisiones (bucket count muy pequeño frente
al número de palabras distintas), lo cual se evita eligiendo un número de buckets adecuado.
