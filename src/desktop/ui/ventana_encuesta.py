from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit
from services.servicio_encuestas import ServicioEncuestas
from services.servicio_materias import ServicioMaterias
from ui.ventana_materias import VentanaMaterias

class VentanaEncuesta(QMainWindow):
    def __init__(self, servicio_encuestas: ServicioEncuestas, servicio_materias: ServicioMaterias, id_encuesta: int):
        super().__init__()
        self.servicio_encuestas = servicio_encuestas
        self.servicio_materias = servicio_materias
        self.id_encuesta = id_encuesta
        encuesta = self.servicio_encuestas.obtener_encuesta(id_encuesta)

        self.ventana_materias = None

        self.setWindowTitle(encuesta.nombre)
        self.setMinimumSize(1066, 600)
        self.showMaximized()

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        # nombre
        label_nombre = QLabel(encuesta.nombre)
        label_nombre.setStyleSheet("font-size: 24px;")
        layout.addWidget(label_nombre)

        # fechas
        layout_fechas = QHBoxLayout()
        layout_fechas.setSpacing(10)

        label_fecha_inicio = QLabel("Fecha de inicio:")
        input_fecha_inicio = QLineEdit(encuesta.fecha_inicio.strftime("%d/%m/%Y"))
        input_fecha_inicio.setReadOnly(True)
        layout_fechas.addWidget(label_fecha_inicio)
        layout_fechas.addWidget(input_fecha_inicio)

        label_fecha_fin = QLabel("Fecha de fin:")
        input_fecha_fin = QLineEdit(encuesta.fecha_fin.strftime("%d/%m/%Y"))
        input_fecha_fin.setReadOnly(True)
        layout_fechas.addWidget(label_fecha_fin)
        layout_fechas.addWidget(input_fecha_fin)

        layout.addLayout(layout_fechas)

        # materias
        layout_materias = QHBoxLayout()
        boton_ver_materias = QPushButton("Ver materias")
        boton_ver_materias.setFixedSize(200, 50)
        boton_ver_materias.clicked.connect(self.mostrar_materias)
        layout_materias.addWidget(boton_ver_materias)
        layout.addLayout(layout_materias)

        container = QWidget()
        container.setLayout(layout)

        outer_layout = QHBoxLayout()
        outer_layout.addStretch()
        outer_layout.addWidget(container)
        outer_layout.addStretch()

        wrapper = QWidget()
        wrapper.setLayout(outer_layout)
        self.setCentralWidget(wrapper)

    def mostrar_materias(self):
        if (self.ventana_materias is None):
            self.ventana_materias = VentanaMaterias(self.servicio_materias, self.id_encuesta)
            self.ventana_materias.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)
            self.ventana_materias.destroyed.connect(self.limpiar_ventana_materias)
            self.ventana_materias.show()

    def limpiar_ventana_materias(self):
        self.ventana_materias = None

    def closeEvent(self, event):
        if (self.ventana_materias is not None):
            self.ventana_materias.close()
            self.ventana_materias = None
        event.accept()