import re
from datetime import datetime
# constantes
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

def verificar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None


# Declaramos una clase datos que sera usada por la funcion principal para controlar el archivo donde se guardan los datos
class Experimento:
    resultados: list[float] = []

    def promedio (self):
        result = self.resultados
        suma = 0
        length = len(result)
        for i in range(length):
            suma += result[i]
        return suma / length

    def minimo (self):
        return min(self.resultados)

    def maximo (self):
        return max(self.resultados)
    
    def _init_(self, nombre, fecha, tipo):
        self.nombre = nombre
        self.fecha = fecha
        self.tipo = tipo

class Datos:
    
    usuarios = []
    experimentos = []
    usuario = -1
    
    def iniciarSesion (self, correo, clave):
        usuarios = self.usuarios
        inited = False
        for i in range(len(usuarios)):
            usuario = usuarios[i]
            if usuario['correo'] == correo:
                if usuario['clave'] == clave:
                    self.usuario = i
                    inited = True
        if inited:
            return usuarios[self.usuario]
    
    def obtenerUsuario (self):
        if self.usuario > -1:
            return self.usuarios[self.usuario]
    def validar_fecha (fecha):
        try:
          return datetime.strptime(fecha, '%Y-%m-%d')
        except:
          return False
    def agregarUsuario (self, correo: str, clave: str, nombreArchivo: str, formatoArchivo: str, telefono: str, nombre: str, apellido: str):
        usuario = {
            'correo': correo,
            'clave': clave,
            'nombreArchivo': nombreArchivo,
            'formatoArchivo': formatoArchivo,
            'telefono': telefono,
            'nombre': nombre,
            'apellido': apellido
        }
        self.usuarios.append(usuario)
        print("*** Usuario agregado con exito ***")
        return usuario

    def agregarExperimento(self):
        nombre = input("Ingrese el nombre del experimento: ")
        tipo = input("Ingrese el tipo de experimento: ")
        fecha = ""
        resultados = []

        while True:
            print("¿Ya realizó el experimento? (si/no)")
            confirm_Realiz_Experimento = input().strip().lower()
            if confirm_Realiz_Experimento == "si":
                fecha_str = input("Ingrese la fecha en que realizó el experimento (YYYY-MM-DD): ")
                fecha = self.validar_fecha(fecha_str)
                if not fecha:
                    print("Fecha inválida. Intente de nuevo.")
                    continue
                datos_resultados = int(input("¿Cuántos datos desea almacenar en los resultados? "))
                for i in range(datos_resultados):
                    dato_resultado = input(f"Ingrese el resultado {i + 1}: ")
                    resultados.append(dato_resultado)
                break
            elif confirm_Realiz_Experimento == "no":
                fecha = input("Ingrese la fecha en que realizará su experimento (YYYY-MM-DD): ")
                if not self.validar_fecha(fecha):
                    print("Fecha inválida. Intente de nuevo.")
                    continue
                break
            else:
                print("Solo puede escoger: si o no")

        experimento = Experimento(nombre, fecha, tipo, resultados)
        self.experimentos.append(experimento)
        print("Experimento agregado exitosamente.")
        
    # el metodo guardar nos permite guardar la informacion ya establecida
    def guardar (self): 
        if len(self.usuarios) == 0 and len(self.experimentos) == 0:
            # evitamos que el programa siga en ejecucion si no hay nada que guardar
            return
        
        # definimos la variable text como una cadena vacia para modificarla posteriormente
        text = ""
        #escribimos la informacion de los usuarios
        if len(self.usuarios) > 0:
            for i in range(len(self.usuarios)):
                usuario = self.usuarios[i]
                text += f"\n{usuario['correo']}\n{usuario['clave']}\n{usuario['nombreArchivo']}~\n{usuario['formatoArchivo']}"
                text += f"\n~{usuario['telefono']}\n~{usuario['nombre']}\n~{usuario['apellido']}"
                if i < len(self.usuarios)-1:
                    text += "\n----"
        else:
            #si no hay usuarios se escribe uno por defecto
            text += "usuario~\n0000"
        # solo si hay experimentos se agrega informacion
        if len(self.experimentos) > 0:
            text += "\n####"
            for i in range(len(self.experimentos)):
                experimento = self.experimentos[i]
                text += f"\n{experimento['nombre']}~\n{experimento['fecha']}~\n{experimento['tipo']}~\n{str(experimento['resultados'])}"
                if i < len(self.experimentos)-1:
                    text += "\n----"
        # abrimos el archivo donde estan los datos
        with open("datos.txt", "w") as datos:
            #escribimos la informacion
            datos.write(text)
    
    def clear (self):
        self.experimentos = []
        self.guardar()


