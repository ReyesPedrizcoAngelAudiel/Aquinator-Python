import json
from ruamel.yaml import YAML
import os                                                                                       # Para verificar si existe el archivo y sino crearlo

yaml = YAML()

with open("preguntas.yaml", "r") as archivo_preguntas:                                       # Cargar las preguntas desde el archivo YAML
    preguntas = yaml.load(archivo_preguntas)["Preguntas"]
with open("emojis.yaml", "r", encoding="utf-8") as archivo_animales_emojis:                  # Cargar los emojis de animales desde el archivo YAML
    animales_emojis = yaml.load(archivo_animales_emojis)["Animales"]

emojis = {animal["nombre"]: animal["emoji"] for animal in animales_emojis}                      # Convertir la lista de animales a un diccionario para facilitar la búsqueda por nombre

if not os.path.exists("animales.json"):                                                      # Verificar si existe el archivo animales.json
    animales_vacios = {"Animales": []}                                                          # Si no existe, lo crea con una estructura vacía
    with open("animales.json", "w") as archivo_animales:
        json.dump(animales_vacios, archivo_animales, indent=2)

with open("animales.json", "r") as archivo_animales:                                         # Cargar los animales del archivo JSON
    animales = json.load(archivo_animales)["Animales"]

def filtrar_animales(animales, propiedad, respuesta):                                           # Función para filtrar los animales en base a la respuesta del usuario
    if respuesta.upper() == 'S':
        return [animal for animal in animales if animal[propiedad] == True]
    elif respuesta.upper() == 'N':
        return [animal for animal in animales if animal[propiedad] == False]
    return animales

def obtener_respuesta_valida(pregunta):                                                         # Función para obtener una respuesta válida (S/N)
    while True:
        respuesta = input(pregunta + " (S/N): ").upper()
        if respuesta in ['S', 'N']:
            return respuesta
        else:
            print("🚫 Opción no válida 🚫. Por favor, ingresa 'S' o 'N'.")

def agregar_animal(respuestas_anteriores):                                                      # Función para añadir un nuevo animal
    nuevo_animal = {}
    nombre_animal = input("\n¿Cuál es el nombre del animal?: ").lower()
    
    emoji_animal = emojis.get(nombre_animal, "")                                                # Buscar el emoji correspondiente al nombre del animal | Si no existe, devuelve un vacío
    nuevo_animal["Nombre"] = f"{nombre_animal} {emoji_animal}"                                  # Nombre del animal con el emoji
    
    calificacion = 0
    
    for pregunta in preguntas:                                                                  # Hacer todas las preguntas al usuario y guardar las respuestas
        atributo = pregunta["Atributo"]
        if atributo in respuestas_anteriores:
            respuesta = respuestas_anteriores[atributo]                                         # Usar la respuesta previa
            print(f"{pregunta['Pregunta']} (Respuesta anterior: {respuesta})")
        else:
            respuesta = obtener_respuesta_valida(pregunta["Pregunta"])
            respuestas_anteriores[atributo] = respuesta

        if respuesta == 'S':
            nuevo_animal[pregunta["Atributo"]] = True
            calificacion += pregunta["Valor"]
        else:
            nuevo_animal[pregunta["Atributo"]] = False

    nuevo_animal["Calificacion"] = calificacion

    animales.append(nuevo_animal)                                                               # Añadir el nuevo animal a la lista de animales y guardarlo en el archivo
    with open("animales.json", "w") as archivo_animales:
        json.dump({"Animales": animales}, archivo_animales, indent=2)
    print(f"\nAnimal: {nombre_animal} {emoji_animal} agregado.")

