from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton

class ConfirmacionDialog(QDialog):
    def __init__(self, nombre: str, mensaje: str, funcion_confirmar, funcion_cancelar=None):
        super().__init__()
        self.setWindowTitle(nombre)
        self.setMinimumSize(300, 150)

        self.funcion_confirmar = funcion_confirmar
        self.funcion_cancelar = funcion_cancelar

        layout = QVBoxLayout()
        label_mensaje = QLabel(mensaje)
        layout.addWidget(label_mensaje)

        layout_botones = QHBoxLayout()

        boton_confirmar = QPushButton("Confirmar")
        boton_confirmar.clicked.connect(self.confirmar)
        layout_botones.addWidget(boton_confirmar)

        
        boton_cancelar = QPushButton("Cancelar")
        boton_cancelar.clicked.connect(self.cancelar)
        layout_botones.addWidget(boton_cancelar)

        layout.addLayout(layout_botones)

        self.setLayout(layout)

    def confirmar(self):
        self.funcion_confirmar()
        self.close()

    def cancelar(self):
        if self.funcion_cancelar:
            self.funcion_cancelar()
        self.close()