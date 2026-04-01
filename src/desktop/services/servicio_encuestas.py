from entities.encuesta import Encuesta
from repositories.repositorio_encuestas import RepositorioEncuestas
from datetime import date


class ServicioEncuestas:
    def __init__(self, repositorio: RepositorioEncuestas):
        self.repositorio = repositorio
        self.encuestas = None
        self.cargar_encuestas()

    def guardar_encuesta(self, encuesta: Encuesta):
        self.repositorio.guardar_encuesta(encuesta)

    def cargar_encuestas(self):
        self.encuestas = self.repositorio.cargar_encuestas()
        return self.encuestas

    def obtener_encuesta(self, id: int) -> Encuesta:
        for encuesta in self.encuestas:
            if (encuesta.id == id):
                return encuesta
        raise Exception(f"No se encontró la encuesta con id {id}")

    def obtener_encuestas(self):
        return self.encuestas
    
    def crear_encuesta(self, nombre: str, fecha_inicio: date, fecha_fin: date):
        if (not nombre):
            raise ValueError("El nombre de la encuesta no puede estar vacío")
        for encuesta in self.encuestas:
            if (encuesta.nombre == nombre):
                raise ValueError("Ya existe una encuesta con ese nombre")
        if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
            raise TypeError("Las fechas deben ser de tipo date")
        if (fecha_inicio > fecha_fin):
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha fin")
        id = len(self.encuestas) + 1
        encuesta = Encuesta(id, nombre, fecha_inicio, fecha_fin)
        self.encuestas.append(encuesta)
        self.repositorio.guardar_encuesta(encuesta)
        return encuesta
