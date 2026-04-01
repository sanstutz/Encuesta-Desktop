from PyQt6.QtCore import QModelIndex, Qt, QAbstractTableModel
from PyQt6.QtWidgets import QHBoxLayout, QHeaderView, QMainWindow, QTableView, QVBoxLayout, QPushButton, QWidget
from ui.error_dialog import ErrorDialog
from ui.ventana_crear_materia import VentanaCrearMateria
from services.servicio_materias import ServicioMaterias

class VentanaMaterias(QMainWindow):
    def __init__(self, servicio_materias: ServicioMaterias, id_encuesta: int):
        super().__init__()
        self.servicio_materias = servicio_materias
        self.id_encuesta = id_encuesta
        
        self.ventana_crear_materia = None
        
        self.setWindowTitle("Materias")
        self.setMinimumSize(800, 600)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.tabla_materias = QTableView()
        self.materias_model = self.cargar_modelo_materias()
        self.tabla_materias.setModel(self.materias_model)
        self.tabla_materias.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.tabla_materias)

        layout_botones = QHBoxLayout()
        layout_botones.setSpacing(10)

        boton_agregar = QPushButton("Agregar materia")
        boton_agregar.clicked.connect(self.agregar_materia_pressed)
        layout_botones.addWidget(boton_agregar)
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
        if (self.ventana_crear_materia is None):
            self.ventana_crear_materia = VentanaCrearMateria(self)
            self.ventana_crear_materia.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.ventana_crear_materia.destroyed.connect(self.limpiar_ventana_crear_materia)
            self.ventana_crear_materia.show()

    def limpiar_ventana_crear_materia(self):
        self.ventana_crear_materia = None

    def agregar_materia(self, codigo: str, nombre: str, nombre_corto: str, nombre_sin_espacios: str, año: int):
        try:
            materia = self.servicio_materias.crear_materia(self.id_encuesta, codigo, nombre, nombre_corto, nombre_sin_espacios, año)
            self.materias_model.agregar_materia(materia)
        except Exception as e:
            error_dialog = ErrorDialog(f"Error al agregar la materia: {str(e)}")
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
                return materia.nombre_corto
            elif index.column() == 3:
                return materia.nombre_sin_espacios
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
                return "Nombre corto"
            elif section == 3:
                return "Nombre sin espacios"
            elif section == 4:
                return "Año"
        return None

    def rowCount(self, parent = ...):
        return len(self.materias)
    
    def columnCount(self, parent = ...):
        return 5
    
    def agregar_materia(self, materia):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self.materias.append(materia)
        self.endInsertRows()
        # self.layoutChanged.emit()

    def eliminar_materia(self, index):
        self.beginRemoveRows(QModelIndex(), index.row(), index.row())
        del self.materias[index.row()]
        self.endRemoveRows()