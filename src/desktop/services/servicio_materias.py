from services.servicio_encuestas import ServicioEncuestas
from entities.materia import Materia

class ServicioMaterias:
    def __init__(self, servicio_encuestas: ServicioEncuestas):
        self.servicio_encuestas = servicio_encuestas

    def obtener_materias_de_encuesta(self, id_encuesta: int) -> list:
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)
        return encuesta.materias
    
    def crear_materia(self, id_encuesta: int, codigo: str, nombre: str, nombre_corto: str, nombre_sin_espacios: str, año: int):
        if (año < 1):
            raise ValueError("El año debe ser mayor a 0")
        materia = Materia(codigo, nombre, nombre_corto, nombre_sin_espacios, año)
        self.servicio_encuestas.añadir_materia_a_encuesta(id_encuesta, materia)
        return materia