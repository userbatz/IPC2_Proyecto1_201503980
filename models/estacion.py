class EstacionBase:
    def __init__(self, id_estacion, nombre):
        self.id = id_estacion
        self.nombre = nombre

    def __str__(self):
        return f"{self.id} - {self.nombre}"
