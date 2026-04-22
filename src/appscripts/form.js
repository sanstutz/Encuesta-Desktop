class Especialidad {
  constructor(id_especialidad, nombre, años) {
    this.id_especialidad = id_especialidad;
    this.nombre = nombre;
    this.años = años;
  }
}

class Materia {
  constructor(codigo, nombre, año, especialidades) {
    this.codigo = codigo;
    this.nombre = nombre;
    this.año = año;
    this.especialidades = especialidades;
  }
}

function mockEncuesta() {
  return {
    nombre: "Encuesta 1",
    especialidades: [
      new Especialidad(1, "Matemática", 5),
      new Especialidad(2, "Computación", 4)
    ],
    materias: [
      new Materia("AN1", "Análisi Matemático I", 1, [1, 2]),
      new Materia("AN2", "Análisis Matemático 2", 2, [1]),
      new Materia("AED", "Algoritmos y Estructuras de Datos", 2, [2])
    ]
  };
}

// main
function main() {
  const encuesta = mockEncuesta();

  crearForm(encuesta, "Encuesta del año 2026");
}

function crearForm(encuesta, descripcion) {
  const form = FormApp.create(encuesta.nombre, true);
  const hojaResultados = SpreadsheetApp.create("Resultados " + encuesta.nombre);

  form.setDescription(descripcion)
    .setAllowResponseEdits(false)
    .setCollectEmail(false)
    .setDestination(FormApp.DestinationType.SPREADSHEET, hojaResultados.getId());

  // input codigo
  form.addTextItem()
    .setTitle("Ingrese su código de alumno")
    .setRequired(true);

  // input especialidad
  const selectorEspecialidad = form.addListItem()
    .setTitle("Seleccione su especialidad")
    .setRequired(true);

  // choices del selector de especialidad
  const choicesEspecialidad = [];

  encuesta.especialidades.forEach(e => {
    // pagina de seleccion de año
    const { pagina: paginaAño, selectorAño } = crearPaginaAño(form, e.nombre);
    
    // crear la choice del selector de especialidad para ir a esta pagina
    const choiceEspecialidad = selectorEspecialidad.createChoice(e.nombre, paginaAño);
    choicesEspecialidad.push(choiceEspecialidad);

    // las choices del selector de año
    const choicesAño = [];

    for (let i = 1; i <= e.años; i++) {
      // pagina con materias por año y especialidad
      const paginaMaterias = crearPaginaMaterias(form, `Materias de ${i}º año de ${e.nombre}`, encuesta.materias, e.id_especialidad, i);
      // crear la choice del selector de año para ir a esta pagina
      const choiceAño = selectorAño.createChoice(`${i} año`,  paginaMaterias);
      choicesAño.push(choiceAño);
    }

    selectorAño.setChoices(choicesAño);
  });

  selectorEspecialidad.setChoices(choicesEspecialidad);

  const url = form.getPublishedUrl();

  return {
    url: url
  }
}

function crearPaginaAño(form, titulo) {
  const pagina = form.addPageBreakItem().setTitle(titulo);
  const selectorAño = form.addListItem()
    .setTitle("Seleccione su año de cursado")
    .setRequired(true);

  return { pagina, selectorAño }
}

function crearPaginaMaterias(form, titulo, materias, id_especialidad, año) {
  const pagina = form.addPageBreakItem()
    .setTitle(titulo)
    .setGoToPage(FormApp.PageNavigationType.SUBMIT);

  const filtradas = materias.filter(m => m.año === año && m.especialidades.find(id => id === id_especialidad));

  filtradas.forEach(m => {
    form.addTextItem()
      .setTitle(m.nombre)
      .setHelpText("¿Cuántas horas estudió el día de la fecha esta materia?")
      .setRequired(false)
      .setValidation(
        FormApp.createTextValidation()
          .requireNumberGreaterThan(0)
          .setHelpText("La cantidad de horas debe ser mayor a 0.")
          .build()
        );
  });

  return pagina;
}