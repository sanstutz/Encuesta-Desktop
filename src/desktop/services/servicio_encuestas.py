from entities.encuesta import Encuesta
from datetime import date


class ServicioEncuestas:
    def __init__(self):
        self.encuestas = list()

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
        if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
            raise TypeError("Las fechas deben ser de tipo date")
        if (fecha_inicio > fecha_fin):
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha fin")
        id = len(self.encuestas) + 1
        encuesta = Encuesta(id, nombre, fecha_inicio, fecha_fin)
        self.encuestas.append(encuesta)
        return encuesta
    
    def añadir_materia_a_encuesta(self, id_encuesta: int, materia):
        encuesta = self.obtener_encuesta(id_encuesta)
        if (encuesta is not None):
            encuesta.añadir_materia(materia)