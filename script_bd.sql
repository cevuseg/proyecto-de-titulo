-- Crear tabla de Roles
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL
);

-- Crear tabla de Usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(200) NOT NULL,
    id_rol INTEGER REFERENCES roles(id),
    activo BOOLEAN DEFAULT TRUE
);

-- Crear tabla de Reportes
CREATE TABLE reportes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion VARCHAR(500),
    url_powerbi VARCHAR(500) NOT NULL,
    area VARCHAR(100),
    id_usuario_subio INTEGER REFERENCES usuarios(id)
);

-- Crear tabla de Permisos
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    id_rol INTEGER REFERENCES roles(id),
    id_reporte INTEGER REFERENCES reportes(id),
    id_tipo_permiso INTEGER
);

-- Crear tabla de Logs de Acceso
CREATE TABLE logs_acceso (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuarios(id),
    id_reporte INTEGER REFERENCES reportes(id),
    fecha_acceso TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insertar roles por defecto
INSERT INTO roles (nombre) VALUES ('administrador');
INSERT INTO roles (nombre) VALUES ('usuario');

-- Insertar un usuario administrador inicial
INSERT INTO usuarios (nombre, correo, contrasena, id_rol, activo)
VALUES ('Admin Principal', 'cesar@empresa.com', '$2b$12$zHqYx8vGhhtAL7gfLkIVMuZef3EoqKfBXhhNiTf7Wl2Ogu47h5NSq
', 1, TRUE);

-- NOTA: La contraseña '$2b$12$abcdefghijklmnopqrstuv' es un hash Bcrypt de ejemplo.
-- Luego puedes cambiarlo o usar un registro real.
