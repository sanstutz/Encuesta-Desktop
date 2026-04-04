from entities.encuesta import Encuesta
from entities.especialidad import Especialidad
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

    def editar_encuesta(self, id: int, nombre: str, fecha_inicio: date, fecha_fin: date):
        encuesta = self.obtener_encuesta(id)
        if (not nombre):
            raise ValueError("El nombre de la encuesta no puede estar vacío")
        for e in self.encuestas:
            if (e.nombre == nombre and e.id != id):
                raise ValueError("Ya existe una encuesta con ese nombre")
        if not isinstance(fecha_inicio, date) or not isinstance(fecha_fin, date):
            raise TypeError("Las fechas deben ser de tipo date")
        if (fecha_inicio > fecha_fin):
            raise ValueError("La fecha de inicio no puede ser mayor que la fecha fin")
        encuesta.nombre = nombre
        encuesta.fecha_inicio = fecha_inicio
        encuesta.fecha_fin = fecha_fin
        self.repositorio.guardar_encuesta(encuesta)

    def actualizar_form_url(self, id_encuesta: int, url: str):
        encuesta = self.obtener_encuesta(id_encuesta)
        encuesta.form_url = url
        self.repositorio.guardar_encuesta(encuesta)

    def crear_especialidad(self, id_encuesta: int, nombre: str):
        encuesta = self.obtener_encuesta(id_encuesta)
        if (not nombre):
            raise ValueError("El nombre de la especialidad no puede estar vacío")
        for especialidad in encuesta.especialidades:
            if (especialidad.nombre == nombre):
                raise ValueError("Ya existe una especialidad con ese nombre en esta encuesta")
        id_especialidad = encuesta.especialidades[len(encuesta.especialidades) - 1].id_especialidad + 1 if len(encuesta.especialidades) > 0 else 1
        especialidad = Especialidad(id_especialidad, nombre)
        encuesta.añadir_especialidad(especialidad)
        self.repositorio.guardar_encuesta(encuesta)
        return especialidad
    
    def obtener_especialidades(self, id_encuesta: int) -> list[Especialidad]:
        encuesta = self.obtener_encuesta(id_encuesta)
        return encuesta.especialidades

    def editar_especialidad(self, id_encuesta: int, id_especialidad: int, nombre: str):
        if (not nombre):
            raise ValueError("El nombre de la especialidad no puede estar vacío")
        encuesta = self.obtener_encuesta(id_encuesta)
        for e in encuesta.especialidades:
            if (e.nombre == nombre and e.id_especialidad != id_especialidad):
                raise ValueError("Ya existe una especialidad con ese nombre en esta encuesta")
        especialidad = encuesta.obtener_especialidad_por_id(id_especialidad)
        especialidad.nombre = nombre
        self.repositorio.guardar_encuesta(encuesta)

    def eliminar_especialidad(self, id_encuesta: int, id_especialidad: int):
        encuesta = self.obtener_encuesta(id_encuesta)
        encuesta.eliminar_especialidad(id_especialidad)
        self.repositorio.guardar_encuesta(encuesta)
        for materia in encuesta.materias:
            materia.eliminar_especialidad(id_especialidad)