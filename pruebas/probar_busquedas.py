"""
Módulo de Pruebas Unitarias para las Búsquedas No Informadas (en Español)
"""

import sys
import os

# Agregar directorio raíz al path de Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nucleo.ambiente import AmbienteCuadricula
from algoritmos.anchura import BusquedaAnchura
from algoritmos.profundidad import BusquedaProfundidad
from algoritmos.profundidad_iterativa import ProfundidadIterativa
from algoritmos.bidireccional import BusquedaBidireccional

def probar_entorno():
    print("--- Test 1: Ambiente de Cuadricula 10x20 ---")
    ambiente = AmbienteCuadricula()
    print(f"Estado Inicial S_0: {ambiente.estado_inicial}")
    print(f"Estado Objetivo S_g: {AmbienteCuadricula.ESTADO_OBJETIVO}")
    
    # Probar límites en esquina (1, 1)
    sucesores_1_1 = AmbienteCuadricula.obtener_sucesores((1, 1))
    print(f"Sucesores de (1, 1): {sucesores_1_1}")
    assert ("Oeste", (-1, 1)) not in sucesores_1_1
    assert ("Sur", (1, 0)) not in sucesores_1_1
    assert ((1, 2), "Norte") in sucesores_1_1
    assert ((2, 1), "Este") in sucesores_1_1

    # Probar límites en esquina (10, 20)
    sucesores_10_20 = AmbienteCuadricula.obtener_sucesores((10, 20))
    print(f"Sucesores de (10, 20): {sucesores_10_20}")
    assert ("Norte", (10, 21)) not in sucesores_10_20
    assert ("Este", (11, 20)) not in sucesores_10_20
    print("[OK] Ambiente validado correctamente.\n")

def probar_algoritmos():
    print("--- Test 2: Ejecucion de Algoritmos desde S_0 = (10, 20) hacia S_g = (1, 10) ---")
    s0 = (10, 20)

    # 1. Anchura
    res_anchura = BusquedaAnchura.resolver(s0)
    print(f"Anchura: Exito={res_anchura['exito']}, Largo Camino={len(res_anchura['camino'])-1}, Nodos Exp={res_anchura['nodos_expandidos']}, Nodos Gen={res_anchura['nodos_generados']}, Tiempo={res_anchura['tiempo_ejecucion_ms']:.2f}ms")
    assert res_anchura['exito']
    assert res_anchura['camino'][-1][0] == (1, 10)

    # 2. Profundidad
    res_prof = BusquedaProfundidad.resolver(s0)
    print(f"Profundidad: Exito={res_prof['exito']}, Largo Camino={len(res_prof['camino'])-1}, Nodos Exp={res_prof['nodos_expandidos']}, Nodos Gen={res_prof['nodos_generados']}, Tiempo={res_prof['tiempo_ejecucion_ms']:.2f}ms")
    assert res_prof['exito']
    assert res_prof['camino'][-1][0] == (1, 10)

    # 3. Profundidad Iterativa
    res_prof_it = ProfundidadIterativa.resolver(s0)
    print(f"Profundidad Iterativa: Exito={res_prof_it['exito']}, Largo Camino={len(res_prof_it['camino'])-1}, Nodos Exp={res_prof_it['nodos_expandidos']}, Nodos Gen={res_prof_it['nodos_generados']}, Tiempo={res_prof_it['tiempo_ejecucion_ms']:.2f}ms")
    assert res_prof_it['exito']
    assert res_prof_it['camino'][-1][0] == (1, 10)

    # 4. Bidireccional
    res_bi = BusquedaBidireccional.resolver(s0)
    print(f"Bidireccional: Exito={res_bi['exito']}, Largo Camino={len(res_bi['camino'])-1}, Nodos Exp={res_bi['nodos_expandidos']}, Nodos Gen={res_bi['nodos_generados']}, Tiempo={res_bi['tiempo_ejecucion_ms']:.2f}ms")
    assert res_bi['exito']
    assert res_bi['camino'][-1][0] == (1, 10)

    print("[OK] Todos los 4 algoritmos encontraron el objetivo (1, 10) exitosamente.\n")

if __name__ == "__main__":
    probar_entorno()
    probar_algoritmos()
