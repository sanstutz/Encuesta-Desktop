from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QDateEdit
from services.servicio_encuestas import ServicioEncuestas
from services.servicio_materias import ServicioMaterias
from services.servicio_formulario import ServicioFormulario
from ui.ventana_encuesta.layout_fechas import LayoutFechas
from ui.ventana_encuesta.layout_especialidades import LayoutEspecialidades
from ui.ventana_encuesta.layout_materias import LayoutMaterias
from ui.error_dialog import ErrorDialog
from ui.confirmacion_dialog import ConfirmacionDialog
from ui.notificacion_dialog import NotificacionDialog

class VentanaEncuesta(QMainWindow):
    def __init__(self, servicio_encuestas: ServicioEncuestas, servicio_materias: ServicioMaterias, id_encuesta: int):
        super().__init__()
        self.servicio_encuestas = servicio_encuestas
        self.servicio_materias = servicio_materias
        self.id_encuesta = id_encuesta
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)

        self.nombre_encuesta = encuesta.nombre
        self.fecha_inicio = encuesta.fecha_inicio
        self.fecha_fin = encuesta.fecha_fin

        self.ventana_materias = None

        self.setWindowTitle(encuesta.nombre)
        self.setMinimumSize(1066, 600)
        self.showMaximized()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # nombre
        layout_nombre = QHBoxLayout()
        label_nombre = QLabel(encuesta.nombre)
        label_nombre.setStyleSheet("font-size: 30px;")
        layout_nombre.addWidget(label_nombre)
        layout_nombre.setStretch(0, 1)
        layout.addLayout(layout_nombre)

        # central
        layout_central = QHBoxLayout()
        layout.addLayout(layout_central, 9)

        layout_lateral_izq = QVBoxLayout()
        layout_lateral_izq.setSpacing(20)
        layout_central.addLayout(layout_lateral_izq, 3)

        # fondo
        layout_bottom = QHBoxLayout()
        layout.addLayout(layout_bottom, 1)

        # fechas
        layout_fechas = LayoutFechas(self, encuesta)
        layout_lateral_izq.addLayout(layout_fechas)

        # especialidades
        self.layout_especialidades = LayoutEspecialidades(self, encuesta.especialidades)
        layout_lateral_izq.addLayout(self.layout_especialidades)

        # materias
        self.layout_materias = LayoutMaterias(self, encuesta.materias, encuesta.especialidades)
        layout_central.addLayout(self.layout_materias, 7)

        # formulario
        layout_url = QVBoxLayout()
        layout_url.setSpacing(10)
        label_url = QLabel("URL del formulario:")
        layout_url.addWidget(label_url)
        url_formulario = QLineEdit(encuesta.form_url if encuesta.form_url else "")
        url_formulario.setReadOnly(True)
        layout_url.addWidget(url_formulario)
        layout_bottom.addLayout(layout_url, 7)

        layout_generar_formulario = QVBoxLayout()
        boton_generar_formulario = QPushButton("Generar formulario")
        boton_generar_formulario.clicked.connect(self.generar_formulario_pressed)
        layout_generar_formulario.addWidget(boton_generar_formulario)
        layout_generar_formulario.setStretch(0, 1)
        layout_bottom.addLayout(layout_generar_formulario, 3)

        # container
        container = QWidget()
        container.setLayout(layout)

        self.setCentralWidget(container)

    def editar_fechas(self, fecha_inicio, fecha_fin):
        try:
            self.servicio_encuestas.editar_encuesta(self.id_encuesta, self.nombre_encuesta, fecha_inicio, fecha_fin)
            return True
        except Exception as e:
            error = ErrorDialog(str(e))
            error.exec()
            return False

    def crear_especialidad(self, nombre: str):
        try:
            self.servicio_encuestas.crear_especialidad(self.id_encuesta, nombre)
            especialidades = self.servicio_encuestas.obtener_especialidades(self.id_encuesta)
            self.layout_especialidades.actualizar_especialidades(especialidades)
            self.layout_materias.actualizar_especialidades(especialidades)
            return True
        except Exception as e:
            error = ErrorDialog(str(e))
            error.exec()
            return False
        
    def editar_especialidad(self, id_especialiad: int, nombre: str):
        try:
            self.servicio_encuestas.editar_especialidad(self.id_encuesta, id_especialiad, nombre)
            especialidades = self.servicio_encuestas.obtener_especialidades(self.id_encuesta)
            self.layout_especialidades.actualizar_especialidades(especialidades)
            self.layout_materias.actualizar_especialidades(especialidades)
            return True
        except Exception as e:
            error = ErrorDialog(str(e))
            error.exec()
            return False

    def eliminar_especialidad(self, id_especialidad: int):
        try:
            self.servicio_encuestas.eliminar_especialidad(self.id_encuesta, id_especialidad)
            especialidades = self.servicio_encuestas.obtener_especialidades(self.id_encuesta)
            self.layout_especialidades.actualizar_especialidades(especialidades)
            self.layout_materias.actualizar_especialidades(especialidades)
            return True
        except Exception as e:
            error = ErrorDialog(str(e))
            error.exec()
            return False

    def limpiar_ventana_materias(self):
        self.ventana_materias = None

    def agregar_materia(self, codigo: str, nombre: str, tipo: str, especialidades: list[int], año: int, nombre_corto: str, nombre_sin_espacios: str, orden: int):
        try:
            self.servicio_materias.crear_materia(self.id_encuesta, codigo, nombre, tipo, especialidades, año, nombre_corto, nombre_sin_espacios, orden)
            self.layout_materias.actualizar_materias(self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta))
            return True
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al agregar la materia: {str(e)}")
            error_dialog.exec()
            return False

    def editar_materia(self, id_materia: int, codigo: str, nombre: str, tipo: str, especialidades: list[int], año: int, nombre_corto: str, nombre_sin_espacios: str):
        try:
            self.servicio_materias.editar_materia(self.id_encuesta, id_materia, codigo, nombre, tipo, especialidades, año, nombre_corto, nombre_sin_espacios)
            self.layout_materias.actualizar_materias(self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta))
            return True
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al editar la materia: {str(e)}")
            error_dialog.exec()
            return False

    def mover_materia(self, index: int, nuevo_index: int):
        try:
            self.servicio_materias.intercambiar_materias(self.id_encuesta, index, nuevo_index)
            self.layout_materias.actualizar_materias(self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta))
            return True
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al mover la materia: {str(e)}")
            error_dialog.exec()
            return False

    def eliminar_materia(self, id_materia: int):
        try:
            self.servicio_materias.eliminar_materia(self.id_encuesta, id_materia)
            self.layout_materias.actualizar_materias(self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta))
            return True
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al eliminar la materia: {str(e)}")
            error_dialog.exec()
            return False

    def generar_formulario_pressed(self):
        confirmacion = ConfirmacionDialog("Generar Formulario", "¿Está seguro que desea generar el formulario? Una vez generado se bloqueará la edición de los datos de la encuesta." \
        " Puede dar de baja el formulario para editar los datos, pero eso podría dejar las respuestas ya existentes incompatibles." \
        " Asegúrese de que los datos de la encuesta sean correctos.\nLa generación del formulario puede tardar unos segundos.",
        self.generar_formulario)
        confirmacion.exec()

    def generar_formulario(self):
        try:
            servicio_formulario = ServicioFormulario()
            encuesta = self.servicio_encuestas.obtener_encuesta(self.id_encuesta)
            url_formulario = servicio_formulario.crear_json_formulario(encuesta, encuesta.nombre)
            self.servicio_encuestas.actualizar_form_url(self.id_encuesta, url_formulario)
            notificacion = NotificacionDialog("Formulario generado", "El formulario se ha generado correctamente.")
            notificacion.exec()
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al generar el formulario: {str(e)}")
            error_dialog.exec()

    def closeEvent(self, event):
        if (self.ventana_materias is not None):
            self.ventana_materias.close()
            self.ventana_materias = None
        event.accept()