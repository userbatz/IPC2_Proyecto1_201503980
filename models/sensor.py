class SensorSuelo:
    def __init__(self, id_sensor, nombre):
        self.id = id_sensor
        self.nombre = nombre
        self.frecuencias = {}  # {id_estacion: valor}

    def agregar_frecuencia(self, id_estacion, valor):
        self.frecuencias[id_estacion] = valor

    def __str__(self):
        return f"Sensor Suelo {self.id} - {self.nombre} - Frecuencias: {self.frecuencias}"


class SensorCultivo:
    def __init__(self, id_sensor, nombre):
        self.id = id_sensor
        self.nombre = nombre
        self.frecuencias = {}  # {id_estacion: valor}

    def agregar_frecuencia(self, id_estacion, valor):
        self.frecuencias[id_estacion] = valor

    def __str__(self):
        return f"Sensor Cultivo {self.id} - {self.nombre} - Frecuencias: {self.frecuencias}"
