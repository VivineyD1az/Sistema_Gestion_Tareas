import json
from datetime import datetime

# Clase Tarea
class Tarea:
    def __init__(self, titulo, descripcion, fecha_vencimiento):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha_vencimiento = fecha_vencimiento
        self.completado = False

    def marcar_completada(self):
        self.completado = True

    def editar_tarea(self, nuevo_titulo, nueva_descripcion, nueva_fecha):
        self.titulo = nuevo_titulo
        self.descripcion = nueva_descripcion
        self.fecha_vencimiento = nueva_fecha


# Clase Usuario
class Usuario:
    def __init__(self, nombre_usuario, contraseña):
        self.nombre_usuario = nombre_usuario
        self.contraseña = contraseña
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def eliminar_tarea(self, titulo_tarea):
        self.tareas = [tarea for tarea in self.tareas if tarea.titulo != titulo_tarea]

    def obtener_tareas(self):
        return self.tareas


# Clase SistemaGestionTareas
class SistemaGestionTareas:
    def __init__(self, archivo_datos="datos_usuario.json"):
        self.usuarios = {}
        self.archivo_datos = archivo_datos
        self.cargar_datos()

    def cargar_datos(self):
        try:
            with open(self.archivo_datos, "r") as archivo:
                datos = json.load(archivo)
                for nombre_usuario, info in datos.items():
                    usuario = Usuario(nombre_usuario, info["contraseña"])
                    for tarea_info in info["tareas"]:
                        tarea = Tarea(tarea_info["titulo"], tarea_info["descripcion"], tarea_info["fecha_vencimiento"])
                        tarea.completado = tarea_info["completada"]
                        usuario.agregar_tarea(tarea)
                    self.usuarios[nombre_usuario] = usuario
        except FileNotFoundError:
            print("Archivo de datos no encontrado, se creará uno nuevo al guardar.")

    def guardar_datos(self):
        datos = {}
        for nombre_usuario, usuario in self.usuarios.items():
            datos[nombre_usuario] = {
                "contraseña": usuario.contraseña,
                "tareas": [
                    {
                        "titulo": tarea.titulo,
                        "descripcion": tarea.descripcion,
                        "fecha_vencimiento": tarea.fecha_vencimiento,
                        "completada": tarea.completado
                    }
                    for tarea in usuario.tareas
                ]
            }
        with open(self.archivo_datos, "w") as archivo:
            json.dump(datos, archivo, indent=4)

    def registrar_usuario(self, nombre_usuario, contraseña):
        if nombre_usuario in self.usuarios:
            print("El nombre de usuario ya existe.")
            return False
        self.usuarios[nombre_usuario] = Usuario(nombre_usuario, contraseña)
        self.guardar_datos()
        print("Usuario registrado con éxito.")
        return True

    def iniciar_sesion(self, nombre_usuario, contraseña):
        usuario = self.usuarios.get(nombre_usuario)
        if usuario and usuario.contraseña == contraseña:
            print("Inicio de sesión exitoso.")
            return usuario
        else:
            print("Nombre de usuario o contraseña incorrectos.")
            return None

    def menu_usuario(self, usuario):
        while True:
            print("\n--- MENÚ USUARIO ---")
            print("1. Crear tarea")
            print("2. Ver tareas")
            print("3. Editar tarea")
            print("4. Completar tarea")
            print("5. Eliminar tarea")
            print("6. Cerrar sesión")

            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                titulo = input("Título de la tarea: ")
                descripcion = input("Ingresa la descripción: ")
                fecha_vencimiento = input("Fecha de vencimiento (YYYY-MM-DD): ")
                tarea = Tarea(titulo, descripcion, fecha_vencimiento)
                usuario.agregar_tarea(tarea)
                self.guardar_datos()
                print("Tarea guardada con éxito.")

            elif opcion == "2":
                tareas = usuario.obtener_tareas()
                if not tareas:
                    print("No tienes tareas.")
                else:
                    for idx, tarea in enumerate(tareas, start=1):
                        estado = "Completada" if tarea.completado else "Pendiente"
                        print(f"{idx}. {tarea.titulo} - {estado} (vence {tarea.fecha_vencimiento})")

            elif opcion == "3":
                titulo_tarea = input("Título de la tarea a editar: ")
                tarea = next((t for t in usuario.tareas if t.titulo == titulo_tarea), None)
                if tarea:
                    nuevo_titulo = input("Nuevo título: ")
                    nueva_descripcion = input("Nueva descripción: ")
                    nueva_fecha = input("Fecha de vencimiento (YYYY-MM-DD): ")
                    tarea.editar_tarea(nuevo_titulo, nueva_descripcion, nueva_fecha)
                    self.guardar_datos()
                    print("Tarea actualizada con éxito.")
                else:
                    print("Tarea no encontrada.")

            elif opcion == "4":
                titulo_tarea = input("Título de la tarea a completar: ")
                tarea = next((t for t in usuario.tareas if t.titulo == titulo_tarea), None)
                if tarea:
                    tarea.marcar_completada()
                    self.guardar_datos()
                    print("Tarea marcada como completada.")
                else:
                    print("Tarea no encontrada.")

            elif opcion == "5":
                titulo_tarea = input("Título de la tarea a eliminar: ")
                usuario.eliminar_tarea(titulo_tarea)
                self.guardar_datos()
                print("Tarea eliminada con éxito.")

            elif opcion == "6":
                print("Cerrando sesión...")
                break

            else:
                print("Opción no válida.")


if __name__ == "__main__":
    sistema = SistemaGestionTareas()
    while True:
        print("\n--- SISTEMA DE GESTIÓN DE TAREAS ---")
        print("1. Registrar usuario")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            contraseña = input("Ingrese su contraseña: ")
            sistema.registrar_usuario(nombre_usuario, contraseña)

        elif opcion == "2":
            nombre_usuario = input("Nombre de usuario: ")
            contraseña = input("Contraseña: ")
            usuario = sistema.iniciar_sesion(nombre_usuario, contraseña)
            if usuario:
                sistema.menu_usuario(usuario)

        elif opcion == "3":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción no válida.")
