from services.servicio_encuestas import ServicioEncuestas
from entities.materia import Materia
from entities.especialidad import Especialidad

class ServicioMaterias:
    def __init__(self, servicio_encuestas: ServicioEncuestas):
        self.servicio_encuestas = servicio_encuestas

    def obtener_materias_de_encuesta(self, id_encuesta: int) -> list:
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)
        return encuesta.materias
    
    def crear_materia(self, id_encuesta: int, codigo: str, nombre: str, tipo: str, id_especialidades: list[int], año: int, nombre_corto: str, nombre_sin_espacios: str, orden: int = -1):
        if (año < 1):
            raise ValueError("El año debe ser mayor a 0")
        
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)
        if tipo == "Teorico/Practico":
            tipo_int = 0
        elif tipo == "Teorico":
            tipo_int = 1
        elif tipo == "Practico":
            tipo_int = 2
        else:
            raise ValueError("Tipo de materia inválido")
        for materia in encuesta.materias:
            if (materia.codigo == codigo and (materia.tipo == tipo_int or materia.tipo == 0 or tipo_int == 0)):
                raise ValueError("Ya existe una materia con ese código del mismo tipo en la encuesta")
        
        especialidades_encuesta = self.servicio_encuestas.obtener_especialidades(id_encuesta)
        if len(especialidades_encuesta) > 0 and len(id_especialidades) == 0:
            raise ValueError("Debe seleccionar al menos una especialidad para la materia")
        for id_esp in id_especialidades:
            especialidad = None
            for e in especialidades_encuesta:
                if e.id_especialidad == id_esp:
                    especialidad = e
                    break
            if not especialidad:
                raise ValueError("Especialidad con id " + str(id_esp) + " no existe en la encuesta")
            if año > especialidad.años:
                raise ValueError("El año de la materia no puede ser mayor a los años de la especialidad " + especialidad.nombre)
            
        materia = Materia(codigo, nombre, tipo_int, nombre_corto, nombre_sin_espacios, año, id_especialidades)
        if (orden and orden >= 0 and orden <= len(encuesta.materias)):
            encuesta.añadir_materia_en_orden(materia, orden)
        else:
            encuesta.añadir_materia(materia)
        self.servicio_encuestas.guardar_encuesta(encuesta)
        return materia

    def editar_materia(self, id_encuesta: int, id_materia: int, codigo: str, nombre: str, tipo: str, id_especialidades: list[int], año: int, nombre_corto: str, nombre_sin_espacios: str):
        if (año < 1):
            raise ValueError("El año debe ser mayor a 0")
        
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)
        materia = encuesta.obtener_materia_por_indice(id_materia)

        if tipo == "Teorico/Practico":
            tipo_int = 0
        elif tipo == "Teorico":
            tipo_int = 1
        elif tipo == "Practico":
            tipo_int = 2
        else:
            raise ValueError("Tipo de materia inválido")
        for m in encuesta.materias:
            if (m.codigo == codigo and m != materia and (m.tipo == tipo_int or m.tipo == 0 or tipo_int == 0)):
                raise ValueError("Ya existe una materia con ese código del mismo tipo en la encuesta")
            
        especialidades_encuesta = self.servicio_encuestas.obtener_especialidades(id_encuesta)
        if len(especialidades_encuesta) > 0 and len(id_especialidades) == 0:
            raise ValueError("Debe seleccionar al menos una especialidad para la materia")
        for id_esp in id_especialidades:
            especialidad = None
            for e in especialidades_encuesta:
                if e.id_especialidad == id_esp:
                    especialidad = e
                    break
            if not especialidad:
                raise ValueError("Especialidad con id " + str(id_esp) + " no existe en la encuesta")
            if año > especialidad.años:
                raise ValueError("El año de la materia no puede ser mayor a los años de la especialidad " + especialidad.nombre)

        materia.codigo = codigo
        materia.nombre = nombre
        materia.tipo = tipo_int
        materia.nombre_corto = nombre_corto
        materia.nombre_sin_espacios = nombre_sin_espacios
        materia.año = año
        materia.especialidades = id_especialidades

        self.servicio_encuestas.guardar_encuesta(encuesta)

    def intercambiar_materias(self, id_encuesta: int, indice1: int, indice2: int):
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)
        encuesta.intercambiar_materias(indice1, indice2)
        self.servicio_encuestas.guardar_encuesta(encuesta)

    def eliminar_materia(self, id_encuesta: int, id_materia: int):
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)
        encuesta.eliminar_materia_por_indice(id_materia)
        self.servicio_encuestas.guardar_encuesta(encuesta)
