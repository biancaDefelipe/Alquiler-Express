CREATE TABLE usuario (
    id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE CHECK(length(dni) <= 24),
    nombre TEXT NOT NULL CHECK(length(nombre) <= 50),
    apellido TEXT NOT NULL CHECK(length(apellido) <= 50),
    mail TEXT NOT NULL UNIQUE CHECK(length(mail) <= 50),
    telefono TEXT NOT NULL CHECK(length(telefono) <= 24),
    fecha_nacimiento TEXT NOT NULL CHECK(length(fecha_nacimiento) = 10),
    contrasenia TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(length(rol) <= 24),
    fecha_registro DATE NOT NULL,
    eliminado TEXT NOT NULL CHECK(length(eliminado) <= 2)
);

CREATE TABLE propiedad (
    id_propiedad INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL CHECK(length(titulo) <= 100),
    tipo TEXT NOT NULL CHECK(length(tipo) <= 24),
    localidad TEXT NOT NULL CHECK(length(localidad) <= 50),
    descripcion TEXT NULL CHECK(length(descripcion) <= 255),
    cantidad_banios INTEGER NOT NULL CHECK(cantidad_banios BETWEEN 1 AND 99),
    cantidad_habitaciones INTEGER NOT NULL CHECK(cantidad_habitaciones BETWEEN 1 AND 99),
    cantidad_huespedes INTEGER NOT NULL CHECK(cantidad_huespedes BETWEEN 1 AND 99),
    politica_cancelacion TEXT NOT NULL CHECK(length(politica_cancelacion) <= 100),
    metros_cuadrados NUMERIC(9, 2) NOT NULL CHECK(metros_cuadrados > 0),
    minimo_dias INTEGER NOT NULL CHECK(minimo_dias BETWEEN 1 AND 99),
    precio_por_dia NUMERIC(9, 2) NOT NULL CHECK(precio_por_dia > 0),
    calle TEXT NOT NULL CHECK(length(calle) <= 42),
    numero TEXT NOT NULL CHECK(length(numero) <= 12),
    piso TEXT NULL CHECK(length(piso) <= 3),
    departamento TEXT NULL CHECK(length(departamento) <= 4),
    esta_habilitada TEXT NOT NULL CHECK(length(esta_habilitada) <= 2),
    estado TEXT NOT NULL CHECK(length(estado) <= 50),
    calificacion NUMERIC(9, 2) NULL DEFAULT 0.0,
    total_calificaciones INTEGER NULL DEFAULT 0,
    suma_calificaciones INTEGER NULL DEFAULT 0
);

CREATE TABLE reserva (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_propiedad INTEGER NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    precio_total NUMERIC(9, 2) NOT NULL CHECK(precio_total > 0),
    medio_de_pago TEXT NOT NULL CHECK(length(medio_de_pago) <= 100),
    estado TEXT NOT NULL CHECK(length(estado) <= 100),
    fecha_check_in TEXT,
    fecha_check_out TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_propiedad) REFERENCES propiedad(id_propiedad),
    calificacion INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE pregunta (
    id_pregunta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_propiedad INTEGER NOT NULL,
    fecha DATE NOT NULL,
    esta_respondida TEXT NOT NULL CHECK(length(esta_respondida) <= 2),
    pregunta TEXT NOT NULL CHECK(length(pregunta) <= 155),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_propiedad) REFERENCES propiedad(id_propiedad)
);

CREATE TABLE respuesta (
    id_respuesta INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_pregunta INTEGER NOT NULL,
    fecha DATE NOT NULL,
    respuesta TEXT NOT NULL CHECK(length(respuesta) <= 155),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_respuesta) REFERENCES respuesta(id_respuesta)
);

CREATE TABLE comentario (
    id_comentario INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario INTEGER NOT NULL,
    id_reserva INTEGER NOT NULL,
    texto TEXT NOT NULL CHECK(length(texto) <= 500),
    fecha DATE NOT NULL,
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva),
    UNIQUE(id_usuario, id_reserva)
);
