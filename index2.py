import re
import getpass
import bcrypt
from datetime import datetime
import os
import platform

# Constantes utiles
SELECT = "Seleccione una opcion: "
BAD_OPTION = "Opcion incorrecta"
BAD_INFO_REQUEST = "! Datos ingresados no validos"
WRITE_U_RESPONSE = "Escriba su respuesta: "
BARSPACE = "--------------------"
RETURN_TO_MENU = "Volver al menu principal"
FORMATO_LETRAS = {
    'N': "Nombre del experimento",
    'F': "Fecha del experimento",
    'T': "Tipo de experimento",
    'R': "Resultados del experimento"
}
SI_NO_OPTION = """
    1. Si
    2. No
"""

# Definición de los menús, que se usan más adelante en las funciones principales.
MENU_LOGIN = """
--- Menú de Login ---
1. Registrarse
2. Iniciar Sesión
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

MENU_VER_EXPERIMENTOS = """
--- Menú Ver Experimentos ---
1. Ver Todos los Experimentos
2. Buscar Experimento
3. Ordenar Experimentos
4. Filtrar por Tipo de Experimento
5. Volver al Menú Principal
"""

GENERAR_INFORME = """
--- Generar Informe ---
1. Exportar informe
2. Previsualizacion del informe
3. Seleccionar experimentos para informe
4. Volver al Menú Principal
"""

MENU_ANALIZAR_RESULTADOS = """
    --- Analizar resultados ---
    1. Calcular promedio
    2. Calcular maximo
    3. Calcular minimo
    4. Seleccionar experimentos
    5. Volver al menu principal
