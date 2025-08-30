from services.xmlRead import XMLManager
from services.procesador import Procesador

def main():
    gestor_xml = XMLManager()
    procesador = Procesador(gestor_xml)

    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Cargar archivo")
        print("2. Procesar archivo")
        print("3. Escribir archivo salida")
        print("4. Mostrar datos del estudiante")
        print("5. Generar gráfica")
        print("6. Salida")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ruta = input("Ingrese la ruta del archivo XML de entrada: ")
            gestor_xml.cargar_archivo(ruta)
        elif opcion == "2":
            procesador.procesar()
        elif opcion == "3":
            ruta = input("Ingrese la ruta y nombre del archivo de salida (ej: salida/salida.xml): ")
            gestor_xml.escribir_salida(ruta)
        elif opcion == "4":
            print("Nombre: Gerson Batz Cocon\nCarné: 201503980\nCurso: IPC2 - Proyecto 1")
        elif opcion == "5":
            if not gestor_xml.campos:
                print("❌ No hay campos cargados para graficar.")
                continue
            from services.graficador import Graficador
            graficador = Graficador()
            print("Seleccione el tipo de gráfica:")
            print("1. Frecuencias originales")
            print("2. Matriz reducida")
            print("3. Patrones")
            tipo_op = input("Opción: ")
            if tipo_op == "1":
                tipo = "frecuencia"
            elif tipo_op == "2":
                tipo = "reducida"
            elif tipo_op == "3":
                tipo = "patrones"
            else:
                print("Opción inválida.")
                continue
            campo = gestor_xml.campos[0]  # Por simplicidad, graficar el primer campo
            archivo = input("Nombre de archivo de salida (ej: graphs/campo_01): ")
            graficador.graficar_matriz(campo, tipo=tipo, archivo=archivo)
        elif opcion == "6":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