# declaramos la funcion iniciadora
    def _init_(self) -> None:
        # abrimos el archivo de datos
        with open("datos.txt", "r") as datos:
            text: str = datos.read()
            text = text.replace("\n", "")
            # solo ejecutamos el codigo si el texto no esta vacio
            if text != "":
                #diferenciamos las tablas de contenido con el separador dispuesto para ellas
                tablasContenido = text.split("####")
                # obtenemos los usuarios como primer item de las tablas de contenido y lo separamos
                usuarios = tablasContenido[0].split("----")
                for i in range(len(usuarios)):
                    # separamos los datos de cada usuario para formatearlo
                    usuario_list = usuarios[i].split("~")
                    usuario = {
                        'correo': usuario_list[0],
                        'clave': usuario_list[1],
                        'nombreArchivo': usuario_list[2],
                        'formatoArchivo': usuario_list[3],
                        'telefono': usuario_list[4],
                        'nombre': usuario_list[5],
                        'apellido': usuario_list[6]
                    }
                    if usuario['correo'] != "usuario":
                        self.usuarios.append(usuario)
                
                if len(tablasContenido) > 1:
                    # hacemos lo mismo con los experimentos
                    experimentos = tablasContenido[1].split("----")
                    for i in range(len(experimentos)):
                        # y lo mismo con experimentos
                        experimento_list = experimentos[i].split("~")
                        experimento = Experimento(experimento_list[0], experimento_list[1], experimento_list[2])
                        experimento.resultados = eval(experimento_list[3])
                        self.experimentos.append(experimento)


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
        informe += f"Experimento numero {i+1} \n"
        resultados = "|"
        for h in range(len(experimento.resultados)):
            resultados += experimento.resultados[h] + "|"
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
        print(f"{i+1}. {experimento.nombre}")
    pass

# funcion para menu principal
def generarInforme (datos: Datos):
    # esta variable esta definida fuera del while para que las diferentes ciclos de este no la alteren
    # Es basicamente la lista que controla que experimentos iran en el informe si esta vacia todos los experimentos
    # seran incluidos
    paraInforme = []
    while True:
        print(BARSPACE)
        print("Generar informe")
        print("1. Exportar informe")
        print("2. Previsualizacion de informe")
        print("3. Seleccionar experimentos para informe")
        print("4. "+RETURNTOMENU)
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
            print(BADOPTION)
                

def configuracion (usuario, datos: Datos):
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
            print(f"{i+1}. {FORMATOlETRAS[letra]}")

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
                print(f"1. {FORMATOlETRAS['N']}")
                print(f"2. {FORMATOlETRAS['T']}")
                print(f"3. {FORMATOlETRAS['F']}")
                print(f"4. {FORMATOlETRAS['R']}")
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
                        print(BADINFOREQUEST)
                    
            elif respuesta == "2" or respuesta == "no" or respuesta == "No" or respuesta == "NO":
                break
            else:
                print(BADOPTION)
        return


    def optionSecure ():
        print("Por favor ingrese la contraseña para poder cambiarla (De enter sin escribir nada para cancelar)")
        response = input(WRITEURESPONSE)
        if response == "":
            return
        if response == usuario['clave']:
            print("Escriba la nueva contraseña")
            nuevaClave = input(WRITEURESPONSE)
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
        print("5. "+RETURNTOMENU)
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
            print(BADOPTION)
    
    return


# ---------------------------------------------------------------
# Procesos

# Función principal para gestionar el acceso de usuarios
def menuUsuario():
    # vamos a abrir la base de datos
    datos = Datos()
    # viejo a partir de ahora todos los print dentro de funciones
    acceso = ['Iniciar sesión', 'Registrarse']
    
    def menuRegistrarse():
        while True:
            print("Ingrese su nombre:")
            nombre = input()
            if not (nombre.isalpha() and len(nombre) > 2):
                continue
            print("Ingrese su apellido:")
            apellido = input()
            if not (apellido.isalpha() and len(apellido) > 2):
                continue
            print("Correo electrónico:")
            correo = input()
            if not verificar_email(correo):
                print(f"{correo} no es un correo electrónico válido.")
                continue
            print("Ingrese una clave:")
            clave = input()
            if 8 <= len(clave) <= 20:
                print("Confirme clave:")
                claveConfirmada = input()
                if clave == claveConfirmada:
                    break
                else:
                    print("Las claves no coinciden.")
            else:
                print("La clave debe tener entre 8 y 20 caracteres.")
            print("Ingrese su número de teléfono:")
            telefono = input()
            if len(telefono) != 10:
                continue
            datos.agregarUsuario(correo, clave, "", "", telefono, nombre, apellido)
            datos.guardar()
            print("Datos guardados exitosamente")
            break

    def menuIniciarSesion():
        if not datos.usuarios:
            print("No hay usuarios registrados")
            return
        print("Ingrese su correo:")
        correo_a_Verificar = input()
        print("Ingrese su clave:")
        clave_a_Verificar = input()
        usuario = datos.iniciarSesion(correo_a_Verificar, clave_a_Verificar)
        if usuario:
            print(f"Bienvenido, {usuario['nombre']}")
            main(datos)
        else:
            print("Correo o clave incorrectos")

    while True:
        print("Bienvenido a nuestro Asistente de Laboratorio")
        print("\nAcceso:")
        for i, opcion_Acceso in enumerate(acceso):
            print(f"{i+1}: {opcion_Acceso}")

        acceso_Seleccionado = int(input())
        if acceso_Seleccionado == 1:
            menuIniciarSesion()
        elif acceso_Seleccionado == 2:
            menuRegistrarse()
        else:
            print("Ingrese una opción válida")

def main (data: Datos):
    while True:
        print("--------------------")
        print("Menu principal")
        print("1. Agregar experimento")
        print("2. Agregar resultados")
        print("3. Editar experimento")
        print("4. Eliminar experimento")
        print("5. Ver experimento")
        print("6. Analisis de resultados")
        print("7. Generar informe")
        print("8. Configuracion")
        print("9. Salir")
        print("--------------------")
        respuesta = input(SELECT)
        if respuesta == "1":
            data.agregarExperimento()
        elif respuesta == "8":
            configuracion(data.obtenerUsuario())
        elif respuesta == "9":
            print("Saliendo del programa...")
            data.guardar()
            break
        else:
            print(BADOPTION)

if __name__ == "__main__":
    menuUsuario()