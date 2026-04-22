from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QDateEdit, QHBoxLayout, QPushButton, QWidget, QStackedLayout, QSizePolicy
from ui.error_dialog import ErrorDialog
from entities.encuesta import Encuesta

class LayoutFechas(QVBoxLayout):
    def __init__(self, ventana_encuesta, encuesta: Encuesta):
        super().__init__()
        self.setSpacing(10)
        self.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.ventana_encuesta = ventana_encuesta
        self.fecha_inicio = encuesta.fecha_inicio
        self.fecha_fin = encuesta.fecha_fin

        self.bloqueado = False
        self.botones: list[QPushButton] = []

        # fecha inicio
        layout_fecha_inicio = QHBoxLayout()
        label_fecha_inicio = QLabel("Fecha de inicio:")
        self.input_fecha_inicio = QDateEdit(encuesta.fecha_inicio)
        self.input_fecha_inicio.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_fecha_inicio.setReadOnly(True)
        self.input_fecha_inicio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout_fecha_inicio.addWidget(label_fecha_inicio)
        layout_fecha_inicio.addWidget(self.input_fecha_inicio)
        layout_fecha_inicio.setStretch(1, 1)
        self.addLayout(layout_fecha_inicio)

        # fecha fin
        layout_fecha_fin = QHBoxLayout()
        label_fecha_fin = QLabel("Fecha de fin:")
        self.input_fecha_fin = QDateEdit(encuesta.fecha_fin)
        self.input_fecha_fin.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.input_fecha_fin.setReadOnly(True)
        self.input_fecha_fin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        layout_fecha_fin.addWidget(label_fecha_fin)
        layout_fecha_fin.addWidget(self.input_fecha_fin)
        layout_fecha_fin.setStretch(1, 1)
        self.addLayout(layout_fecha_fin)

        # botones
        contenedor_botones = QWidget()
        contenedor_botones.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        self.layout_botones = QStackedLayout()
        self.layout_botones.setSpacing(0)
        contenedor_botones.setLayout(self.layout_botones)

        contenedor_editar = QWidget()
        layout_editar = QHBoxLayout()
        layout_editar.setContentsMargins(0, 0, 0, 0)
        self.boton_editar = QPushButton("Editar")
        self.botones.append(self.boton_editar)
        layout_editar.addWidget(self.boton_editar)
        contenedor_editar.setLayout(layout_editar)
        self.layout_botones.addWidget(contenedor_editar)
        
        contenedor_confirmar = QWidget()
        layout_confirmar = QHBoxLayout()
        layout_confirmar.setContentsMargins(0, 0, 0, 0)
        self.boton_editar.clicked.connect(self.habilitar_edicion)
        self.boton_confirmar = QPushButton("Confirmar")
        self.boton_confirmar.clicked.connect(self.confirmar_edicion)
        self.boton_cancelar = QPushButton("Cancelar")
        self.boton_cancelar.clicked.connect(self.cancelar_edicion)
        layout_confirmar.addWidget(self.boton_confirmar)
        layout_confirmar.addWidget(self.boton_cancelar)
        contenedor_confirmar.setLayout(layout_confirmar)
        self.layout_botones.addWidget(contenedor_confirmar)

        self.addWidget(contenedor_botones)

    def bloquear_edicion(self, bloquear: bool):
        self.bloqueado = bloquear
        for boton in self.botones:
            boton.setEnabled(not bloquear)
        if bloquear:
            self.deshabilitar_edicion()
        

    def habilitar_edicion(self):
        if (self.bloqueado):
            return
        self.input_fecha_inicio.setReadOnly(False)
        self.input_fecha_fin.setReadOnly(False)
        self.input_fecha_inicio.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.input_fecha_fin.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.layout_botones.setCurrentIndex(1)

    def deshabilitar_edicion(self):
        self.input_fecha_inicio.setReadOnly(True)
        self.input_fecha_fin.setReadOnly(True)
        self.input_fecha_inicio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.input_fecha_fin.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.layout_botones.setCurrentIndex(0)

    def confirmar_edicion(self):
        fecha_inicio = self.input_fecha_inicio.date().toPyDate()
        fecha_fin = self.input_fecha_fin.date().toPyDate()
        exito = self.ventana_encuesta.editar_fechas(fecha_inicio, fecha_fin)
        if exito:
            self.fecha_inicio = fecha_inicio
            self.fecha_fin = fecha_fin
            self.deshabilitar_edicion()

    def cancelar_edicion(self):
        self.input_fecha_inicio.setDate(self.fecha_inicio)
        self.input_fecha_fin.setDate(self.fecha_fin)
        self.deshabilitar_edicion()