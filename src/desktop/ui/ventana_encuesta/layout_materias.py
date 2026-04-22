from PyQt6.QtCore import Qt, QAbstractTableModel
from PyQt6.QtWidgets import QHeaderView, QTableView, QVBoxLayout, QPushButton, QGridLayout, QLabel
from ui.confirmacion_dialog import ConfirmacionDialog
from ui.ventana_encuesta.ventana_ce_materia import VentanaCrearEditarMateria
from entities.materia import Materia
from entities.especialidad import Especialidad

class LayoutMaterias(QVBoxLayout):
    def __init__(self, ventana_encuesta, materias: list[Materia], especialidades: list[Especialidad]):
        super().__init__()
        
        self.ventana_ce_materia: VentanaCrearEditarMateria = None
        self.ventana_encuesta = ventana_encuesta

        self.especialidades = especialidades

        self.bloqueado = False
        self.botones: list[QPushButton] = []

        self.setSpacing(5)

        label = QLabel("Materias:")
        self.addWidget(label)

        self.tabla_materias = QTableView()
        self.materias_model = MateriasModel(materias, especialidades)
        self.tabla_materias.setModel(self.materias_model)
        self.tabla_materias.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tabla_materias.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tabla_materias.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.addWidget(self.tabla_materias)

        layout_botones = QGridLayout()
        layout_botones.setVerticalSpacing(0)
        layout_botones.setHorizontalSpacing(10)

        boton_agregar = QPushButton("Agregar materia")
        boton_agregar.clicked.connect(self.agregar_materia_pressed)
        layout_botones.addWidget(boton_agregar, 0, 0)
        self.botones.append(boton_agregar)

        boton_eliminar = QPushButton("Eliminar materia")
        boton_eliminar.clicked.connect(self.eliminar_materia_pressed)
        layout_botones.addWidget(boton_eliminar, 1, 0)
        self.botones.append(boton_eliminar)

        boton_editar = QPushButton("Editar materia")
        boton_editar.clicked.connect(self.editar_materia_pressed)
        layout_botones.addWidget(boton_editar, 0, 1)
        self.botones.append(boton_editar)

        boton_mover_arriba = QPushButton("↑")
        boton_mover_arriba.clicked.connect(lambda: self.mover_materia(-1))
        layout_botones.addWidget(boton_mover_arriba, 0, 2)
        boton_mover_abajo = QPushButton("↓")
        boton_mover_abajo.clicked.connect(lambda: self.mover_materia(1))
        layout_botones.addWidget(boton_mover_abajo, 1, 2)
        self.botones.append(boton_mover_arriba)
        self.botones.append(boton_mover_abajo)

        self.addLayout(layout_botones)

    def bloquear_edicion(self, bloquear: bool):
        self.bloqueado = bloquear
        for boton in self.botones:
            boton.setEnabled(not bloquear)

    def actualizar_materias(self, materias: list[Materia]):
        self.materias_model.actualizar_materias(materias)

    def actualizar_especialidades(self, especialidades: list[Especialidad]):
        self.especialidades = especialidades
        self.materias_model.actualizar_especialidades(especialidades)
        
    def agregar_materia_pressed(self):
        if (self.ventana_ce_materia is None and not self.bloqueado):
            if self.tabla_materias.selectionModel().hasSelection():
                orden = self.tabla_materias.selectionModel().selectedRows()[0].row() + 1 # +1 para agregar después de la seleccionada
            else:
                orden = -1
            self.ventana_ce_materia = VentanaCrearEditarMateria(self, self.especialidades, True, orden)
            self.ventana_ce_materia.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.ventana_ce_materia.destroyed.connect(self.limpiar_ventana_ce_materia)
            self.ventana_ce_materia.show()

    def editar_materia_pressed(self):
        if (self.ventana_ce_materia is None and self.tabla_materias.selectionModel().hasSelection() and not self.bloqueado):
            index = self.tabla_materias.selectionModel().selectedRows()[0].row()
            materia = self.materias_model.materias[index]
            self.ventana_ce_materia = VentanaCrearEditarMateria(self, self.especialidades, False, index, materia.codigo, materia.nombre, materia.tipo, materia.especialidades, materia.año, materia.nombre_corto, materia.nombre_sin_espacios)
            self.ventana_ce_materia.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.ventana_ce_materia.destroyed.connect(self.limpiar_ventana_ce_materia)
            self.ventana_ce_materia.show()

    def eliminar_materia_pressed(self):
        if self.tabla_materias.selectionModel().hasSelection() and self.ventana_ce_materia is None and not self.bloqueado:
            index = self.tabla_materias.selectionModel().selectedRows()[0].row()
            confirmacion_dialog = ConfirmacionDialog("Confirmar eliminación", "¿Estás seguro de que quieres eliminar esta materia?", lambda: self.eliminar_materia(index))
            confirmacion_dialog.exec()

    def limpiar_ventana_ce_materia(self):
        self.ventana_ce_materia = None

    def agregar_materia(self, codigo: str, nombre: str, tipo: str, especialidades: list[int], año: int, nombre_corto: str, nombre_sin_espacios: str, orden: int):
        resultado = self.ventana_encuesta.agregar_materia(codigo, nombre, tipo, especialidades, año, nombre_corto, nombre_sin_espacios, orden)
        if resultado:
            self.ventana_ce_materia.close()

    def editar_materia(self, id_materia: int, codigo: str, nombre: str, tipo: str, especialidades: list[int], año: int, nombre_corto: str, nombre_sin_espacios: str):
        resultado = self.ventana_encuesta.editar_materia(id_materia, codigo, nombre, tipo, especialidades, año, nombre_corto, nombre_sin_espacios)
        if resultado:
            self.ventana_ce_materia.close()

    def mover_materia(self, direccion: int):
        if not self.tabla_materias.selectionModel().hasSelection() or self.ventana_ce_materia is not None or self.bloqueado:
            return
        index = self.tabla_materias.selectionModel().selectedRows()[0].row()
        nuevo_index = index + direccion
        if nuevo_index < 0 or nuevo_index >= self.materias_model.rowCount():
            return
        resultado = self.ventana_encuesta.mover_materia(index, nuevo_index)
        if resultado:
            self.tabla_materias.selectRow(nuevo_index)

    def eliminar_materia(self, id_materia: int):
        self.ventana_encuesta.eliminar_materia(id_materia)

