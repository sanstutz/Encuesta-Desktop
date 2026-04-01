from datetime import date


class Encuesta:
    def __init__(self, id: int, nombre: str, fecha_inicio: date, fecha_fin: date):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.materias = []

    def añadir_materia(self, materia):
        self.materias.append(materia)

    def __str__(self):
        return f"Encuesta(id={self.id}, nombre='{self.nombre}', fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin})"