def descartar_animales(posibles_animales, respuestas_anteriores):                               # Función para descartar animales individualmente
    while len(posibles_animales) > 1:                                                           # Sigue preguntando mientras haya más de un animal
        for animal in posibles_animales[:]:                                                     # Copia de la lista para evitar problemas al modificarla
            respuesta = obtener_respuesta_valida(f"¿Es un {animal['Nombre']}?")
            if respuesta == 'S':
                print(f"\nTu animal es: {animal['Nombre']}")
            else:
                posibles_animales.remove(animal)                                                # Eliminar el animal si la respuesta es 'N'
                break                                                                           # Reiniciar el bucle para ajustar la lista de animales restantes
    
    if len(posibles_animales) == 1:                                                             # Si solo queda un animal después de las eliminaciones
        print(f"\nTu animal es: {posibles_animales[0]['Nombre']}")
        verificar_acierto(posibles_animales[0], respuestas_anteriores)
    else:
        print("No sé cuál es 🥲")

def verificar_acierto(animal, respuestas_anteriores):                                           # Función para verificar si el programa acertó
    respuesta = obtener_respuesta_valida("\n¿Adiviné tu animal?")
    if respuesta == 'N':
        print("¡Vaya! No acerté 🫠. Vamos a agregar tu animal.")
        agregar_animal(respuestas_anteriores)

def seleccionar_animal():                                                                       # Función principal del juego de preguntas
    respuestas_anteriores = {}
    posibles_animales = animales[:]                                                             # Lista de posibles animales
    if len(posibles_animales) < 3:
        print("\n        🤖 Hagamos más divertido el juego 🤖          ")
        print("                 Agrega más animales                   \n")
        return
    
    for pregunta in preguntas:
        if len(posibles_animales) == 1: break                                                   # Si solo queda un animal, terminamos

        propiedad = pregunta["Atributo"]
        texto_pregunta = pregunta["Pregunta"]

        si_respuestas = sum(1 for animal in posibles_animales if animal[propiedad] == True)     # Contamos cuántos animales responden "S" o "N"
        no_respuestas = len(posibles_animales) - si_respuestas

        if si_respuestas == 0 or no_respuestas == 0:                                            # Si todos los animales responden igual, no tiene sentido hacer la pregunta
            respuestas_anteriores[propiedad] = 'S' if si_respuestas > 0 else 'N'
            continue

        if propiedad in respuestas_anteriores:                                                  # Si ya tenemos la respuesta de una pregunta anterior
            respuesta = respuestas_anteriores[propiedad]
            print(f"{texto_pregunta} (Respuesta anterior: {respuesta})")
        else:
            respuesta = obtener_respuesta_valida(texto_pregunta)
            respuestas_anteriores[propiedad] = respuesta

        posibles_animales = filtrar_animales(posibles_animales, propiedad, respuesta)           # Filtramos la lista de animales en base a la respuesta

    if len(posibles_animales) == 1:                                                             # Si no se identificó el animal
        print(f"\nTu animal es: {posibles_animales[0]['Nombre']}")
        verificar_acierto(posibles_animales[0], respuestas_anteriores)
    else:
        descartar_animales(posibles_animales, respuestas_anteriores)

def menu_principal():                                                                           # Menú principal
    while True:
        print("------------------------------------------------------")
        print("                 ✨  BIENVENIDO  ✨                  ")
        print("------------------------------------------------------")
        print("Selecciona una opción:")
        print("1. Trataré de adivinar en qué animal estás pensando 🤔")
        print("2. Añadir un nuevo animal (ej: conejo)")
        print("3. Salir 👋🏼")
        opcion = input("Elige una opción (1/2/3): ")

        if opcion == "1":
            print("------------------------------------------------------")
            seleccionar_animal()
        elif opcion == "2":
            print("------------------------------------------------------")
            agregar_animal({})
        elif opcion == "3":
            print("------------------------------------------------------")
            print("     Gracias por jugar conmigo, ¡hasta luego! 😍     ")
            print("------------------------------------------------------")
            break
        else:
            print("------------------------------------------------------")
            print("              🚫 Opción no válida 🚫                 ")
            print("    No sea imbecil y seleccione una opción correcta.  ")

# Iniciar el programa
menu_principal()