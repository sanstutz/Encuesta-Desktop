from datetime import date
from entities.materia import Materia


class Encuesta:
    def __init__(self, id: int, nombre: str, fecha_inicio: date, fecha_fin: date):
        self.id = id
        self.nombre = nombre
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.materias = []
        self.form_url = None

    def añadir_materia(self, materia):
        self.materias.append(materia)

    def añadir_materia_en_orden(self, materia, orden: int):
        if (orden >= 0 and orden <= len(self.materias)):
            self.materias.insert(orden, materia)
        else:
            self.añadir_materia(materia)

    def obtener_materia_por_indice(self, indice: int) -> Materia:
        if (indice >= 0 and indice < len(self.materias)):
            return self.materias[indice]
        else:
            raise IndexError("Índice de materia fuera de rango")

    def intercambiar_materias(self, indice1: int, indice2: int):
        if (indice1 >= 0 and indice1 < len(self.materias) and indice2 >= 0 and indice2 < len(self.materias)):
            self.materias[indice1], self.materias[indice2] = self.materias[indice2], self.materias[indice1]
        else:
            raise IndexError("Índice de materia fuera de rango")
        
    def eliminar_materia_por_indice(self, indice: int):
        if (indice >= 0 and indice < len(self.materias)):
            del self.materias[indice]
        else:
            raise IndexError("Índice de materia fuera de rango")

    def __str__(self):
        return f"Encuesta(id={self.id}, nombre='{self.nombre}', fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin}, form_url={self.form_url})"

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha_inicio": self.fecha_inicio.isoformat(),
            "fecha_fin": self.fecha_fin.isoformat(),
            "materias": [
                materia.to_dict()
                for materia in self.materias
            ],
            "form_url": self.form_url,
        }

    @staticmethod
    def from_dict(data):
        encuesta = Encuesta(
            data["id"],
            data["nombre"],
            date.fromisoformat(data["fecha_inicio"]),
            date.fromisoformat(data["fecha_fin"]),
        )
        encuesta.form_url = data.get("form_url")
        encuesta.materias = [Materia.from_dict(materia_data) for materia_data in data.get("materias", [])]
        return encuesta