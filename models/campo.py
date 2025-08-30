from structures.lista import Lista

class CampoAgricola:
    def __init__(self, id_campo, nombre):
        self.id = id_campo
        self.nombre = nombre
        self.estaciones = Lista()
        self.sensores_suelo = Lista()
        self.sensores_cultivo = Lista()

        # Nuevos atributos para guardar resultados del procesamiento
        self.estaciones_reducidas = []  # lista de estaciones agrupadas
        self.matriz_suelo_reducida = []  # frecuencias reducidas suelo
        self.matriz_cultivo_reducida = []  # frecuencias reducidas cultivo

    def __str__(self):
        return f"Campo {self.id} - {self.nombre}"
