from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QTableView, QHeaderView
from entities.especialidad import Especialidad
from ui.ventana_encuesta.ventana_ce_especialidad import VentanaCrearEditarEspecialidad
from ui.confirmacion_dialog import ConfirmacionDialog

class LayoutEspecialidades(QVBoxLayout):
    def __init__(self, ventana_encuesta, lista_especialidades: list[Especialidad]):
        super().__init__()
        self.ventana_encuesta = ventana_encuesta

        self.ventana_ce_especialidad = None

        self.bloqueado = False
        self.botones: list[QPushButton] = []

        self.setSpacing(5)

        label = QLabel("Especialidades:")
        self.addWidget(label)

        self.tabla_especialidades = QTableView()
        self.especialidades_model = EspecialidadesModel(lista_especialidades)
        self.tabla_especialidades.setModel(self.especialidades_model)
        self.tabla_especialidades.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tabla_especialidades.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tabla_especialidades.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.addWidget(self.tabla_especialidades)

        botones_layout = QVBoxLayout()
        botones_layout.setSpacing(0)
        self.addLayout(botones_layout)

        boton_agregar = QPushButton("Agregar especialidad")
        boton_agregar.clicked.connect(self.agregar_especialidad_pressed)
        botones_layout.addWidget(boton_agregar)
        self.botones.append(boton_agregar)

        boton_editar = QPushButton("Editar especialidad")
        boton_editar.clicked.connect(self.editar_especialidad_pressed)
        botones_layout.addWidget(boton_editar)
        self.botones.append(boton_editar)

        boton_eliminar = QPushButton("Eliminar especialidad")
        boton_eliminar.clicked.connect(self.eliminar_especialidad_pressed)
        botones_layout.addWidget(boton_eliminar)
        self.botones.append(boton_eliminar)

    def bloquear_edicion(self, bloquear: bool):
        self.bloqueado = bloquear
        for boton in self.botones:
            boton.setEnabled(not bloquear)

    def actualizar_especialidades(self, nueva_lista: list[Especialidad]):
        self.especialidades_model.actualizar_especialidades(nueva_lista)

    def agregar_especialidad_pressed(self):
        if self.ventana_ce_especialidad is None and not self.bloqueado:
            self.ventana_ce_especialidad = VentanaCrearEditarEspecialidad(self.crear_especialidad, esCrear=True)
            self.ventana_ce_especialidad.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.ventana_ce_especialidad.destroyed.connect(self.limpiar_ventana_ce_especialidad)
            self.ventana_ce_especialidad.show()

    def crear_especialidad(self, nombre: str, años: int):
        resultado = self.ventana_encuesta.crear_especialidad(nombre, años)
        if resultado:
            self.ventana_ce_especialidad.close()

    def limpiar_ventana_ce_especialidad(self):
        self.ventana_ce_especialidad = None

    def editar_especialidad_pressed(self):
        if self.tabla_especialidades.selectionModel().hasSelection() and self.ventana_ce_especialidad is None and not self.bloqueado:
            index = self.tabla_especialidades.selectionModel().selectedRows()[0].row()
            especialidad = self.especialidades_model.especialidades[index]
            id_especialidad = especialidad.id_especialidad
            self.ventana_ce_especialidad = VentanaCrearEditarEspecialidad(lambda nombre, años: self.editar_especialidad(id_especialidad, nombre, años), False, especialidad.nombre, especialidad.años)
            self.ventana_ce_especialidad.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.ventana_ce_especialidad.destroyed.connect(self.limpiar_ventana_ce_especialidad)
            self.ventana_ce_especialidad.show()

    def editar_especialidad(self, id_especialiad: int, nombre: str, años: int):
        resultado = self.ventana_encuesta.editar_especialidad(id_especialiad, nombre, años)
        if resultado:
            self.ventana_ce_especialidad.close()

    def eliminar_especialidad_pressed(self):
        if self.tabla_especialidades.selectionModel().hasSelection() and self.ventana_ce_especialidad is None and not self.bloqueado:
            index = self.tabla_especialidades.selectionModel().selectedRows()[0].row()
            id_especialidad = self.especialidades_model.especialidades[index].id_especialidad
            dialog = ConfirmacionDialog("Borrar Especialidad", "¿Estás seguro de que deseas eliminar esta especialidad?", lambda: self.eliminar_especialidad(id_especialidad))
            dialog.exec()

    def eliminar_especialidad(self, id_especialidad: int):
        self.ventana_encuesta.eliminar_especialidad(id_especialidad)
        

class EspecialidadesModel(QAbstractTableModel):
    def __init__(self, especialidades: list[Especialidad]):
        super().__init__()
        self.especialidades = especialidades

    def rowCount(self, parent=None):
        return len(self.especialidades)

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            especialidad = self.especialidades[index.row()]
            return especialidad.nombre
        return None
    
    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "Especialidad"
        return None
    
    def actualizar_especialidades(self, nueva_lista: list[Especialidad]):
        self.beginResetModel()
        self.especialidades = nueva_lista
        self.endResetModel()