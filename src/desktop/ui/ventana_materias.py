from PyQt6.QtCore import QModelIndex, Qt, QAbstractTableModel
from PyQt6.QtWidgets import QHeaderView, QMainWindow, QTableView, QVBoxLayout, QPushButton, QWidget, QGridLayout
from ui.error_dialog import ErrorDialog
from ui.confirmacion_dialog import ConfirmacionDialog
from ui.ventana_ce_materia import VentanaCrearEditarMateria
from services.servicio_materias import ServicioMaterias

class VentanaMaterias(QMainWindow):
    def __init__(self, servicio_materias: ServicioMaterias, id_encuesta: int):
        super().__init__()
        self.servicio_materias = servicio_materias
        self.id_encuesta = id_encuesta
        
        self.ventana_ce_materia = None
        
        self.setWindowTitle("Materias")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()

        self.tabla_materias = QTableView()
        self.materias_model = self.cargar_modelo_materias()
        self.tabla_materias.setModel(self.materias_model)
        self.tabla_materias.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.tabla_materias.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.tabla_materias.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla_materias)

        layout_botones = QGridLayout()
        layout_botones.setVerticalSpacing(0)
        layout_botones.setHorizontalSpacing(10)

        boton_agregar = QPushButton("Agregar materia")
        boton_agregar.clicked.connect(self.agregar_materia_pressed)
        layout_botones.addWidget(boton_agregar, 0, 0)

        boton_eliminar = QPushButton("Eliminar materia")
        boton_eliminar.clicked.connect(self.eliminar_materia_pressed)
        layout_botones.addWidget(boton_eliminar, 1, 0)

        boton_editar = QPushButton("Editar materia")
        boton_editar.clicked.connect(self.editar_materia_pressed)
        layout_botones.addWidget(boton_editar, 0, 1)


        boton_mover_arriba = QPushButton("↑")
        boton_mover_arriba.clicked.connect(lambda: self.mover_materia(-1))
        layout_botones.addWidget(boton_mover_arriba, 0, 2)
        boton_mover_abajo = QPushButton("↓")
        boton_mover_abajo.clicked.connect(lambda: self.mover_materia(1))
        layout_botones.addWidget(boton_mover_abajo, 1, 2)

        layout.addLayout(layout_botones)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def cargar_modelo_materias(self):
        try:
            materias = self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta)
            model = MateriasModel(materias)
            return model
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al cargar las materias: {str(e)}")
            error_dialog.exec()
            return MateriasModel([])
        
    def agregar_materia_pressed(self):
        if (self.ventana_ce_materia is None):
            if self.tabla_materias.selectionModel().hasSelection():
                orden = self.tabla_materias.selectionModel().selectedRows()[0].row() + 1 # +1 para agregar después de la seleccionada
            else:
                orden = -1
            self.ventana_ce_materia = VentanaCrearEditarMateria(self, True, orden)
            self.ventana_ce_materia.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.ventana_ce_materia.destroyed.connect(self.limpiar_ventana_ce_materia)
            self.ventana_ce_materia.show()

    def editar_materia_pressed(self):
        if (self.ventana_ce_materia is None and self.tabla_materias.selectionModel().hasSelection()):
            index = self.tabla_materias.selectionModel().selectedRows()[0]
            try:
                materia = self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta)[index.row()]
            except Exception as e:
                error_dialog = ErrorDialog(f"Error al obtener la materia: {str(e)}")
                error_dialog.exec()
                return
            self.ventana_ce_materia = VentanaCrearEditarMateria(self, False, index.row(), materia.codigo, materia.nombre, materia.tipo, materia.nombre_corto, materia.nombre_sin_espacios, materia.año)
            self.ventana_ce_materia.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.ventana_ce_materia.destroyed.connect(self.limpiar_ventana_ce_materia)
            self.ventana_ce_materia.show()

    def eliminar_materia_pressed(self):
        if self.tabla_materias.selectionModel().hasSelection():
            index = self.tabla_materias.selectionModel().selectedRows()[0].row()
            confirmacion_dialog = ConfirmacionDialog("Confirmar eliminación", "¿Estás seguro de que quieres eliminar esta materia?", lambda: self.eliminar_materia(index))
            confirmacion_dialog.exec()

    def limpiar_ventana_ce_materia(self):
        self.ventana_ce_materia = None

    def agregar_materia(self, codigo: str, nombre: str, tipo: str, nombre_corto: str, nombre_sin_espacios: str, año: int, orden: int):
        try:
            materia = self.servicio_materias.crear_materia(self.id_encuesta, codigo, nombre, tipo, nombre_corto, nombre_sin_espacios, año, orden)
            self.materias_model.actualizar_materias(
                self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta)
            )
            self.ventana_ce_materia.close()
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al agregar la materia: {str(e)}")
            error_dialog.exec()

    def editar_materia(self, id_materia: int, codigo: str, nombre: str, tipo: str, nombre_corto: str, nombre_sin_espacios: str, año: int):
        try:
            self.servicio_materias.editar_materia(self.id_encuesta, id_materia, codigo, nombre, tipo, nombre_corto, nombre_sin_espacios, año)
            self.materias_model.actualizar_materias(
                self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta)
            )
            self.ventana_ce_materia.close()
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al editar la materia: {str(e)}")
            error_dialog.exec()

    def mover_materia(self, direccion: int):
        if not self.tabla_materias.selectionModel().hasSelection():
            return
        index = self.tabla_materias.selectionModel().selectedRows()[0].row()
        nuevo_index = index + direccion
        if nuevo_index < 0 or nuevo_index >= self.materias_model.rowCount():
            return
        try:
            self.servicio_materias.intercambiar_materias(self.id_encuesta, index, nuevo_index)
            self.materias_model.actualizar_materias(
                self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta)
            )
            self.tabla_materias.selectRow(nuevo_index)
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al mover la materia: {str(e)}")
            error_dialog.exec()

    def eliminar_materia(self, id_materia: int):
        try:
            self.servicio_materias.eliminar_materia(self.id_encuesta, id_materia)
            self.materias_model.actualizar_materias(
                self.servicio_materias.obtener_materias_de_encuesta(self.id_encuesta)
            )
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al eliminar la materia: {str(e)}")
            error_dialog.exec()

class MateriasModel(QAbstractTableModel):
    def __init__(self, materias):
        super().__init__()
        self.materias = materias or []

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
                return materia.nombre_corto
            elif index.column() == 4:
                return str(materia.año)
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
                return "Nombre corto"
            elif section == 4:
                return "Año"
        return None

    def rowCount(self, parent = ...):
        return len(self.materias)
    
    def columnCount(self, parent = ...):
        return 5

    def actualizar_materias(self, materias):
        self.beginResetModel()
        self.materias = materias or []
        self.endResetModel()