"""
Punto de Entrada Principal (main.py)

Ejecuta la Aplicación Gráfica Tkinter para la materia de Inteligencia Artificial.
Uso:
    python main.py
"""

import sys
import os
import tkinter as tk

# Asegurar importación de módulos locales
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from visualizador.aplicacion import AplicacionVisualizador

def principal():
    raiz = tk.Tk()
    app = AplicacionVisualizador(raiz)
    raiz.mainloop()

if __name__ == "__main__":
    principal()
