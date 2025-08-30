from structures.lista import Lista

class Procesador:
    def __init__(self, gestor_xml):
        self.gestor_xml = gestor_xml

    def procesar(self):
        if not self.gestor_xml.campos:
            print("❌ No hay campos cargados. Use la opción 1 primero.")
            return

        for campo in self.gestor_xml.campos:
            print(f"\n⚙️ Procesando {campo.nombre}...")

            # Obtener listas como arrays
            estaciones = self._lista_a_array(campo.estaciones)
            sensores_suelo = self._lista_a_array(campo.sensores_suelo)
            sensores_cultivo = self._lista_a_array(campo.sensores_cultivo)

            # Construir matrices F
            matriz_suelo = self._construir_matriz(estaciones, sensores_suelo)
            matriz_cultivo = self._construir_matriz(estaciones, sensores_cultivo)

            print("\n📊 Matriz F[n,s] (suelo):")
            self._imprimir_matriz(matriz_suelo, estaciones)

            print("\n📊 Matriz F[n,t] (cultivo):")
            self._imprimir_matriz(matriz_cultivo, estaciones)

            # Construir patrones
            patrones_suelo = self._generar_patrones(matriz_suelo)
            patrones_cultivo = self._generar_patrones(matriz_cultivo)

            print("\n🔎 Patrones suelo (Fp[n,s]):")
            for i, patron in enumerate(patrones_suelo):
                print(f"{estaciones[i].id}: {patron}")

            print("\n🔎 Patrones cultivo (Fp[n,t]):")
            for i, patron in enumerate(patrones_cultivo):
                print(f"{estaciones[i].id}: {patron}")

            # Reducir matrices
            matriz_suelo_reducida, estaciones_reducidas_suelo = self._reducir_matriz(matriz_suelo, estaciones, patrones_suelo)
            matriz_cultivo_reducida, estaciones_reducidas_cultivo = self._reducir_matriz(matriz_cultivo, estaciones, patrones_cultivo)

            print("\n✅ Matriz reducida Fr[n,s] (suelo):")
            self._imprimir_matriz(matriz_suelo_reducida, estaciones_reducidas_suelo)

            print("\n✅ Matriz reducida Fr[n,t] (cultivo):")
            self._imprimir_matriz(matriz_cultivo_reducida, estaciones_reducidas_cultivo)

            # Guardar resultados en el campo
            campo.matriz_suelo_reducida = matriz_suelo_reducida
            campo.matriz_cultivo_reducida = matriz_cultivo_reducida
            campo.estaciones_reducidas = estaciones_reducidas_suelo  # usamos las de suelo, aplica igual a cultivo

    # ---------------- Métodos auxiliares ----------------

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

    def _reducir_matriz(self, matriz, estaciones, patrones):
        grupos = {}
        for i, patron in enumerate(patrones):
            clave = tuple(patron)
            if clave not in grupos:
                grupos[clave] = {
                    "indices": [],
                    "suma": [0] * len(patron)
                }
            grupos[clave]["indices"].append(estaciones[i].id)
            for j, val in enumerate(matriz[i]):
                grupos[clave]["suma"][j] += val

        matriz_reducida = []
        estaciones_reducidas = []
        for datos in grupos.values():
            matriz_reducida.append(datos["suma"])
            estaciones_reducidas.append(",".join(datos["indices"]))

        return matriz_reducida, estaciones_reducidas

    def _imprimir_matriz(self, matriz, estaciones_reducidas):
        if not matriz:
            print("❌ Matriz vacía")
            return

        # Encabezados
        encabezado = "      " + "  ".join([f"S{i+1}" for i in range(len(matriz[0]))])
        print(encabezado)

        # Filas con estaciones reducidas
        for i, fila in enumerate(matriz):
            fila_str = "  ".join(str(x) for x in fila)
            print(f"{estaciones_reducidas[i]}: {fila_str}")
