# 🎓 Agente de Búsquedas No Informadas - Aula de Clases (10x20)

Este repositorio contiene la solución completa e interactiva desarrollada en **Python 3** con **Tkinter** para la asignatura de **Inteligencia Artificial** (7mo Semestre de Ingeniería en Software - Universidad Técnica de Ambato).

El proyecto modela a un **agente inteligente no informado** que percibe su entorno dentro de un plano cartesiano discreto de $10 \times 20$ cerámicas (aula de clases). El agente no posee información previa del espacio ni heurísticas guiadas; únicamente percibe su estado actual $S$ y aplica su **Función Sucesora formal** respetando las barreras del aula.

> 💡 **Implementación de Estructuras de Datos Propias:** No se utilizaron librerías externas ni auxiliares para las fronteras (`deque`, etc.). Las clases **`Cola`** (FIFO) y **`Pila`** (LIFO) fueron programadas **desde cero** en [nucleo/estructuras.py](file:///c:/Users/sebas/OneDrive%20-%20UNIVERSIDAD%20T%C3%89CNICA%20DE%20AMBATO/Inteligencia%20Artificial%202/B%C3%BAsquedas%20no%20Informadas/nucleo/estructuras.py).

---

## 📌 Formulación Formal del Problema

* **Espacio de Estados ($S$):** $s = (x, y)$ con $x \in [1..10]$ e $y \in [1..20]$. Total: $|S| = 200$ estados posibles.
* **Estado Inicial ($S_0$):** Asignado o generado aleatoriamente $(x_0, y_0) \in S$.
* **Estado Objetivo ($S_g$):** Fijo en $(1, 10)$ (Salida del aula).
* **Test Objetivo:** `es_objetivo(estado) -> True si estado == (1, 10)`.
* **Conjunto de Acciones ($A$):** $\{\text{Norte}, \text{Sur}, \text{Este}, \text{Oeste}\}$.
* **Función Sucesora ($Succ(s, a)$):** Valida físicamente los movimientos sin condicionales de atajo:
  * $\text{Norte}: (x, y + 1)$ si $y < 20$
  * $\text{Sur}: (x, y - 1)$ si $y > 1$
  * $\text{Este}: (x + 1, y)$ si $x < 10$
  * $\text{Oeste}: (x - 1, y)$ si $x > 1$
* **Costo del Camino ($g(n)$):** Costo unitario $c(s, a, s') = 1$ por cada movimiento.

---

## 🚀 Estrategias de Búsqueda Implementadas

1. **🏦 Búsqueda en Anchura:**
   * Estructura de Datos: **`Cola` propia (FIFO)** (`encolar`, `desencolar`).
   * Explora por niveles de profundidad. Garantiza completitud y la solución óptima.
2. **🥞 Búsqueda en Profundidad:**
   * Estructura de Datos: **`Pila` propia (LIFO)** (`apilar`, `desapilar`).
   * Explora las ramas hasta la máxima profundidad acotada por el control de nodos visitados.
3. **🔄 Profundidad Iterativa:**
   * Estructura de Datos: **`Pila` propia (LIFO)** con Límite $L$ creciente ($0, 1, 2, \dots$).
   * Combina la ventaja de memoria de profundidad con la optimidad de anchura.
4. **↔️ Búsqueda Bidireccional:**
   * Estructura de Datos: **DOS `Cola` propias (FIFO)** simultáneas.
   * Lanza un frente desde $S_0$ y otro desde $S_g = (1, 10)$ hasta detectar el punto de intersección.

---

## 📊 Tabla de Complejidad Computacional

| Estrategia | Cálculo Matemático Exacto (Nodos Generados) | Complejidad Tiempo | Complejidad Espacio | Completitud | Optimidad |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Anchura** | $b + b^2 + \dots + b^d + (b^{d+1} - b)$ | $O(b^{d+1})$ | $O(b^{d+1})$ | Sí | Sí |
| **Profundidad** | Depende de la rama elegida (Máx. $b^m$) | $O(b^m)$ | $O(b \times m)$ | Sí (con visitados) | No |
| **Profundidad Iterativa** | $(d)b + (d-1)b^2 + \dots + (1)b^d$ | $O(b^d)$ | $O(b \times d)$ | Sí | Sí |
| **Bidireccional** | $2 \times b^{d/2}$ | $O(b^{d/2})$ | $O(b^{d/2})$ | Sí | Sí |

---

## 📁 Estructura del Repositorio (100% en Español)

```
Búsquedas no Informadas/
├── nucleo/
│   ├── estructuras.py          # CLASES PROPIAS: Cola (FIFO) y Pila (LIFO) sin librerías
│   ├── nodo.py                 # Clase Nodo (Padre, costo g(n), profundidad d, id)
│   ├── ambiente.py             # Clase AmbienteCuadricula (Aula 10x20 y Función Sucesora)
│   └── metricas.py             # Calculadora de fórmulas exactas y complejidades
├── algoritmos/
│   ├── anchura.py              # Búsqueda en Anchura (Usa Cola propia)
│   ├── profundidad.py          # Búsqueda en Profundidad (Usa Pila propia)
│   ├── profundidad_iterativa.py# Profundidad Iterativa (Usa Pila propia)
│   └── bidireccional.py        # Búsqueda Bidireccional (Usa dos Cola propias)
├── visualizador/
│   └── aplicacion.py           # Dashboard visual e interactivo Tkinter
├── pruebas/
│   └── probar_busquedas.py     # Script de pruebas automatizadas
├── main.py                     # Ejecutable principal
├── .gitignore
└── README.md
```

---

## 💻 Instrucciones de Ejecución

### Prerrequisitos:
* **Python 3.8+** y la librería estándar `tkinter`.

### Ejecutar la Aplicación Gráfica:
```bash
python main.py
```

### Ejecutar Pruebas Automatizadas:
```bash
python pruebas/probar_busquedas.py
```
