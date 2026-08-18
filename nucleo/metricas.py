"""
Módulo Núcleo: Métricas Teóricas y Empíricas para Búsquedas No Informadas

Calcula las fórmulas matemáticas exactas de nodos generados,
las complejidades en Tiempo y Espacio (Big-O) y evalúa
la completitud y optimalidad de cada estrategia.
"""

class MetricasBusqueda:
    @staticmethod
    def calcular_teorico_anchura(b, d):
        """
        Cálculo exacto para Búsqueda en Anchura:
        Nodos generados = b + b^2 + ... + b^d + (b^(d+1) - b)
        """
        if b <= 1:
            return d + 1
        suma_niveles = sum(b**i for i in range(1, d + 1))
        termino_extra = (b**(d + 1)) - b
        return suma_niveles + termino_extra

    @staticmethod
    def calcular_teorico_profundidad(b, m):
        """
        Cálculo exacto para Búsqueda en Profundidad (peor caso):
        Máximo b^m nodos
        """
        return b**m if m <= 10 else f"O({b}^{m})"

    @staticmethod
    def calcular_teorico_profundidad_iterativa(b, d):
        """
        Cálculo exacto para Profundidad Iterativa:
        (d)b + (d-1)b^2 + ... + (1)b^d
        """
        if b <= 1:
            return (d * (d + 1)) // 2
        total = 0
        for i in range(1, d + 1):
            peso = (d - i + 1)
            total += peso * (b**i)
        return total

    @staticmethod
    def calcular_teorico_bidireccional(b, d):
        """
        Cálculo exacto para Búsqueda Bidireccional:
        2 * b^(d/2)
        """
        d_mitad = d / 2.0
        return 2 * (b**d_mitad)

    @classmethod
    def obtener_tabla_resumen_teorica(cls, b=3.0, d=10, m=200):
        """
        Genera el cuadro comparativo teórico según las especificaciones del deber.
        """
        return [
            {
                "estrategia": "🏦 Anchura",
                "formula_exacta": "b + b² + ... + b^d + (b^(d+1) - b)",
                "calculo_ejemplo": f"{cls.calcular_teorico_anchura(b, d):,.0f}" if isinstance(cls.calcular_teorico_anchura(b, d), (int, float)) else str(cls.calcular_teorico_anchura(b, d)),
                "tiempo": "O(b^(d+1))",
                "espacio": "O(b^(d+1))",
                "completitud": "Sí (espacio finito)",
                "optimidad": "Sí (costo 1)"
            },
            {
                "estrategia": "🥞 Profundidad",
                "formula_exacta": "Depende de la rama (Máx. b^m)",
                "calculo_ejemplo": str(cls.calcular_teorico_profundidad(b, m)),
                "tiempo": "O(b^m)",
                "espacio": "O(b × m)",
                "completitud": "Sí (con visitados)",
                "optimidad": "No"
            },
            {
                "estrategia": "🔄 Profundidad Iterativa",
                "formula_exacta": "(d)b + (d-1)b² + ... + (1)b^d",
                "calculo_ejemplo": f"{cls.calcular_teorico_profundidad_iterativa(b, d):,.0f}",
                "tiempo": "O(b^d)",
                "espacio": "O(b × d)",
                "completitud": "Sí",
                "optimidad": "Sí (costo 1)"
            },
            {
                "estrategia": "↔️ Bidireccional",
                "formula_exacta": "2 × b^(d/2)",
                "calculo_ejemplo": f"{cls.calcular_teorico_bidireccional(b, d):,.2f}",
                "tiempo": "O(b^(d/2))",
                "espacio": "O(b^(d/2))",
                "completitud": "Sí",
                "optimidad": "Sí"
            }
        ]
