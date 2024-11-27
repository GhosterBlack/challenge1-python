# Importamos librerías y módulos necesarios
import re  # Para trabajar con expresiones regulares, validaciones de formato
import getpass  # Para gestionar contraseñas de manera segura (ocultas al ingreso)
import bcrypt  # Para encriptar y verificar contraseñas de forma segura
from datetime import datetime  # Para trabajar con fechas y horas
import os  # Para interactuar con el sistema operativo (por ejemplo, borrar consola)
import platform  # Para obtener información sobre el sistema operativo

# Creamos constantes para los menús de interacción con el usuario
MENU_LOGIN = """
--- Menú de Login ---
1. Iniciar Sesión
2. Registrarse
3. Salir
"""

MENU_PRINCIPAL = """
Menu principal
1. Agregar experimento
2. Ver experimentos
3. Análisis de resultados
4. Generar informe
5. Configuración
6. Cerrar sesión
7. Salir
"""

# Menú para agregar experimentos
MENU_AGREGAR_EXPERIMENTO = """
--- Menú Agregar Experimento ---
1. Ingresar Nombre del Experimento
2. ¿Ya realizó el experimento?
3. Guardar Experimento
4. Cancelar
"""

# Menú para ver experimentos
MENU_VER_EXPERIMENTOS = """
--- Menú Ver Experimentos ---
1. Ver Todos los Experimentos
2. Buscar Experimento
3. Ordenar Experimentos
4. Filtrar por Tipo de Experimento
5. Volver al Menú Principal
"""

# Menú para análisis de resultados
MENU_ANALISIS_RESULTADOS = """
--- Menú Análisis de Resultados ---
1. Calcular Promedio
2. Calcular Máximo
3. Calcular Mínimo
4. Ver Análisis Completo
5. Volver al Menú Principal
"""

# Menú para generar informes
MENU_GENERAR_INFORME = """
--- Menú Generar Informe ---
1. Generar Informe Completo
2. Seleccionar Experimentos para Informe
3. Exportar Informe a TXT
4. Vista Previa del Informe
5. Volver al Menú Principal
"""

# Menú de configuración
MENU_CONFIGURACION = """
--- Menú Configuración ---
1. Opciones de Exportación
2. Opciones de Seguridad
3. Restablecer Base de Datos
4. Volver al Menú Principal
"""

# Constantes extras para la interacción
SELECT = "Seleccione una opcion: "
BADOPTION = "Opcion incorrecta"
BADINFOREQUEST = "! Datos ingresados no validos"
WRITEURESPONSE = "Escriba su respuesta: "
BARSPACE = "--------------------"
RETURNTOMENU = "Volver al menu principal"
FORMATOlETRAS = {
    'N': "Nombre del experimento",
    'F': "Fecha del experimento",
    'T': "Tipo de experimento",
    'R': "Resultados del experimento"
}

# Función para borrar la consola dependiendo del sistema operativo
def borrarConsola():
    if platform.system() == "Windows":
        os.system('cls')  # Si es Windows, usar 'cls' para limpiar la consola
    else:
        os.system('clear')  # Si es Linux/Mac, usar 'clear' para limpiar la consola

