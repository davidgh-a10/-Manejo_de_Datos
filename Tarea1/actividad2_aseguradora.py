"""
Manejo de Datos - Facultad de Ciencias, UNAM
Actividad 2: Calculadora de prima de seguro (Aseguradora)


"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class EdadInvalidaError(Exception):
    """Se lanza cuando la edad ingresada no es un entero entre 18 y 99."""


class SumaAseguradaInvalidaError(Exception):
    """Se lanza cuando SA no es un número entre 500,000 y 3,000,000 MXN."""


class SexoInvalidoError(Exception):
    """Se lanza cuando el sexo ingresado no es 'M' ni 'F'."""


class RespuestaSiNoInvalidaError(Exception):
    """Se lanza cuando una respuesta Si/No no es válida."""


class TasaCambioInvalidaError(Exception):
    """Se lanza cuando la tasa de cambio es cero, negativa o no numérica."""



class FactorEdadStrategy(ABC):
    """Interfaz para calcular el factor K según la edad ajustada."""

    @abstractmethod
    def obtener_factor(self, edad_ajustada: int) -> float:
        ...


class FactorFemenino(FactorEdadStrategy):
    _TABLA = [
        (18, 25, 1.5),
        (25, 45, 1.7),
        (45, 65, 2.0),
        (65, 99, 2.2),
    ]

    def obtener_factor(self, edad_ajustada: int) -> float:
        return _buscar_en_tabla(self._TABLA, edad_ajustada)


class FactorMasculino(FactorEdadStrategy):
    _TABLA = [
        (18, 25, 2.0),
        (25, 45, 2.3),
        (45, 65, 2.5),
        (65, 99, 3.0),
    ]

    def obtener_factor(self, edad_ajustada: int) -> float:
        return _buscar_en_tabla(self._TABLA, edad_ajustada)


def _buscar_en_tabla(tabla, edad):
    """Busca el factor correspondiente a la edad dentro de una tabla de rangos."""
    for minimo, maximo, factor in tabla:
        if minimo <= edad <= maximo:
            return factor
    # Si por algún ajuste la edad queda justo en el límite superior (99)
    return tabla[-1][2]


def obtener_estrategia_factor(sexo: str) -> FactorEdadStrategy:
    return FactorFemenino() if sexo == "F" else FactorMasculino()



class ServicioTasaCambio(ABC):
    """Abstracción de un servicio externo que provee la tasa MXN/USD."""

    @abstractmethod
    def obtener_tasa(self) -> float:
        ...


class ServicioTasaCambioFijo(ServicioTasaCambio):
    """Implementación simple que simula un servicio externo."""

    def __init__(self, tasa: float = 21.13):
        self._validar_tasa(tasa)
        self._tasa = tasa

    @staticmethod
    def _validar_tasa(tasa):
        if not isinstance(tasa, (int, float)) or tasa <= 0:
            raise TasaCambioInvalidaError(
                "La tasa de cambio debe ser un número positivo."
            )

    def obtener_tasa(self) -> float:
        return self._tasa



@dataclass
class Asegurado:
    nombre: str
    edad: int
    sexo: str          # 'M' / 'F'
    fumador: str        # "Si" / "No"
    extra_prima: str     # "Si" / "No"
    suma_asegurada: float
    prima_mxn: float = field(default=0.0)
    prima_usd: float = field(default=0.0)

    def edad_ajustada(self) -> int:
        edad = self.edad
        if self.fumador == "No":
            edad -= 5
        if self.sexo == "F":
            edad -= 10
        if self.extra_prima == "Si":
            edad += 10
        return max(18, min(99, edad))



class CalculadoraPrima:
    def __init__(self, servicio_tasa: ServicioTasaCambio):
        self.servicio_tasa = servicio_tasa

    def calcular(self, asegurado: Asegurado) -> Asegurado:
        estrategia = obtener_estrategia_factor(asegurado.sexo)
        k = estrategia.obtener_factor(asegurado.edad_ajustada())
        prima_mxn = asegurado.suma_asegurada * k / 1000
        tasa = self.servicio_tasa.obtener_tasa()
        asegurado.prima_mxn = round(prima_mxn, 2)
        asegurado.prima_usd = round(prima_mxn / tasa, 2)
        return asegurado



def leer_nombre() -> str:
    while True:
        nombre = input("Nombre del asegurado: ").strip()
        if nombre:
            return nombre
        print("El nombre no puede estar vacío. Intenta de nuevo.")


def leer_edad() -> int:
    while True:
        try:
            valor = int(input("Edad (18-99): "))
            if not (18 <= valor <= 99):
                raise EdadInvalidaError("La edad debe estar entre 18 y 99.")
            return valor
        except ValueError:
            print("Error: la edad debe ser un número entero. Intenta de nuevo.")
        except EdadInvalidaError as e:
            print(f"Error: {e} Intenta de nuevo.")


def leer_sexo() -> str:
    while True:
        try:
            valor = input("Sexo (M/F): ").strip().upper()
            if valor not in ("M", "F"):
                raise SexoInvalidoError("El sexo debe ser 'M' o 'F'.")
            return valor
        except SexoInvalidoError as e:
            print(f"Error: {e} Intenta de nuevo.")


def leer_si_no(etiqueta: str) -> str:
    while True:
        try:
            valor = input(f"{etiqueta} (Si/No): ").strip().capitalize()
            if valor not in ("Si", "No"):
                raise RespuestaSiNoInvalidaError(
                    f"{etiqueta} solo acepta 'Si' o 'No'."
                )
            return valor
        except RespuestaSiNoInvalidaError as e:
            print(f"Error: {e} Intenta de nuevo.")


def leer_suma_asegurada() -> float:
    while True:
        try:
            valor = float(input("Suma asegurada SA (500,000 - 3,000,000 MXN): "))
            if not (500_000 <= valor <= 3_000_000):
                raise SumaAseguradaInvalidaError(
                    "SA debe estar entre 500,000 y 3,000,000 MXN."
                )
            return valor
        except ValueError:
            print("Error: SA debe ser un número. Intenta de nuevo.")
        except SumaAseguradaInvalidaError as e:
            print(f"Error: {e} Intenta de nuevo.")


def capturar_asegurado() -> Asegurado:
    nombre = leer_nombre()
    edad = leer_edad()
    sexo = leer_sexo()
    fumador = leer_si_no("¿Es fumador?")
    extra_prima = leer_si_no("¿Tiene extra-prima?")
    sa = leer_suma_asegurada()
    return Asegurado(nombre, edad, sexo, fumador, extra_prima, sa)




class GeneradorReporte:
    @staticmethod
    def generar(asegurados: list[Asegurado]) -> str:
        if not asegurados:
            return "No hay asegurados registrados."

        primas = [a.prima_mxn for a in asegurados]
        promedio = sum(primas) / len(primas)
        maxima = max(asegurados, key=lambda a: a.prima_mxn)
        minima = min(asegurados, key=lambda a: a.prima_mxn)

        con_extra = [a for a in asegurados if a.extra_prima == "Si"]
        mayor_extra = max(con_extra, key=lambda a: a.prima_mxn, default=None)

        lineas = [
            "\n=== Reporte final ===",
            f"Prima promedio: ${promedio:,.2f} MXN",
            f"Prima máxima: ${maxima.prima_mxn:,.2f} MXN ({maxima.nombre})",
            f"Prima mínima: ${minima.prima_mxn:,.2f} MXN ({minima.nombre})",
        ]
        if mayor_extra:
            lineas.append(
                f"Mayor prima con extra-prima: ${mayor_extra.prima_mxn:,.2f} "
                f"MXN ({mayor_extra.nombre})"
            )
        else:
            lineas.append("Ningún asegurado tiene extra-prima.")
        return "\n".join(lineas)


class ExportadorCarnet:
    def __init__(self, ruta: str):
        self.ruta = ruta

    def exportar(self, asegurados: list[Asegurado]) -> bool:
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                for a in asegurados:
                    archivo.write(
                        f"Nombre: {a.nombre}\n"
                        f"Edad: {a.edad} | Sexo: {a.sexo} | "
                        f"Fumador: {a.fumador} | Extra-prima: {a.extra_prima}\n"
                        f"Suma asegurada: ${a.suma_asegurada:,.2f} MXN\n"
                        f"Prima: ${a.prima_mxn:,.2f} MXN "
                        f"(${a.prima_usd:,.2f} USD)\n"
                        f"{'-' * 40}\n"
                    )
            return True
        except (PermissionError, FileNotFoundError, OSError) as e:
            print(f"No se pudo escribir el archivo de carnets: {e}")
            return False

#Programa principal

def leer_entero_positivo(mensaje: str) -> int:
    while True:
        try:
            valor = int(input(mensaje))
            if valor <= 0:
                raise ValueError
            return valor
        except ValueError:
            print("Debes ingresar un entero positivo. Intenta de nuevo.")


def main():
    print("=== Calculadora de Prima de Seguro ===")

    try:
        servicio_tasa = ServicioTasaCambioFijo()  # 21.13 por defecto
    except TasaCambioInvalidaError as e:
        print(f"No se pudo inicializar el servicio de tasa de cambio: {e}")
        return

    calculadora = CalculadoraPrima(servicio_tasa)

    n = leer_entero_positivo("¿Cuántos asegurados deseas capturar? ")
    asegurados = []

    for i in range(1, n + 1):
        print(f"\n--- Asegurado {i} de {n} ---")
        asegurado = capturar_asegurado()
        calculadora.calcular(asegurado)
        print(
            f"Prima calculada: ${asegurado.prima_mxn:,.2f} MXN "
            f"(${asegurado.prima_usd:,.2f} USD)"
        )
        asegurados.append(asegurado)

    print(GeneradorReporte.generar(asegurados))

    exportador = ExportadorCarnet("carnets_asegurados.txt")
    if exportador.exportar(asegurados):
        print("\nCarnets exportados a 'carnets_asegurados.txt'.")


if __name__ == "__main__":
    main()
