import graphviz

class Graficador:
    def __init__(self):
        pass

    def graficar_matriz(self, campo, tipo="frecuencia", archivo="salida/grafica"):
        """
        Genera una gráfica usando Graphviz.
        tipo puede ser: 'frecuencia', 'patrones', 'reducida'
        """
        dot = graphviz.Digraph(comment=f"Grafo {campo.nombre}", format="png")
        dot.attr(rankdir="LR")  # disposición izquierda-derecha

        # Definir nodos de estaciones y sensores como matriz visual
        if tipo == "frecuencia":
            estaciones = self._lista_a_array(campo.estaciones)
            sensores_suelo = self._lista_a_array(campo.sensores_suelo)
            sensores_cultivo = self._lista_a_array(campo.sensores_cultivo)

            matriz_suelo = self._construir_matriz(estaciones, sensores_suelo)
            matriz_cultivo = self._construir_matriz(estaciones, sensores_cultivo)

            # Subgrafo para alinear estaciones horizontalmente (arriba)
            with dot.subgraph() as s:
                s.attr(rank='same')
                for est in estaciones:
                    s.node(str(est), f"Estación {est}", group="estaciones")

            # Subgrafo para alinear sensores verticalmente (izquierda)
            for i, sensor in enumerate(sensores_suelo):
                sensor_id = f"Ss{i+1}"
                dot.node(sensor_id, f"Sensor Suelo {sensor.id}", shape="box", group="sensores")
            for i, sensor in enumerate(sensores_cultivo):
                sensor_id = f"Sc{i+1}"
                dot.node(sensor_id, f"Sensor Cultivo {sensor.id}", shape="ellipse", group="sensores")

            # Conexiones de matriz suelo (estación -> sensor suelo)
            for j, est in enumerate(estaciones):
                for i, sensor in enumerate(sensores_suelo):
                    if matriz_suelo[j][i] > 0:
                        dot.edge(str(est), f"Ss{i+1}", label=str(matriz_suelo[j][i]))

            # Conexiones de matriz cultivo (estación -> sensor cultivo)
            for j, est in enumerate(estaciones):
                for i, sensor in enumerate(sensores_cultivo):
                    if matriz_cultivo[j][i] > 0:
                        dot.edge(str(est), f"Sc{i+1}", label=str(matriz_cultivo[j][i]))

        elif tipo == "reducida":
            estaciones = campo.estaciones_reducidas
            sensores_suelo = self._lista_a_array(campo.sensores_suelo)
            sensores_cultivo = self._lista_a_array(campo.sensores_cultivo)

            matriz_suelo = campo.matriz_suelo_reducida
            matriz_cultivo = campo.matriz_cultivo_reducida

            with dot.subgraph() as s:
                s.attr(rank='same')
                for est in estaciones:
                    s.node(str(est), f"Estación {est}", group="estaciones")

            for i, sensor in enumerate(sensores_suelo):
                sensor_id = f"Ss{i+1}"
                dot.node(sensor_id, f"Sensor Suelo {sensor.id}", shape="box", group="sensores")
            for i, sensor in enumerate(sensores_cultivo):
                sensor_id = f"Sc{i+1}"
                dot.node(sensor_id, f"Sensor Cultivo {sensor.id}", shape="ellipse", group="sensores")

            for j, est in enumerate(estaciones):
                for i, sensor in enumerate(sensores_suelo):
                    if matriz_suelo[j][i] > 0:
                        dot.edge(str(est), f"Ss{i+1}", label=str(matriz_suelo[j][i]))
            for j, est in enumerate(estaciones):
                for i, sensor in enumerate(sensores_cultivo):
                    if matriz_cultivo[j][i] > 0:
                        dot.edge(str(est), f"Sc{i+1}", label=str(matriz_cultivo[j][i]))

        elif tipo == "patrones":
            estaciones = self._lista_a_array(campo.estaciones)
            sensores_suelo = self._lista_a_array(campo.sensores_suelo)
            sensores_cultivo = self._lista_a_array(campo.sensores_cultivo)

            matriz_suelo = self._generar_patrones(
                self._construir_matriz(estaciones, sensores_suelo))
            matriz_cultivo = self._generar_patrones(
                self._construir_matriz(estaciones, sensores_cultivo))

            with dot.subgraph() as s:
                s.attr(rank='same')
                for est in estaciones:
                    s.node(str(est), f"Estación {est}", group="estaciones")

            for i, sensor in enumerate(sensores_suelo):
                sensor_id = f"Ss{i+1}"
                dot.node(sensor_id, f"Patrón Suelo {sensor.id}", shape="box", group="sensores")
            for i, sensor in enumerate(sensores_cultivo):
                sensor_id = f"Sc{i+1}"
                dot.node(sensor_id, f"Patrón Cultivo {sensor.id}", shape="ellipse", group="sensores")

            for j, est in enumerate(estaciones):
                for i, sensor in enumerate(sensores_suelo):
                    if matriz_suelo[j][i] > 0:
                        dot.edge(str(est), f"Ss{i+1}", label="1")
            for j, est in enumerate(estaciones):
                for i, sensor in enumerate(sensores_cultivo):
                    if matriz_cultivo[j][i] > 0:
                        dot.edge(str(est), f"Sc{i+1}", label="1")

        else:
            print("❌ Tipo de gráfica inválido")
            return

        salida = dot.render(archivo, cleanup=True)
        print(f"📊 Gráfica generada: {salida}")

    # ---------------- Auxiliares ----------------

    def _lista_a_array(self, lista):
        arr = []
        actual = lista.primero
        while actual:
            arr.append(actual.dato)
            actual = actual.siguiente
        return arr

    def _construir_matriz(self, estaciones, sensores):
        matriz = []
        for estacion in estaciones:
            fila = []
            for sensor in sensores:
                valor = sensor.frecuencias.get(estacion.id, 0)
                fila.append(valor)
            matriz.append(fila)
        return matriz

    def _generar_patrones(self, matriz):
        patrones = []
        for fila in matriz:
            patron = [1 if val > 0 else 0 for val in fila]
            patrones.append(patron)
        return patrones
