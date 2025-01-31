from ruamel.yaml import YAML
import json

# Estructura de preguntas
Preguntas = {
  "Preguntas": [
    {
      "Pregunta": "Es un animal terrestre?",
      "Atributo": "Terrestre",
      "Valor": 128
    },
    {
      "Pregunta": "Es un animal acuatico?",
      "Atributo": "Acuatico",
      "Valor": 64
    },
    {
      "Pregunta": "Tiene cuatro patas?",
      "Atributo": "Cuadrupedo",
      "Valor": 32
    },
    {
      "Pregunta": "Es oviparo (pone huevos)?",
      "Atributo": "Oviparo",
      "Valor": 16
    },
    {
      "Pregunta": "Es un animal domestico?",
      "Atributo": "Domestico",
      "Valor": 8
    },
    {
      "Pregunta": "Tiene dientes?",
      "Atributo": "Dientes",
      "Valor": 4
    },
    {
      "Pregunta": "Tiene pelo?",
      "Atributo": "Pelo",
      "Valor": 2
    },
    {
      "Pregunta": "Es un animal grande?",
      "Atributo": "Grande",
      "Valor": 1
    }
  ]
}

# Guardar en archivo YAML
yaml = YAML()
with open("E1/preguntas.yaml", "w") as archivo_yaml:
    yaml.dump(Preguntas, archivo_yaml)

# Guardar preguntas en archivo JSON
with open("E1/preguntas.json", "w") as archivo_json:
    json.dump(Preguntas, archivo_json, indent=2)

# Imprimir el contenido para verificar
print(json.dumps(Preguntas, indent=2))
