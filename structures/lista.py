from structures.nodo import Nodo

class Lista:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def esta_vacia(self):
        return self.primero is None

    def agregar(self, dato):
        nuevo = Nodo(dato)
        if self.esta_vacia():
            self.primero = nuevo
            self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            self.ultimo = nuevo

    def recorrer(self):
        actual = self.primero
        while actual is not None:
            print(actual.dato)
            actual = actual.siguiente