"""

# Función para limpiar consola
def borrarConsola():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Función para verificar entradas flotantes
def isFloat (string):
    try:
        return float(string)
    except:
        return False

# Clase donde almacenamos los datos
class Datos:
    
    usuarios = []
    experimentos = []
    usuario = None

    def obtenerUsuario(self):
        if self.usuario is not None:
            return self.usuarios[self.usuario]
    
    def validar_fecha(self, fecha):
        try:
            return datetime.strptime(fecha, '%Y-%m-%d')
        except:
            return False

    def agregarUsuario(self, correo: str, clave: str, telefono: str, nombre: str, apellido: str):
        usuario = {
            'correo': correo,
            'clave': clave,
            'telefono': telefono,
            'nombre': nombre,
            'apellido': apellido
        }
        self.usuarios.append(usuario)
        print("*** Usuario agregado con exito ***")
        return usuario
    
    @staticmethod
    def verificarEmail(email):
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None

    # Método para guardar los datos
    def guardar(self): 
        if len(self.usuarios) == 0 and len(self.experimentos) == 0:
            return
        
        # Definimos la variable text como una cadena vacía para modificarla posteriormente
        text = ""
        
        # Escribimos la información de los usuarios
        if len(self.usuarios) > 0:
            for i in range(len(self.usuarios)):
                usuario = self.usuarios[i]
                text += f"\n{usuario['correo']}\n~{usuario['clave']}\n~{usuario['telefono']}"
                text += f"\n~{usuario['nombre']}\n~{usuario['apellido']}"
                if i < len(self.usuarios)-1:
                    text += "\n----"
        else:
            # Si no hay usuarios se escribe uno por defecto
            text += "usuario~\n0000"
        
        # Solo si hay experimentos se agrega información
        if len(self.experimentos) > 0:
            text += "\n####"
            for i in range(len(self.experimentos)):
                experimento: Experimento = self.experimentos[i]
                text += f"\n{experimento.nombre}\n~{experimento.fecha}\n~{experimento.tipo}\n~{str(experimento.resultados)}"
                if i < len(self.experimentos)-1:
                    text += "\n----"
        
        # Abrimos el archivo donde están los datos
        with open("datos.txt", "w") as datos:
            datos.write(text)
            print("Datos guardados.")
    
    def clear(self):
        self.experimentos = []
        self.guardar()

    def __init__(self) -> None:
        with open("datos.txt", "r") as datos:
            text: str = datos.read()
            text = text.replace("\n", "")
            if text != "":
                tablasContenido = text.split("####")
                usuarios = tablasContenido[0].split("----")
                for i in range(len(usuarios)):
                    usuario_list = usuarios[i].split("~")
                    usuario = {
                        'correo': usuario_list[0],
                        'clave': usuario_list[1],
                        'telefono': usuario_list[2],
                        'nombre': usuario_list[3],
                        'apellido': usuario_list[4]
                    }
                    if usuario['correo'] != "usuario":
                        self.usuarios.append(usuario)
                
                if len(tablasContenido) > 1:
                    experimentos = tablasContenido[1].split("----")
                    for i in range(len(experimentos)):
                        experimento_list = experimentos[i].split("~")
                        experimento = Experimento(experimento_list[0], experimento_list[1], experimento_list[2])
                        experimento.resultados = eval(experimento_list[3])
                        self.experimentos.append(experimento)

# Clase para manejar los experimentos
class Experimento:
    resultados: list[float] = []

    def promedio(self):
        return sum(self.resultados) / len(self.resultados)

    def minimo(self):
        return min(self.resultados)

    def maximo(self):
        return max(self.resultados)
    
    def __init__(self, nombre, fecha, tipo, resultados = []):
        self.nombre = nombre
        self.fecha = fecha
        self.tipo = tipo
        self.resultados = resultados

# Clase que maneja las operaciones del sistema de usuarios
class SistemaDeUsuarios:
    def __init__(self, datos):
        self.datos = datos  # Recibe una instancia de la clase Datos

    def registrarUsuario(self):
        # Código de registro...
        pass

    def iniciarSesion(self):
        print("\n--- Iniciar Sesión ---")
        login_input = input("Ingrese su nombre de usuario o correo electrónico: ")
        contraseña = getpass.getpass("Contraseña: ")

        # Buscar si el login_input es un nombre de usuario o un correo
        usuario_data = None
        
        # Verificar si el input es un correo electrónico
        if Datos.verificarEmail(login_input):  # Si es un correo
            usuario_data = next((u for u in self.datos.usuarios if u['correo'] == login_input), None)
        else:  # Si no es un correo, asumimos que es un nombre de usuario
            usuario_data = next((u for u in self.datos.usuarios if u['nombre'] == login_input), None)
        
        # Verificar si el usuario existe y la contraseña es correcta
        if usuario_data and bcrypt.checkpw(contraseña.encode('utf-8'), usuario_data['clave'].encode('utf-8')):
            print("Inicio de sesión exitoso.")
            self.datos.usuario = self.datos.usuarios.index(usuario_data)  # Guardamos el índice del usuario
            return True
        else:
            print("Nombre de usuario/correo o contraseña incorrectos.")
            return False

    def cerrarSesion(self):
        """Cerrar sesión del usuario actual y guardar los datos."""
        if self.datos.usuario is not None:
            # Limpiar la sesión actual
            usuario = self.datos.obtenerUsuario()
            print(f"Adiós, {usuario['nombre']} {usuario['apellido']}.")
            self.datos.usuario = None  # El usuario se establece como None
            self.datos.guardar()  # Guardamos los datos antes de cerrar sesión
            print("Datos guardados correctamente.")
            return True
        else:
            print("No hay sesión activa.")
            return False

    def menuLogin(self):
        while True:
            print(MENU_LOGIN)
            opcion = input(SELECT)

            if opcion == '1':
                self.registrarUsuario()  # Registrar un nuevo usuario
            elif opcion == '2':
                if self.iniciarSesion():  # Iniciar sesión si los datos son correctos
                    return True
            elif opcion == '3':
                print("Saliendo...")
                return False  # Salir del programa
            else:
                print(BAD_OPTION)  # Manejo de opciones inválidas

# Función de menú principal
def main(data: Datos):
    sistema = SistemaDeUsuarios(data)  # Crear la instancia de SistemaDeUsuarios

    while True:
        borrarConsola()
        if data.usuario is not None:
            usuario = data.obtenerUsuario()
            print(BARSPACE)
            print(f"Hola, {usuario['nombre']} {usuario['apellido']}")  # Saludo al usuario
        else:
            print(BARSPACE)

        print(MENU_PRINCIPAL)
        opcion = input(SELECT)

        if opcion == "1":
            # Agregar un nuevo experimento
            agregarExperimento(data)
            pass
        elif opcion == "2":
            verExperimentos(data)  # Ver experimentos
        elif opcion == "3":
            # Análisis de resultados
            analizisResultados(data)
            pass
        elif opcion == "4":
            # Generar informe
            generarInforme(data)
            pass
        elif opcion == "5":
            # Configuración
            configuracion(data)
            pass
        elif opcion == "6":
            # Cerrar sesión
            if data.usuario is not None:
                if sistema.cerrarSesion():  # Llamamos a la función cerrarSesion
                    print("Sesión cerrada con éxito.")
                    input("Presione enter para continuar...")
            else:
                print("No hay sesión activa.")
                input("Presione enter para continuar...")
        elif opcion == "7":
            print("Saliendo del programa...")
            data.guardar()  # Guardamos los datos antes de salir
            break
        else:
            print(BAD_OPTION)

# Funciones para la interaccion del usuario con el asistente de experimentos

# Opcion 1
def agregarExperimento(datos: Datos):
    borrarConsola()
    nombre = input("Ingrese el nombre del experimento: ")
    tipo = input("Ingrese el tipo de experimento: ")
    fecha = ""
    resultados = []

    while True:
        print("¿Ya realizó el experimento? (si/no)")
        confirm_Realiz_Experimento = input().strip().lower()
        if confirm_Realiz_Experimento == "si":
            fecha_str = input("Ingrese la fecha en que realizó el experimento (YYYY-MM-DD): ")
            fecha = datos.validar_fecha(fecha_str)
            if not fecha:
                print("Fecha inválida. Intente de nuevo.")
                continue
            datos_resultados = int(input("¿Cuántos datos desea almacenar en los resultados? "))
            for i in range(datos_resultados):
                dato_resultado = input(f"Ingrese el resultado {i + 1}: ")
                flotante = isFloat(dato_resultado)
                if flotante != False:
                    resultados.append(flotante)
            break
        elif confirm_Realiz_Experimento == "no":
            fecha = input("Ingrese la fecha en que realizará su experimento (YYYY-MM-DD): ")
            if not datos.validar_fecha(fecha):
                print("Fecha inválida. Intente de nuevo.")
                continue
            break
        else:
            print("Solo puede escoger: si o no")

    experimento = Experimento(nombre, fecha, tipo, resultados)
    datos.experimentos.append(experimento)
    print("Experimento agregado exitosamente.")

# Opcion 2
# Función para ver los experimentos
def verExperimentos(data: Datos):
    while True:
        borrarConsola()
        print(MENU_VER_EXPERIMENTOS)
        opcion = input(SELECT)

        if opcion == "1":
            print("\n--- Todos los Experimentos ---")
            for exp in data.experimentos:
                print(f"{exp.nombre} - {exp.fecha} - {exp.tipo}")
            input("Presione enter para continuar...")
        elif opcion == "2":
            nombre = input("Ingrese el nombre del experimento a buscar: ")
            encontrado = False
            for exp in data.experimentos:
                if nombre.lower() in exp.nombre.lower():
                    print(f"{exp.nombre} - {exp.fecha} - {exp.tipo}")
                    encontrado = True
            if not encontrado:
                print("No se encontró el experimento.")
            input("Presione enter para continuar...")
        elif opcion == "3":
            print("\n--- Ordenar Experimentos ---")
            data.experimentos.sort(key=lambda x: x.fecha)  # Ordenar por fecha
            print("Experimentos ordenados por fecha.")
            input("Presione enter para continuar...")
        elif opcion == "4":
            tipo = input("Ingrese el tipo de experimento para filtrar: ")
            encontrados = [exp for exp in data.experimentos if tipo.lower() in exp.tipo.lower()]
            if encontrados:
                for exp in encontrados:
                    print(f"{exp.nombre} - {exp.fecha} - {exp.tipo}")
            else:
                print("No se encontraron experimentos de ese tipo.")
            input("Presione enter para continuar...")
        elif opcion == "5":
            return  # Volver al menú principal
        else:
            print(BAD_OPTION)

# Opcion 3
def analizisResultados (experimentos: list[Experimento]):
    # variables
    listaExperimentosAnalizar: list[Experimento] = []
    
    def verificacionExperimentos ():
        print("¿Desea analizar todos los experimentos?")
        print(SI_NO_OPTION)
        respuesta = input("")
        if respuesta == "si" or respuesta == "1" or respuesta == "Si" or respuesta == "SI":
            for i in range(len(experimentos)):
                listaExperimentosAnalizar.append(experimentos[i])
        else:
            print("Seleccione los experimentos que desea agregar al analisis")
            mostrarExperimentos(experimentos)
            isBreak = False
            while not isBreak:
                respuestaExperimento = input("")
                if not respuestaExperimento.isnumeric():
                    print(BAD_OPTION)
                    continue
                respuestaExperimento = int(respuestaExperimento)
                experimentoSeleccionado = experimentos[respuestaExperimento]
                if not experimentoSeleccionado in listaExperimentosAnalizar:
                    listaExperimentosAnalizar.append(experimentoSeleccionado)
                else:
                    print("El experimento seleccionado ya esta en la lista para analizar")
                    continue
                print("Experimento agregado, ¿desea agregar otro?")
                print(SI_NO_OPTION)
                respuesta = input("")
                if respuesta == "no" or respuesta == "2" or respuesta == "No" or respuesta == "NO":
                    isBreak = True
            borrarConsola()

    borrarConsola()
    while True:
        print(MENU_ANALIZAR_RESULTADOS)
        respuesta = input(SELECT)

        if respuesta == "1":
            if len(listaExperimentosAnalizar) == 0:
                verificacionExperimentos()
                pass
            calcularPromedio(listaExperimentosAnalizar)   
        elif respuesta == "2":
            if len(listaExperimentosAnalizar) == 0:
                verificacionExperimentos()
            calcularMaximo(listaExperimentosAnalizar)
        elif respuesta == "3":
            if len(listaExperimentosAnalizar) == 0:
                verificacionExperimentos()
            calcularMinimo(listaExperimentosAnalizar)
        elif respuesta == "4":
            verificacionExperimentos()
        elif respuesta == "5":
            break
        else:
            print(BAD_OPTION)
    pass

# Funciones para la opcion de analizis de resultados
def calcularPromedio (experimentos: list[Experimento]):
    resultado = 0
    for i, experimento in enumerate(experimentos):
        resultado += experimento.promedio()
    
    resultado /= len(experimentos)
    print(f"El promedio de los experimentos analizados es: {resultado}")
    pass

def calcularMaximo (experimentos: list[Experimento]):
    resultado = 0
    indexResultado = 0
    for i, experimento in enumerate(experimentos):
        maximo = experimento.maximo()
        if resultado < maximo:
            resultado = maximo
            indexResultado = i
    print(f"El numero maximo de los resultados entre los experimentos analizados es {resultado} del experimento {experimentos[indexResultado].nombre}")

def calcularMinimo (experimentos: list[Experimento]):
    resultado = 0
    indexResultado = 0
    for i, experimento in enumerate(experimentos):
        minimo = experimento.minimo()
        if resultado > minimo or resultado == 0:
            resultado = minimo
            indexResultado = i
    print(f"El numero minimo de los resultados entre los experimentos analizados es {resultado} del experimento {experimentos[indexResultado].nombre}")


# Opcion 4
def generarInforme (datos: Datos):
    # esta variable esta definida fuera del while para que las diferentes ciclos de este no la alteren
    # Es basicamente la lista que controla que experimentos iran en el informe si esta vacia todos los experimentos
    # seran incluidos
    borrarConsola()
    paraInforme = []
    while True:
        print(BARSPACE)
        print(GENERAR_INFORME)
        print(BARSPACE)
        response = input(SELECT)
        if response == "1":
            informe = obtenerInforme(paraInforme, datos)
            exportarInforme(informe, datos.obtenerUsuario())
        elif response == "2":
            print(obtenerInforme(paraInforme, datos))
        elif response == "3":
            print("Seleccione los experimentos que va a incluir en el informe")
            print("0. Seleccionar todos")
            mostrarExperimentos(datos.experimentos)
            isBreak = False
            while not isBreak:
                select = input(SELECT)
                if not select.isnumeric():
                    print("Escriba un numero")
                    continue
                select = int(select)
                if select > 0: 
                    paraInforme.append(select-1)
                    print("¿Desea ingresar otro experimento?")
                    print("1. Si")
                    print("2. No")
                    respuesta = input()
                    if respuesta == "2" or respuesta == "No" or respuesta == "NO" or respuesta == "no":
                        isBreak = True
                else:
                    paraInforme = []
                    isBreak = True
        elif response == "4":
            break
        else:
            print(BAD_OPTION)

# Funiones para la opcion de generar informe
def obtenerInforme (indexs: list[int], datos: Datos):
    # declaramos esta variable que va a almacenar todos los experimentos que seran detallados en el informe
    paraInforme: list[Experimento] = []
    experimentos = datos.experimentos
    formatoInforme: str = datos.obtenerUsuario()["formatoArchivo"]
    if formatoInforme == "":
        formatoInforme = "N-T-F-R"

    if formatoInforme:
        formatoInforme = formatoInforme.split("-")
    informe = "Informe de experimentos \n \n"
    if len(indexs) == 0:
        # si no hay elementos en indexs significa que sera de todos los experimentos
        paraInforme = experimentos
    else:
        # en caso de que si haya elementos en index significa que si habra una discriminacion de experimentos
        for i, index in enumerate(indexs):
            experimento = experimentos[index]
            paraInforme.append(experimento)
    
    for i, experimento in enumerate(paraInforme):
        informe += f"\n \nExperimento numero {i+1} \n"
        resultados = "|"
        for h in range(len(experimento.resultados)):
            resultados += str(experimento.resultados[h]) + "|"
        for j in range(len(formatoInforme)):
            seccion = formatoInforme[j]
            if seccion == "N":
                informe += f"Nombre: {experimento.nombre} \n"
            if seccion == "F":
                informe += f"Fecha de realizacion: {experimento.fecha} \n"
            if seccion == "T":
                informe += f"Tipo: {experimento.tipo} \n"
            if seccion == "R":
                informe += f"Resultados: \n {resultados}"
    return informe
        
def exportarInforme (informe, usuario):
    nombreArchivo = usuario['nombreArchivo']
    if nombreArchivo == "":
        nombreArchivo = usuario['nombre'] + " " + usuario['telefono'] + ".txt"
    with open(nombreArchivo, "w") as archivo:
        archivo.write(informe)
        print("* Informe guardado con exito *")

def mostrarExperimentos (experimentos: list[Experimento]):
    for i, experimento in enumerate(experimentos):
        print(f"{i+1}. {experimento.nombre} - {experimento.tipo}")
    pass

# Opcion 5
def configuracion (usuario, datos: Datos):
    borrarConsola()
    def optionExport ():
        nombrePorDefecto = usuario['nombreArchivo']
        formatoPorDefecto = usuario['formatoArchivo']
        if nombrePorDefecto == "":
            nombrePorDefecto = usuario['nombre'] + " " + usuario['telefono']
        if formatoPorDefecto == "":
            formatoPorDefecto = "N-F-T-R"
        formato_split = formatoPorDefecto.split("-")
        print(".: Configuracion de exportacion :.")
        print(f"Nombre de archivo de exportacion: {nombrePorDefecto}")
        print("Formato de exportacion, (orden de la informacion): ")
        for i in range(len(formato_split)):
            letra = formato_split[i]
            print(f"{i+1}. {FORMATO_LETRAS[letra]}")

        print("Escriba el nombre de exportacion de su archivo, si no desea cambiarlo precione enter sin escribir nada")
        respuesta = input()
        if respuesta != "":
            usuario['nombreArchivo'] = respuesta
        while True:
            print("¿Desea cambiar el orden del formato?")
            print("1. Si")
            print("2. No")
            respuesta = input(SELECT)
            if respuesta == "1" or respuesta == "si" or respuesta == "Si" or respuesta == "SI":
                print("Escriba el orden en que quiera que se ordenen los datos en el informe, separados por guiones")
                print("Ejemplo: 2-1-4-3")
                print(f"1. {FORMATO_LETRAS['N']}")
                print(f"2. {FORMATO_LETRAS['T']}")
                print(f"3. {FORMATO_LETRAS['F']}")
                print(f"4. {FORMATO_LETRAS['R']}")
                while True:
                    response = input(SELECT)
                    try:
                        # esta variable es para almacenar el formato del informe
                        fl = list(map(int, response.split("-")))
                        formato = f"{fl[0]}-{fl[1]}-{fl[2]}-{fl[3]}"
                        formato = formato.replace("1", "N")
                        formato = formato.replace("2", "T")
                        formato = formato.replace("3", "F")
                        formato = formato.replace("4", "R")
                        usuario['formatoArchivo'] = formato
                        break
                    except ValueError:
                        print(BAD_INFO_REQUEST)
                    
            elif respuesta == "2" or respuesta == "no" or respuesta == "No" or respuesta == "NO":
                break
            else:
                print(BAD_OPTION)
        return

    def optionSecure ():
        print("Por favor ingrese la contraseña para poder cambiarla (De enter sin escribir nada para cancelar)")
        response = input(WRITE_U_RESPONSE)
        if response == "":
            return
        if response == usuario['clave']:
            print("Escriba la nueva contraseña")
            nuevaClave = input(WRITE_U_RESPONSE)
            usuario['clave'] = nuevaClave
            print("** Contraseña cambiada con exito **")
                
    def dataBaseRestore ():
        print("¿Esta seguro de borrar la base de datos?")
        print("1. Si")
        print("2. No")
        response = input(SELECT)
        if response == "1" or response == "Si" or response == "si" or response == "SI":
            datos.clear()
        return
            
    def viewUserData ():
        print(BARSPACE)
        print("Informacion de perfil")
        print(f"Nombre de usuario: {usuario['nombre']} {usuario['apellido']}")
        print(f"Correo: {usuario['correo']}")
        print(f"Numero de telefono: {usuario['telefono']}")
        print(BARSPACE)
    while True:
        print("\n"+BARSPACE)
        print("** Menu de configuracion **")
        print("1. Opciones de exportacion")
        print("2. Opciones de seguridad")
        print("3. Restablecer base de datos")
        print("4. Ver datos de usuario")
        print("5. "+RETURN_TO_MENU)
        print(BARSPACE)
        respuesta = input(SELECT)
        if respuesta == "1":
            optionExport()
        elif respuesta == "2":
            optionSecure()
        elif respuesta == "3":
            dataBaseRestore()
        elif respuesta == "4":
            viewUserData()
        elif respuesta == "5":
            break
        else:
            print(BAD_OPTION)
    
    return