class MateriasModel(QAbstractTableModel):
    def __init__(self, materias: list[Materia], especialidades: list[Especialidad]):
        super().__init__()
        self.materias: list[Materia] = materias or []
        self.especialidades: list[Especialidad] = especialidades or []

    def data(self, index, role = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            materia = self.materias[index.row()]
            if index.column() == 0:
                return materia.codigo
            elif index.column() == 1:
                return materia.nombre
            elif index.column() == 2:
                return materia.tipo_str()
            elif index.column() == 3:
                return ", ".join([self.encontrar_especialidad(id).nombre for id in materia.especialidades])
            elif index.column() == 4:
                return str(materia.año)
            elif index.column() == 5:
                return materia.nombre_corto
        return None
    
    def headerData(self, section, orientation, role = ...):
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            if section == 0:
                return "Código"
            elif section == 1:
                return "Nombre"
            elif section == 2:
                return "Tipo"
            elif section == 3:
                return "Especialidad"
            elif section == 4:
                return "Año"
            elif section == 5:
                return "Nombre corto"
        return None

    def rowCount(self, parent = ...):
        return len(self.materias)
    
    def columnCount(self, parent = ...):
        return 6

    def actualizar_materias(self, materias):
        self.beginResetModel()
        self.materias = materias or []
        self.endResetModel()

    def actualizar_especialidades(self, especialidades):
        self.especialidades = especialidades or []
        self.layoutChanged.emit()

    def encontrar_especialidad(self, id_especialidad):
        for especialidad in self.especialidades:
            if especialidad.id_especialidad == id_especialidad:
                return especialidad
        return None
