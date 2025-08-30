import xml.etree.ElementTree as ET

from models.campo import CampoAgricola
from models.estacion import EstacionBase
from models.sensor import SensorSuelo, SensorCultivo


class XMLManager:
    def __init__(self):
        self.campos = []  # lista de objetos CampoAgricola

    # -------------------------
    # Lectura del archivo XML
    # -------------------------
    def cargar_archivo(self, ruta):
        try:
            tree = ET.parse(ruta)
            root = tree.getroot()
            self.campos.clear()

            for campo_elem in root.findall("campo"):
                # Crear campo agrícola
                campo = CampoAgricola(
                    id_campo=campo_elem.get("id"),
                    nombre=campo_elem.get("nombre")
                )

                # ---- Estaciones Base ----
                est_base_elem = campo_elem.find("estacionesBase")
                if est_base_elem is not None:
                    for est_elem in est_base_elem.findall("estacion"):
                        estacion = EstacionBase(
                            id_estacion=est_elem.get("id"),
                            nombre=est_elem.get("nombre")
                        )
                        campo.estaciones.agregar(estacion)

                # ---- Sensores de Suelo ----
                sensores_suelo_elem = campo_elem.find("sensoresSuelo")
                if sensores_suelo_elem is not None:
                    for sensor_elem in sensores_suelo_elem.findall("sensorS"):
                        sensor = SensorSuelo(
                            id_sensor=sensor_elem.get("id"),
                            nombre=sensor_elem.get("nombre")
                        )
                        for freq_elem in sensor_elem.findall("frecuencia"):
                            id_est = freq_elem.get("idEstacion")
                            valor = int((freq_elem.text or "0").strip())
                            sensor.agregar_frecuencia(id_est, valor)
                        campo.sensores_suelo.agregar(sensor)

                # ---- Sensores de Cultivo ----
                sensores_cultivo_elem = campo_elem.find("sensoresCultivo")
                if sensores_cultivo_elem is not None:
                    for sensor_elem in sensores_cultivo_elem.findall("sensorT"):
                        sensor = SensorCultivo(
                            id_sensor=sensor_elem.get("id"),
                            nombre=sensor_elem.get("nombre")
                        )
                        for freq_elem in sensor_elem.findall("frecuencia"):
                            id_est = freq_elem.get("idEstacion")
                            valor = int((freq_elem.text or "0").strip())
                            sensor.agregar_frecuencia(id_est, valor)
                        campo.sensores_cultivo.agregar(sensor)

                self.campos.append(campo)

            print("✅ Archivo cargado con éxito")
            return True

        except Exception as e:
            print(f"❌ Error al cargar el archivo: {e}")
            return False

    # -------------------------
    # Mostrar Campos cargados
    # -------------------------
    def mostrar_campos(self):
        for campo in self.campos:
            print(f"Campo {campo.id} - {campo.nombre}")

    # -------------------------
    # Escritura del archivo XML
    # -------------------------
    def escribir_salida(self, ruta):
        if not self.campos:
            print("❌ No hay datos procesados para exportar")
            return

        try:
            root = ET.Element("camposAgricolas")

            for campo in self.campos:
                campo_elem = ET.SubElement(root, "campo", {
                    "id": campo.id,
                    "nombre": campo.nombre
                })

                # --- Estaciones Reducidas ---
                est_base_elem = ET.SubElement(campo_elem, "estacionesBaseReducidas")
                for est in campo.estaciones_reducidas:
                    # Si est es un string de ids agrupados, usar como id y nombre
                    ET.SubElement(est_base_elem, "estacion", {
                        "id": est,
                        "nombre": est
                    })

                # --- Sensores de Suelo (matriz reducida) ---
                sensores_suelo_elem = ET.SubElement(campo_elem, "sensoresSuelo")
                sensores_suelo = self._lista_a_array(campo.sensores_suelo)
                matriz_suelo = campo.matriz_suelo_reducida or []

                for j, sensor in enumerate(sensores_suelo):
                    sensor_elem = ET.SubElement(sensores_suelo_elem, "sensorS", {
                        "id": sensor.id,
                        "nombre": sensor.nombre
                    })
                    for i, est in enumerate(campo.estaciones_reducidas or []):
                        # Validar que la matriz tenga la fila y columna
                        if i < len(matriz_suelo) and j < len(matriz_suelo[i]):
                            valor = matriz_suelo[i][j]
                            if valor > 0:
                                ET.SubElement(sensor_elem, "frecuencia", {
                                    "idEstacion": est
                                }).text = str(valor)

                # --- Sensores de Cultivo (matriz reducida) ---
                sensores_cultivo_elem = ET.SubElement(campo_elem, "sensoresCultivo")
                sensores_cultivo = self._lista_a_array(campo.sensores_cultivo)
                matriz_cultivo = campo.matriz_cultivo_reducida or []

                for j, sensor in enumerate(sensores_cultivo):
                    sensor_elem = ET.SubElement(sensores_cultivo_elem, "sensorT", {
                        "id": sensor.id,
                        "nombre": sensor.nombre
                    })
                    for i, est in enumerate(campo.estaciones_reducidas or []):
                        # Validar que la matriz tenga la fila y columna
                        if i < len(matriz_cultivo) and j < len(matriz_cultivo[i]):
                            valor = matriz_cultivo[i][j]
                            if valor > 0:
                                ET.SubElement(sensor_elem, "frecuencia", {
                                    "idEstacion": est
                                }).text = str(valor)

            # Guardar archivo
            tree = ET.ElementTree(root)
            tree.write(ruta, encoding="utf-8", xml_declaration=True)

            print(f"💾 Archivo de salida generado: {ruta}")

        except Exception as e:
            print(f"❌ Error al escribir archivo de salida: {e}")

    # -------------------------
    # Auxiliar para convertir Lista a array
    # -------------------------
    def _lista_a_array(self, lista):
        arr = []
        actual = lista.primero
        while actual:
            arr.append(actual.dato)
            actual = actual.siguiente
        return arr