# Clase para almacenar y gestionar los datos de usuarios y experimentos
class Datos:
    def __init__(self):
        self.experimentos = []  # Lista para almacenar los experimentos
        self.usuarios = {  # Diccionario para almacenar los usuarios registrados
            "EdIv": {
                "contraseña": self.hash_password("Ediv-7*"),  # Contraseña hasheada
                "telefono": "3122003538",
                "correo": "ediv@example.com"
            }
        }

    # Función para validar un correo electrónico con expresión regular
    def validar_correo(self, correo):
        return bool(re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', correo))

    # Agregar un nuevo experimento a la lista
    def agregar_experimento(self, experimento):
        self.experimentos.append(experimento)

    # Agregar un nuevo usuario con sus datos: usuario, contraseña, teléfono y correo
    def agregar_usuario(self, usuario, contraseña, telefono, correo):
        self.usuarios[usuario] = {"contraseña": contraseña, "telefono": telefono, "correo": correo}

    # Obtener la lista de experimentos
    def obtener_experimentos(self):
        return self.experimentos

    # Obtener la lista de usuarios
    def obtener_usuarios(self):
        return self.usuarios

    # Método para visualizar todos los experimentos registrados
    def ver_experimentos(self):
        for experimento in self.experimentos:
            experimento.ver_experimento()

    # Método para visualizar todos los usuarios registrados
    def ver_usuarios(self):
        for usuario, datos in self.usuarios.items():
            print(f"Usuario: {usuario}, Correo: {datos['correo']}, Teléfono: {datos['telefono']}")

    # Función para encriptar contraseñas usando bcrypt
    def hash_password(self, password):
        salt = bcrypt.gensalt()  # Genera un 'salt' aleatorio para la encriptación
        hashed = bcrypt.hashpw(password.encode(), salt)  # Hashea la contraseña con el salt
        return hashed

    # Función para verificar si una contraseña ingresada coincide con una contraseña hasheada
    def check_password(self, hashed, password):
        return bcrypt.checkpw(password.encode(), hashed)

    # Guardar usuarios y experimentos en un archivo de texto
    def guardar(self):
        if len(self.usuarios) == 0 and len(self.experimentos) == 0:
            return  # Si no hay datos, no guardamos nada
        
        text = ""  # Inicializamos la variable que almacenará la información
        
        # Escribimos los datos de los usuarios en el archivo
        if len(self.usuarios) > 0:
            for i, usuario in self.usuarios.items():
                text += f"\n{usuario['correo']}\n~{usuario['contraseña']}\n~{usuario['telefono']}"
                if i != len(self.usuarios) - 1:
                    text += "\n----"  # Separador entre usuarios
        else:
            text += "usuario~\n0000"
        
        # Escribimos los experimentos si existen
        if len(self.experimentos) > 0:
            text += "\n####"
            for i, experimento in enumerate(self.experimentos):
                text += f"\n{experimento.nombre}\n~{experimento.fecha}\n~{experimento.tipo}\n~{str(experimento.resultados)}"
                if i != len(self.experimentos) - 1:
                    text += "\n----"
        
        # Guardamos la información en el archivo 'datos.txt'
        with open("datos.txt", "w") as archivo:
            archivo.write(text)
        print("Datos guardados correctamente.")  # Confirmación de que los datos fueron guardados

    # Limpiar la lista de experimentos y guardar los cambios
    def clear(self):
        self.experimentos = []  # Limpiar la lista de experimentos
        self.guardar()  # Guardar los cambios (sin experimentos) en el archivo

# Clase que maneja las operaciones del sistema de usuarios
class SistemaDeUsuarios:
    def __init__(self, datos):
        self.datos = datos  # Recibe una instancia de la clase Datos

    # Registro de un nuevo usuario
    def registrar_usuario(self):
        print("\n--- Registro de Usuario ---")
        usuario = input("Ingrese un nombre de usuario: ")
        
        # Validación de nombre de usuario con formato
        if not self.datos.validar_nombre_usuario(usuario):
            print("El nombre de usuario debe contener mayúsculas al comienzo y después de cada espacio.")
            return

        correo = input("Ingrese su correo electrónico: ")
        
        # Validación de formato de correo
        if not self.datos.validar_correo(correo):
            print("El correo electrónico no tiene un formato válido.")
            return

        telefono = input("Ingrese su número de teléfono (10 dígitos): ")
        
        # Validación de número de teléfono
        if not self.datos.validar_telefono(telefono):
            print("El número de teléfono debe tener 10 dígitos.")
            return

        contraseña = getpass.getpass("Ingrese una contraseña: ")
        
        # Validación de contraseña (debe cumplir con ciertos requisitos)
        if not self.datos.validar_contraseña(contraseña):
            print("La contraseña debe tener al menos una mayúscula, una minúscula, números y al menos un carácter especial (*_-).")
            return

        hashed_contraseña = self.datos.hash_password(contraseña)  # Hasheamos la contraseña
        self.datos.agregar_usuario(usuario, hashed_contraseña, telefono, correo)  # Registramos el usuario
        print("Usuario registrado exitosamente.")

    # Iniciar sesión de un usuario
    def iniciar_sesion(self):
        if not self.datos.obtener_usuarios():
            print("No hay usuarios registrados. Por favor, registre un usuario primero.")
            return False

        print("\n--- Inicio de Sesión ---")
        login_input = input("Ingrese su usuario o correo electrónico: ")
        contraseña = getpass.getpass("Contraseña: ")

        # Verificamos si el login corresponde a un usuario o correo
        usuario_data = None
        for usuario, datos in self.datos.obtener_usuarios().items():
            if usuario == login_input or datos['correo'] == login_input:
                usuario_data = datos
                break

        if usuario_data and self.datos.check_password(usuario_data["contraseña"], contraseña):  # Verificación de contraseña
            print("Inicio de sesión exitoso.")
            return True
        else:
            print("Usuario o correo electrónico, o contraseña incorrectos.")
            return False

    # Menú de inicio de sesión
    def menu_login(self):
        while True:
            print(MENU_LOGIN)
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                self.registrar_usuario()  # Registrar un nuevo usuario
            elif opcion == '2':
                if self.iniciar_sesion():  # Iniciar sesión si los datos son correctos
                    return True
            elif opcion == '3':
                print("Saliendo...")
                return False  # Salir del programa
            else:
                print("Opción inválida. Intente de nuevo.")  # Manejo de opciones inválidas

# Menú principal (Lógica de interacción con el usuario una vez que haya iniciado sesión)
def menu_principal(self):
    while True:
        borrarConsola()  # Limpiar la consola
        print(MENU_PRINCIPAL)  # Mostrar el menú principal
        opcion = input("Seleccione una opción: ")

        # Dependiendo de la opción, ejecutamos la acción correspondiente
        if opcion == '1':
            self.agregar_experimento()
        elif opcion == '2':
            self.ver_experimentos()
        elif opcion == '3':
            self.analisis_de_resultados()
        elif opcion == '4':
            self.generar_informe()
        elif opcion == '5':
            self.configuracion()
        elif opcion == '6':
            print("Cerrando sesión...")
            return  # Salir de la sesión
        elif opcion == '7':
            print("Saliendo...")
            exit()  # Salir del programa
        else:
            print("Opción inválida. Intente de nuevo.")  # Manejo de opciones inválid