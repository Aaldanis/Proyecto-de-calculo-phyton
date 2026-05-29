# Importa expresiones regulares para buscar la marca GRAFICAR_PYTHON
import re

# Importa NumPy para crear valores numéricos de x
import numpy as np

# Importa SymPy para interpretar expresiones matemáticas
import sympy as sp

# Importa Matplotlib para crear la gráfica
import matplotlib.pyplot as plt


# Función para detectar si la respuesta contiene una función graficable
def extraer_funcion_para_graficar(respuesta):

    # Busca una línea como:
    # GRAFICAR_PYTHON: x**2 - 4
    coincidencia = re.search(r"GRAFICAR_PYTHON:\s*(.+)", respuesta)

    # Si no encuentra la marca, no hay gráfica
    if not coincidencia:
        return None

    # Extrae la expresión matemática
    funcion = coincidencia.group(1).strip()

    # Limpia símbolos innecesarios
    funcion = funcion.replace("$", "")
    funcion = funcion.replace("`", "")

    # Devuelve la función limpia
    return funcion


# Función para crear la gráfica de una función explícita de x
def crear_grafica(funcion_texto):

    try:
        # Define la variable simbólica x
        x = sp.Symbol("x")

        # Convierte la expresión escrita en texto a expresión simbólica
        expresion = sp.sympify(funcion_texto)

        # Convierte la expresión simbólica en función numérica
        funcion = sp.lambdify(x, expresion, "numpy")

        # Crea valores de x desde -10 hasta 10
        valores_x = np.linspace(-10, 10, 500)

        # Evalúa la función en los valores de x
        valores_y = funcion(valores_x)

        # Crea la figura y los ejes
        fig, ax = plt.subplots()

        # Grafica la función
        ax.plot(valores_x, valores_y)

        # Dibuja el eje horizontal
        ax.axhline(0, linewidth=0.8)

        # Dibuja el eje vertical
        ax.axvline(0, linewidth=0.8)

        # Agrega cuadrícula
        ax.grid(True)

        # Agrega título
        ax.set_title(f"Gráfica de y = {funcion_texto}")

        # Etiqueta del eje x
        ax.set_xlabel("x")

        # Etiqueta del eje y
        ax.set_ylabel("y")

        # Devuelve la figura para mostrarla en Streamlit
        return fig

    except Exception:

        # Si ocurre un error, devuelve None
        return None