from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import random

from entities.encuesta import Encuesta
from entities.materia import Materia
from entities.especialidad import Especialidad

SCOPES = ["https://www.googleapis.com/auth/drive"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"

class ServicioFormulario:
    @staticmethod
    def obtener_credenciales() -> Credentials:
        creds = None
        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())
        return creds

    def __init__(self):
        self.creds = self.obtener_credenciales()
        self.service = build("forms", "v1", credentials=self.creds, discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)
        self.formId = None

    def crear_json_formulario(self, encuesta: Encuesta, descripcion: str):
        # crear formulario
        form = {
            "info": {
                "title": encuesta.nombre
            }
        }
        formulario = self.service.forms().create(body=form).execute()
        self.formId = formulario["formId"]

        self.proxima_posicion = 0

        # boton de codigo y descripcion
        primer_batch = {
            "requests": [
                {
                    "updateFormInfo": {
                        "info": {
                            "description": descripcion
                        },
                        "updateMask": "description"
                    }
                },
                {
                    "createItem": {
                        "item": {
                            "title": "Código",
                            "description": "Ingrese su código de alumno",
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "textQuestion": {
                                        "paragraph": False
                                    }
                                }
                            }
                        },
                        "location": {
                            "index": self.obtener_proxima_posicion()
                        }
                    }
                }
            ]
        }

        self.service.forms().batchUpdate(formId=formulario["formId"], body=primer_batch).execute()

        # secciones de elegir año segun especialidad
        secciones_especialidad = list()
        titulos_secciones_especialidad = list()
        for especialidad in encuesta.especialidades:
            titulo = especialidad.nombre
            seccion = {
                "createItem": {
                    "item": {
                        "title": titulo,
                        "pageBreakItem": {}
                    },
                    "location": {
                        "index": self.obtener_proxima_posicion()
                    }
                }
            }
            secciones_especialidad.append(seccion)
            titulos_secciones_especialidad.append(titulo)
        
        self.crear_secciones_con_dropdown(secciones_especialidad, titulos_secciones_especialidad, 1, "Seleccione su especialidad")

        # preguntas de horas por materia
        # los ultimos n elementos son las secciones de cada especialidad
        # el primer dropdown va en proxima_posicion - n + 1 (para quedar despues de la primer seccion)
        indice_selector = self.proxima_posicion - len(encuesta.especialidades) + 1

        for especialidad in encuesta.especialidades:
            secciones_año = list()
            titulos_secciones_año = list()
            for año in range(1, encuesta.obtener_ultimo_año() + 1):
                titulo = f"Materias de {año}º año de {especialidad.nombre}"
                seccion = {
                    "createItem": {
                        "item": {
                            "title": titulo,
                            "pageBreakItem": {}
                        },
                        "location": {
                            "index": self.obtener_proxima_posicion()
                        }
                    }
                }
                preguntas = self.crear_preguntas_por_especialidad_y_año(encuesta.materias, especialidad, año)
                secciones_año.append(seccion)
                secciones_año.extend(preguntas)
                titulos_secciones_año.append(titulo)
            self.crear_secciones_con_dropdown(secciones_año, titulos_secciones_año, indice_selector, f"Seleccione su año de cursado para {especialidad.nombre}")
            indice_selector += 2 # tiene que aumentar 1 por la seccion y otro por el selector
        return formulario["responderUri"]


    def crear_secciones_con_dropdown(self, secciones: list, titulos_secciones: list[str], posicion_dropdown: int, titulo: str, descripcion: str = ""):
        posicion_actual = self.obtener_proxima_posicion()

        resp_secciones = self.service.forms().batchUpdate(formId=self.formId, body={"requests": secciones}).execute()
        id_secciones = [
            reply["createItem"]["itemId"]
            for req, reply in zip(secciones, resp_secciones["replies"])
            if "createItem" in req and "pageBreakItem" in req["createItem"]["item"]
        ]

        batch = {
            "requests": [
                {
                    "createItem": {
                        "item": {
                            "title": titulo,
                            "description": descripcion,
                            "questionItem": {
                                "question": {
                                    "required": True,
                                    "choiceQuestion": {
                                        "type": "DROP_DOWN",
                                        "options": [{
                                            "value": titulos_secciones[i],
                                            "goToSectionId": id_secciones[i]
                                        } for i in range(len(id_secciones))],
                                    }
                                }
                            }
                        },
                        "location": {
                            "index": posicion_actual
                        }
                    }
                }
            ]
        }
        self.service.forms().batchUpdate(formId=self.formId, body=batch).execute()

        self.service.forms().batchUpdate(formId=self.formId, body={
            "requests": [
                {
                    "moveItem": {
                        "originalLocation": {
                            "index": posicion_actual
                        },
                        "newLocation": {
                            "index": posicion_dropdown
                        }
                    }
                }
            ]
        }).execute()

    def crear_preguntas_por_especialidad_y_año(self, materias: list[Materia], especialidad: Especialidad, año: int):
        materias_filtradas = [materia for materia in materias if especialidad.id_especialidad in materia.especialidades and materia.año == año]
        requests = [
            {
                "createItem": {
                    "item": {
                        "title": materia.nombre,
                        "description": f"¿Cuántas horas estudió el día de la fecha esta materia?",
                        "questionItem": {
                            "question": {
                                "required": False,
                                "textQuestion": {
                                    "paragraph": False
                                }
                            }
                        }
                    },
                    "location": {
                        "index": self.obtener_proxima_posicion()
                    }
                }
            } for materia in materias_filtradas
        ]
        return requests

    def obtener_proxima_posicion(self) -> int:
        pos = self.proxima_posicion
        self.proxima_posicion += 1
        return pos
    